"""
This file defines a wrapper to connect to an OpenStack cloud.
It assumes that we use DevStack for the configuration file.

Author: jmlim@os.korea.ac.kr
"""

import argparse
import os
import sys

import openstack
from openstack import utils
from openstack.config import loader

# Uncomment the following line to enable logging for debugging purposes
# utils.enable_logging(True, stream=sys.stdout)

# Defines the OpenStack Config cloud key in your config file,
# typically in $HOME/.config/openstack/clouds.yaml.
# This configuration determines where the examples will be run
# and what resource defaults will be used.
STELLA_CLOUD = os.getenv('OS_CLOUD', 'Stella')

# Load the OpenStack configuration
config = loader.OpenStackConfig()

# Establish a connection to the OpenStack cloud
CLOUD = openstack.connect(cloud=STELLA_CLOUD)


class Opts(object):
    def __init__(self, cloud_name='Stella-DevStack', debug=False):
        """
        Initialize the OpenStack connection options.

        :param cloud_name: Name of the cloud as defined in the clouds.yaml file.
        :param debug: Boolean flag to enable or disable debug mode.
        """
        # Set the cloud name
        self.cloud = cloud_name
        # Enable or disable debugging
        self.debug = debug
        # Specify the identity API version (v3 is the default for OpenStack)
        self.identity_api_version = '3'

    @staticmethod
    def _get_resource_value(resource_key, default):
        """
        Retrieve a resource value from the extra configuration.

        :param resource_key: The key of the resource to retrieve.
        :param default: The default value to return if the key is not found.
        :return: The value of the resource from the configuration, or the default.
        """
        return config.get_extra_config('example').get(resource_key, default)

    # Define default values for various OpenStack resources
    SERVER_NAME = 'openstacksdk-example'
    IMAGE_NAME = _get_resource_value.__func__('image_name', 'cirros-0.3.5-x86_64-disk')
    FLAVOR_NAME = _get_resource_value.__func__('flavor_name', 'm1.small')
    NETWORK_NAME = _get_resource_value.__func__('network_name', 'private')
    KEYPAIR_NAME = _get_resource_value.__func__('keypair_name', 'openstacksdk-example')

    # Define the SSH directory and private key file paths
    SSH_DIR = _get_resource_value.__func__(
        'ssh_dir', '{home}/.ssh'.format(home=os.path.expanduser("~")))
    PRIVATE_KEYPAIR_FILE = _get_resource_value.__func__(
        'private_keypair_file', '{ssh_dir}/id_rsa.{key}'.format(
            ssh_dir=SSH_DIR, key=KEYPAIR_NAME))

    # Define the name for the example image
    EXAMPLE_IMAGE_NAME = 'openstacksdk-example-public-image'

    @staticmethod
    def create_connection_from_config():
        """
        Create an OpenStack connection using the configuration file.

        :return: An openstack.connection.Connection object.
        """
        return openstack.connect(cloud=STELLA_CLOUD)

    @staticmethod
    def create_connection_from_args():
        """
        Create an OpenStack connection using command-line arguments.

        :return: An openstack.connection.Connection object.
        """
        parser = argparse.ArgumentParser()
        config = loader.OpenStackConfig()
        # Register command-line arguments for OpenStack configuration
        config.register_argparse_arguments(parser, sys.argv[1:])
        args = parser.parse_args()
        # Create a connection using the parsed arguments
        return openstack.connect(config=config.get_one(argparse=args))

    @staticmethod
    def create_connection(auth_url, region, project_name, username, password):
        """
        Create an OpenStack connection using explicit authentication parameters.

        :param auth_url: The authentication URL for the OpenStack identity service.
        :param region: The region name.
        :param project_name: The name of the project (tenant) to use.
        :param username: The username for authentication.
        :param password: The password for authentication.
        :return: An openstack.connection.Connection object.
        """
        return openstack.connect(
            auth_url=auth_url,
            project_name=project_name,
            username=username,
            password=password,
            region_name=region,
            app_name='Stella-OpenStack',
            app_version='0.1',
        )
