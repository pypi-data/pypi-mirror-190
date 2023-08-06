#
#  Copyright (c) 2018-2022 Renesas Inc.
#  Copyright (c) 2018-2022 EPAM Systems Inc.
#

import os
import platform
import socket
import subprocess
import uuid
from pathlib import Path
from random import randint
from shutil import copyfile

from aos_prov.actions import download_image
from aos_prov.utils.common import DOWNLOADS_PATH, AOS_DISKS_PATH, DISK_IMAGE_DOWNLOAD_URL, NODE0_IMAGE_FILENAME, \
    NODE1_IMAGE_FILENAME
from aos_prov.utils.errors import AosProvError


def _is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def _delete_controller(vm_uuid: str, controller_name: str):
    command = [
        'VBoxManage', 'storagectl',
        vm_uuid,
        f'--name={controller_name}',
        '--controller=',
        '--remove',
    ]
    execute_command(command, catch_error=True)
def _create_storage_controller(vm_uuid: str, controller_name: str):
    """Create SATA controller for VM.
        Args:
             vm_uuid (str): UUID or Name of VM to attach controller.
             controller_name (str): Name of the controller.
    """
    command = [
        'VBoxManage', 'storagectl',
        vm_uuid,
        f'--name={controller_name}',
        '--add=sata',
        '--controller=IntelAhci',
        '--portcount=1',
        '--hostiocache=on',
        '--bootable=on'
    ]
    execute_command(command)


def _attach_disk(vm_uuid: str, attach_to_controller_name: str, disk_location: str):
    """Attach disk file to the controller.
        Args:
             vm_uuid (str): UUID or Name of VM to attach controller.
             attach_to_controller_name (str): Name of the controller where disk will be attached.
             disk_location (str): path to the disk file.
    """
    command = [
        'VBoxManage', 'storageattach',
        vm_uuid,
        '--storagectl', attach_to_controller_name,
        '--port', '0',
        '--type', 'hdd',
        '--medium', disk_location
    ]
    execute_command(command)


def _create_network(network_name: str):
    print('Creating network for unit...')
    command = [
        'VBoxManage',
        'natnetwork',
        'add',
        '--netname',
        network_name,
        '--network',
        '10.0.0.0/24',
        '--enable',
        '--dhcp',
        'on'
    ]
    execute_command(command)


def _forward_port(network_name: str, forward_name: str, from_ip: str, from_port: int, to_port=None) -> int:
    if to_port is None:
        to_port = randint(8090, 8999)
        while _is_port_in_use(to_port):
            to_port = randint(8090, 8999)

    command = [
        'VBoxManage',
        'natnetwork',
        'modify',
        '--netname',
        network_name,
        '--port-forward-4',
        f"{forward_name}:tcp:[]:{to_port}:[{from_ip}]:{from_port}",
    ]

    execute_command(command)
    return to_port


def new_vm(vm_name: str, disk_location: str, nodes_count=2) -> ():
    print('Creating a new virtual machines...')

    disk_location_path = Path(disk_location)

    if not ((disk_location_path / NODE0_IMAGE_FILENAME).exists()) or \
        not ((disk_location_path / NODE1_IMAGE_FILENAME).exists()):
        if disk_location_path == AOS_DISKS_PATH:
            print('Local images not found. Downloading...')
            download_image(DISK_IMAGE_DOWNLOAD_URL)
        else:
            raise AosProvError(f'Disk images not found in directory {disk_location}. Can\'t proceed!')

    nodes = [
        {
            'name': 'node0',
            'uuid': str(uuid.uuid4()),
            'disk_name': NODE0_IMAGE_FILENAME,
            'disk_location': Path(DOWNLOADS_PATH / NODE0_IMAGE_FILENAME)
        }
    ]

    if nodes_count != 1:
        nodes.append(
            {
                'name': 'node1',
                'uuid': str(uuid.uuid4()),
                'disk_name': NODE1_IMAGE_FILENAME,
                'disk_location': Path(DOWNLOADS_PATH / NODE1_IMAGE_FILENAME)
            }
        )

    units_network_name = f'aos-network-{vm_name}'
    _create_network(units_network_name)
    provisioning_port = _forward_port(
        units_network_name,
        forward_name='provisioningPortForward',
        from_ip='10.0.0.100',
        from_port=8089
    )

    node0_ssh_port = _forward_port(
        units_network_name,
        forward_name='node0ssh',
        from_ip='10.0.0.100',
        from_port=22
    )

    node1_ssh_port = _forward_port(
        units_network_name,
        forward_name='node1ssh',
        from_ip='10.0.0.101',
        from_port=22
    )

    for node in nodes:
        create_node_vm(
            node['name'],
            node['uuid'],
            f'/AosUnits/{vm_name}',
            node['disk_location'],
            node['disk_name'],
            units_network_name
        )

    return provisioning_port, node0_ssh_port, node1_ssh_port


