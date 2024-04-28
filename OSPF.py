from simplecrypt import encrypt, decrypt
from pprint import pprint
from netmiko import ConnectHandler
import json
from time import time
import os.path

#------------------------------------------------------------------------------
def read_devices( devices_filename ):

    devices = {}  # create our dictionary for storing devices and their info

    with open( devices_filename ) as devices_file:

        for device_line in devices_file:

            device_info = device_line.strip().split(',')  #extract device info from line

            device = {'ipaddr': device_info[0],
                      'type':   device_info[1],
                      'name':   device_info[2]}  # create dictionary of device objects ...

            devices[device['ipaddr']] = device  # store our device in the devices dictionary
                                                # note the key for devices dictionary entries is ipaddr

    print ('---------------------------------------')
    print (' Devices Info')
    print ('-----------------------------------------')
    pprint( devices )

    return devices

#------------------------------------------------------------------------------
def read_device_creds( device_creds_filename, key ):

    print ('\n... getting credentials ...\n')
    with open( device_creds_filename, 'rb') as device_creds_file:
        device_creds_json = decrypt( key, device_creds_file.read() )

    device_creds_list = json.loads( device_creds_json.decode('utf-8'))
    pprint( device_creds_list )
    device_creds_list= tuple(device_creds_list)

    print("---------------------------------------------")
    print (' Devices_creds')
    print("---------------------------------------------")

    # convert to dictionary of lists using dictionary comprehension
    for device_creds in device_creds_list :
    #device_creds = {dev[0]:dev for dev in tuple(device_creds_list) }
        pprint( device_creds )
        return device_creds

#------------------------------------------------------------------------------
def config_worker( device, creds ):

   
    device_type = 'cisco_ios'   

    print ('---- Connecting to device {0}, username={1}, password={2}'.format( device['ipaddr'],
                                                                                creds[1], creds[2] ))

    #---- Connect to the device
    session = ConnectHandler( device_type=device_type, ip=device['ipaddr'],
                                                       username=creds[1], password=creds[2],allow_agent=False, ssh_strict= False, conn_timeout=20,banner_timeout=20, auth_timeout=20)
    #session = ConnectHandler( device_type=device_type, ip='172.16.0.1',  # Faking out IP address for now
    #                                                   username=creds[1], password=creds[2] )

    """if device_type == 'cisco_ios':
    #---- Use CLI command to get configuration data from device
        print ('---- Getting configuration from device')
        config_data = session.send_command('show run')"""
    print("---------------------------------------------")
    print('Apply OSPF configuration')
    Cfile='/home/devasc/device-creds/OSPF/'+ device['name']+ '-ospf'
    """with open (device['name']+ '-ospf', 'r') as f:
        lines= f.readlines()
    print(lines)"""
    print("---------------------------------------------")
    if os.path.exists(Cfile):
    #lines =['router ospf 1', 'network 192.168.2.0 0.0.0.3 area 0', 'network 192.168.150.0 0.0.0.0 area 0']
        ospfoutput = session.send_config_from_file(Cfile,delay_factor=2,max_loops=600)
        session.save_config()
        print(ospfoutput)
    else:
        print(device['name']+ ' does not have any OSPF configuration')    
   
   
    #---- Write out configuration information to file
    config_data = session.send_command('show run')
    config_filename = '/home/devasc/device-creds/backup/config-' + device['ipaddr']  # Important - create unique configuration file name

    print ('---- Writing configuration: ', config_filename)
    with open( config_filename, 'w' ) as config_out:  config_out.write( config_data )

    session.disconnect()

    return


#==============================================================================
# ---- Main: Get Configuration
#==============================================================================

devices = read_devices( 'devices-file' )
creds   = read_device_creds( 'encrypted-device-creds', 'cisco' )
print(creds)
starting_time = time()

print ('\n---- Begin get config sequential ------\n')
print(devices)
for ipaddr,device in devices.items():
   # print(type(device))
    print ('Getting config for: ', device)
    config_worker(device, creds)

print ('\n---- End get config sequential, elapsed time=', time()-starting_time)
