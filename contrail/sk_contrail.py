import os
import sys
import psutil
from oslo_config import cfg
from utils import helpers
from utils.configsk import configSetup
from deploy_contrail import reImageAndDeploy

CONF = cfg.CONF
SK_ENV_FILE = 'pockit_env.conf'

class deployContrail(object):

    def __init__(self):
        pass

    def check_config_file_exists(self):
        install_dir = helpers.from_project_root('conf/')
        cfg_file = os.path.join(install_dir, SK_ENV_FILE)
        if not os.path.exists(os.path.join(install_dir, SK_ENV_FILE)):
            print "Missing required configuration file {}".format(cfg_file)
            sys.exit(1)
        print "Configuration file {} exists".format(cfg_file)


if __name__ == '__main__':

    #prep before re-imaging OS and provisioning contrail
    contrail = deployContrail()
    contrail.check_config_file_exists()

    #read conf file
    config = configSetup()
    config.set_base_config_options()

    try:
        config.load_configs(['conf/{}'.format(SK_ENV_FILE)])
        print "Loaded configuration file successfully"
    except cfg.RequiredOptError as e:
        print "Missing required input in pockit_env.conf file, {0}: {1}".format(SK_ENV_FILE, e)
        sys.exit(1)

    config.set_deploy_physical_server_config_options()
    config.set_deploy_virtual_server_config_options()

    #reimage VM, BMS and deploy contrail
    reimage = reImageAndDeploy()
    reimage.check_sm_status()
    reimage.copy_iso_contrail_images()
    reimage.create_cluster_json_file()
    reimage.create_image_json_file()
    reimage.create_vm_server_json_files()
    reimage.create_bms_server_json_files()
    reimage.copy_json_files_to_sm()
    reimage.reimage_vms()
    reimage.reimage_bms()
    reimage.wait_bms_reboot()
    reimage.provision_contrail()
    sys.exit(0)