def create_node_vm(vm_name: str, vm_uuid: str, group: str, original_disk_path: Path, disk_name: str, network_name):
    create_vm_command = [
        'VBoxManage', 'createvm',
        f'--name={vm_name}',
        '--ostype=Linux_64',
        f'--uuid={vm_uuid}',
        f'--groups={group}',
        '--default',
        '--register'
    ]

    cpu_count = 1
    if platform.system() == 'Windows':
        cpu_count = 4

    set_vm_params = [
        'VBoxManage', 'modifyvm',
        vm_uuid,
        '--memory=1024',
        '--firmware=efi',
        f'--cpus={cpu_count}'
    ]

    set_vm_net = [
        'VBoxManage', 'modifyvm',
        vm_uuid,
        '--nic1=natnetwork',
        f'--nat-network1={network_name}'
    ]

    execute_command(create_vm_command)
    execute_command(set_vm_params)
    execute_command(set_vm_net)
    _delete_controller(vm_uuid, 'SATA')
    _delete_controller(vm_uuid, 'IDE')

    _create_storage_controller(vm_uuid, 'SATA')

    destination_image = str((_find_vm_location(vm_uuid) / disk_name).resolve())
    copyfile(original_disk_path.absolute(), destination_image)
    _attach_disk(vm_uuid, 'SATA', disk_location=destination_image)


def _find_vm_location(vm_uuid) -> Path:
    set_vm_params = [
        'VBoxManage', 'showvminfo',
        vm_uuid,
        '--machinereadable'
    ]

    response = execute_command(set_vm_params)

    for row in response.splitlines():
        param = row.split('=')
        if param[0] == 'CfgFile':
            return Path(param[1].replace('"', '')).parent


def start_vms(group: str):
    vms_to_start = []
    list_vms = ['VBoxManage', 'list', 'vms']
    vms = execute_command(list_vms)

    for vm in vms.splitlines():
        guid = vm[vm.find('{')+1:vm.find('}')]
        info_command = ['VBoxManage', 'showvminfo', guid, '--machinereadable']
        info = execute_command(info_command)

        for row in info.splitlines():
            if row.startswith('groups='):
                print(row)
                groups = row.replace('"', '').split('=')[1]
                if group in groups:
                    vms_to_start.append(guid)
                    break


    print(vms_to_start)
    for vm_guid in vms_to_start:
        start_command = ['VBoxManage', 'startvm', vm_guid, '--type=gui']
        execute_command(start_command)


def execute_command(command, catch_error=False) -> str:
    print(' '.join(command))

    return_code = subprocess.run(command, shell=True, env=os.environ.copy(),  capture_output=True)
    print(return_code.returncode)
    if return_code.returncode == 0:
        # print(return_code.stdout.decode("utf-8"))
        return return_code.stdout.decode("utf-8")
    else:
        if not catch_error:
            # for z in return_code.stderr.decode("utf-8").splitlines():
            #     print(z)
            raise AosProvError(return_code)


# vm_name = 'alalala11'
# create_node_vm(vm_name, str(uuid.uuid4()) , f'/AosUnits/{vm_name}', Path(DOWNLOADS_PATH / 'aos-node1.vmdk'), 'aos-disk-node1.vmdk', '')


# print(_find_vm_location('52acdf1d-f895-4ac4-84f0-653063865df5'))

# new_vm(vm_name, AOS_DISKS_PATH)
