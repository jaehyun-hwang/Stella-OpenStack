import argparse
import logging
import os

# Import necessary modules from Flask for creating an API server
from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api

# Import a custom module to connect to OpenStack
import connect_openstack

# Initialize the Flask application
app = Flask(__name__)
api = Api(app)

"""
Stella-OpenStack Comment main file

Author: jmlim@os.korea.ac.kr
"""

class VM_info:
    # A class to store and manage VM information
    _list_vms = {}

    def print_all(self):
        # Return all stored VM information
        return self._list_vms

    def print_num(self):
        # Return the total number of VMs stored
        return len(self._list_vms) + 1

    def set_info(self, _vm_name, _instance_name, _project_id, _hypervisor_name, _hypervisor_ip, _sla_option, _sla_value):
        """
        Store VM information in the _list_vms dictionary.

        Parameters:
        - _vm_name: Name of the VM
        - _instance_name: Instance name of the VM
        - _project_id: Project ID associated with the VM
        - _hypervisor_name: Name of the hypervisor hosting the VM
        - _hypervisor_ip: IP address of the hypervisor
        - _sla_option: SLA option for the VM
        - _sla_value: SLA value for the VM
        """
        # Use the current length of the dictionary as the key
        num = len(self._list_vms)
        # Add the VM information to the dictionary
        self._list_vms[num] = {
            'vm_name': _vm_name,
            'instance_name': _instance_name,
            'project_id': _project_id,
            'hypervisor_name': _hypervisor_name,
            'hypervisor_ip': _hypervisor_ip,
            'SLA_Option': _sla_option,
            'SLA_Value': _sla_value
        }
        return len(self._list_vms)

    def print_SLA(self, _name):
        """
        Print the SLA options and values for a VM with the given name.
        """
        count = -1
        for tmp in self._list_vms:
            # Check if the VM name matches
            if _name in self._list_vms[tmp]["vm_name"]:
                count = tmp
                break
            else:
                print("N")  # Indicate that the VM was not found
        # (The SLA details can be printed or returned as needed)

    def get_instance_name_by_name(self, _name):
        """
        Retrieve the instance name of a VM given its name.

        Parameters:
        - _name: Name of the VM

        Returns:
        - _instance_name: The instance name of the VM
        """
        for count in self._list_vms:
            if _name in self._list_vms[count]["vm_name"]:
                _instance_name = self._list_vms[count]["instance_name"]
                break
        return _instance_name

    def get_sla_option_by_name(self, _name):
        """
        Retrieve the SLA option of a VM given its name.

        Parameters:
        - _name: Name of the VM

        Returns:
        - _sla_option: The SLA option of the VM
        """
        for count in self._list_vms:
            if _name in self._list_vms[count]["vm_name"]:
                _sla_option = self._list_vms[count]["SLA_Option"]
                break
        return _sla_option

    def get_sla_value_by_name(self, _name):
        """
        Retrieve the SLA value of a VM given its name.

        Parameters:
        - _name: Name of the VM

        Returns:
        - _sla_value: The SLA value of the VM
        """
        for count in self._list_vms:
            if _name in self._list_vms[count]["vm_name"]:
                _sla_value = self._list_vms[count]["SLA_Value"]
                break
        return _sla_value

    def set_SLA(self, _name, _SLA_Option, _SLA_Value):
        """
        Set the SLA option and value for a VM with the given name.

        Parameters:
        - _name: Name of the VM
        - _SLA_Option: The SLA option to set
        - _SLA_Value: The SLA value to set

        Returns:
        - count: The index of the VM in the _list_vms dictionary
        """
        count = -1
        for count in self._list_vms:
            if _name in self._list_vms[count]["vm_name"]:
                break
        if count != -1:
            # Update the SLA information
            self._list_vms[count].update(SLA_Option=_SLA_Option)
            self._list_vms[count].update(SLA_Value=_SLA_Value)
        return count


class hypervisor_info:
    # A class to store and manage hypervisor information
    _list_hypervisor = {}

    def set_data(self, _name, _ip):
        """
        Store hypervisor information.

        Parameters:
        - _name: Name of the hypervisor
        - _ip: IP address of the hypervisor
        """
        self._list_hypervisor[_name] = _ip

    def get_data(self, _name):
        """
        Retrieve the IP address of a hypervisor given its name.

        Parameters:
        - _name: Name of the hypervisor

        Returns:
        - IP address of the hypervisor
        """
        return self._list_hypervisor[_name]


