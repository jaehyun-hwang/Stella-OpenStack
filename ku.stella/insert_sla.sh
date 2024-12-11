#!/bin/bash
# This script processes VM SLA settings and updates the /proc/gos_vm_info file accordingly.

# Assign input arguments to variables
vm=$1
sla_option=$2
sla_value=$3

# Initialize counter
count=0

# Get the PID of the VM by parsing its XML file
pid=$(sudo grep domstatus /var/run/libvirt/qemu/${vm}.xml | tr -dc '0-9')

# Extract the device string (e.g., disk name) from the VM's XML configuration
dev_string=$(virsh dumpxml "${vm}" | egrep 'nvme|sd')

# Extract the device name from the device string
name_dev=${dev_string#*\'}
name_dev=${name_dev%\'*}

# If name_dev is empty, set it to "null"
if [ -z "${name_dev}" ]; then
    name_dev="null"
fi

# If the SLA option is "n_maxcredit", adjust the PID to point to the vhost process
if [ "$sla_option" = "n_maxcredit" ]; then
    # Get the vhost process associated with the VM's PID
    vhost_cmd=$(ps -el | grep vhost | grep "${pid}")

    for vhost_pid in ${vhost_cmd}; do
        count=$((count + 1))

        if [ "${count}" = 4 ]; then
            pid=${vhost_pid}
        fi
    done
    # Optionally reset name_dev to "null"
    # name_dev="null"
fi

# Construct the command string with the gathered information
cmd="$vm $sla_option $sla_value ${pid} ${name_dev}"

# Write the command string to the /proc/gos_vm_info file
echo "${cmd}" > /proc/gos_vm_info
