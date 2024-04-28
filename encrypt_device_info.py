from simplecrypt import encrypt, decrypt
from pprint import pprint
import csv
import json

#---- Read in pertinent information from user
dc_in_filename = input('\nInput CSV filename (device-creds) :  ') or 'device-creds'
key            = input(  'Encryption key (cisco)          :  ') or 'cisco'

#---- Read in the device credentials from CSV file into list of device credentials
with open( dc_in_filename, 'r' ) as dc_in:
    device_creds_reader = csv.reader( dc_in )
    device_creds_list = [device for device in device_creds_reader]

print ('\n----- device_creds ---------------------------------------------------')
pprint( device_creds_list )

#---- Encrypt the device credentials using ken from user
encrypted_dc_out_filename = input('\nOutput encrypted filename (encrypted-device-creds):  ') or 'encrypted-device-creds'

with open( encrypted_dc_out_filename, 'wb' ) as dc_out:
    dc_out.write( encrypt( key, json.dumps( device_creds_list ) ) )

print ("woohoo I've encrypted the file")

print ('\n... getting credentials ...\n')
with open( encrypted_dc_out_filename, 'rb') as device_creds_file:
    device_creds_json = decrypt( key, device_creds_file.read() )

device_creds_list = json.loads( device_creds_json.decode('utf-8'))
pprint( device_creds_list )

print ('\n----- confirm: device_creds json in -----------------------------------')

# convert to dictionary of lists using dictionary comprehension
device_creds = { dev[0]:dev for dev in device_creds_list }
pprint( device_creds )