class Stella_OpenStack(Resource):
    # A class representing the Stella OpenStack resource for the API

    def __init__(self, log_file=None):
        """
        Initialize the Stella OpenStack resource.

        Parameters:
        - log_file: Optional log file path
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger("Stella-OpenStack START")
        self.log_file = log_file

        if log_file:
            # Add a file handler if a log file is specified
            self.log_handler = logging.FileHandler(self.log_file)
            self.logger.addHandler(self.log_handler)

        self.__stop = False

        # Signal handling can be added here if needed
        # self.signal(signal.SIGINT, self.stop)
        # self.signal(signal.SIGTERM, self.stop)

    def main(self):
        # Main method to start the resource
        self.logger.info("STELLA: PID {0}".format(os.getpid()))

    def stop(self, signum, frame):
        # Method to handle stopping the resource gracefully
        self.__stop = True
        self.logger.info("STELLA: Signal {0}".format(signum))
        self.logger.info("STELLA: STOP")


# Global instances of the VM_info and hypervisor_info classes
hypervisors = hypervisor_info
vms = VM_info

# Stella-OpenStack API endpoints
# /stella : Check status of Stella scheduler and Stella-OpenStack
# /stella/vms : Returns the list of VMs and information of each VM
# /stella/vms/sla: Set SLA for a VM. Use instance name in Horizon as input
# /stella/hypervisor : Returns Hypervisor IP address

@app.route('/stella/', methods=['GET'])
def StellaAPI_Status():
    # Endpoint to check the status of Stella-OpenStack
    return "Stella-OpenStack is ON"

@app.route('/stella/vms', methods=['GET'])
def StellaAPI_listVMs():
    # Endpoint to list all VMs and their information
    return jsonify(vms.print_all(vms))

@app.route('/stella/vms/sla', methods=['POST'])
def StellaAPI_Set_SLA_VM():
    # Endpoint to set the SLA for a specific VM
    # Validate the incoming JSON data
    if not request.json or 'name' not in request.json:
        abort(400)
    if 'SLA_Option' not in request.json:
        abort(400)
    if 'SLA_Value' not in request.json:
        abort(400)

    # Extract data from the request
    _name = request.json['name']
    _SLA_option = request.json['SLA_Option']
    _SLA_value = request.json['SLA_Value']

    # Update the SLA information for the VM
    count = vms.set_SLA(vms, _name, _SLA_option, _SLA_value)
    instance_name = vms.get_instance_name_by_name(vms, _name)
    sla_option = vms.get_sla_option_by_name(vms, _name)
    sla_value = vms.get_sla_value_by_name(vms, _name)

    # Obtain root privileges if necessary
    olduid = 0
    if os.geteuid() != 0:
        # Running as a normal user; switch to root
        olduid = os.geteuid()
        print(olduid)
        os.seteuid(0)

    # Execute the SLA setting script with the appropriate arguments
    cmd_str = './insert_sla.sh' + ' ' + instance_name + ' ' + sla_option + ' ' + sla_value
    print(cmd_str)
    os.system(cmd_str)

    # Revert back to the original user privileges
    if olduid != 0:
        os.seteuid(olduid)

    if count < 0:
        # Return an error message if the operation failed
        return jsonify({'message': 'error'})
    else:
        # Return the updated VM information
        return jsonify(vms.print_all(vms))

@app.route('/stella/hypervisor', methods=['POST'])
def StellaAPI_SearchHypervisorsByName():
    # Endpoint to retrieve the IP address of a hypervisor by name
    if not request.json or 'name' not in request.json:
        abort(400)
    else:
        _name = request.json['name']
        ip_address = hypervisors.get_data(hypervisors, _name)
        return jsonify({'hypervisor_ip': ip_address})

# End of Stella-OpenStack API endpoints

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", help="log filename", default=None)
    parser.add_argument("--pid", help="pid filename", default='/tmp/stella.pid')
    args = parser.parse_args()

    # Initialize the Stella_OpenStack resource
    Stella = Stella_OpenStack(args.log)
    code = Stella.main()

    # Connect to OpenStack
    Stella.logger.info("STELLA: connect to Stella-cloud")
    conn = connect_openstack.Opts.create_connection_from_config()

    Stella.logger.info("STELLA: listing hypervisor")

    # Lists to store hypervisor names and IPs
    list_hypervisor_name = []
    list_hypervisor_ip = []

    # Retrieve hypervisor names
    for HYPERVISOR in conn.compute.hypervisors():
        list_hypervisor_name.append(HYPERVISOR.name)

    # Retrieve hypervisor IPs based on names
    for HYPERVISOR in conn.compute.hypervisors(list_hypervisor_name):
        list_hypervisor_ip.append(HYPERVISOR.host_ip)

    # Store hypervisor information in the hypervisors object
    count = 0
    for index in list_hypervisor_name:
        print(index)  # For debugging purposes
        hypervisors.set_data(hypervisors, list_hypervisor_name[count], list_hypervisor_ip[count])
        count += 1

    # Store VM information
    print("VM information")
    for VM in conn.compute.servers():
        ip = hypervisors.get_data(hypervisors, VM.hypervisor_hostname)
        # Initialize SLA options with placeholders '-'
        vms.set_info(vms, VM.name, VM.instance_name, VM.project_id, VM.hypervisor_hostname, ip, '-', '-')

    # Run the Flask API server
    app.run(host='0.0.0.0')
