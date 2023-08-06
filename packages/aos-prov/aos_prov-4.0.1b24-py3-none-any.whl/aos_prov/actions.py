#
#  Copyright (c) 2018-2022 Renesas Inc.
#  Copyright (c) 2018-2022 EPAM Systems Inc.
#
import time

from aos_prov.commands.command_provision import run_provision
from aos_prov.commands.download import download_and_save_multinode
from aos_prov.communication.cloud.cloud_api import CloudAPI
from aos_prov.utils.common import DOWNLOADS_PATH
from aos_prov.utils.user_credentials import UserCredentials


def create_new_unit(vm_name: str, uc: UserCredentials, disk_location: str, do_provision=False, nodes_count=2) -> []:
    if do_provision:
        cloud_api = CloudAPI(uc)
        cloud_api.check_cloud_access()

    from aos_prov.commands.command_vm_multi_node_manage import new_vm, start_vms
    vm_port = new_vm(vm_name, disk_location, nodes_count)

    if do_provision:
        start_vms(f'/AosUnits/{vm_name}')
        time.sleep(10)
        run_provision(f'127.0.0.1:{vm_port}', cloud_api, reconnect_times=40)


def start_vm(name: str) -> None:
    from aos_prov.commands.command_vm_multi_node_manage import start_vms
    start_vms(f'/AosUnits/{name}')


def download_image(download_url: str, force: bool = False):
    download_and_save_multinode(download_url, DOWNLOADS_PATH, force)
    print('Download finished. You may find Unit images in: ' + str(DOWNLOADS_PATH.resolve()))
