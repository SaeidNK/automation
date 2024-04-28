import os
from pprint import pprint
os.system('clear')
print('\t1 OSPF')
print('\t2 BGP')
print('\t3 Tunnel')
print('\t0 Exit')
config= input ('Select the configuration to repair or apply:')
while config:
    if config=='1' or config=='OSPF':
        exec(open('Diff.py').read())
        exec(open('OSPF.py').read())
        exec(open('Backup.py').read())
    elif config=='2' or config=='BGP':
        exec(open('Diff.py').read())
        exec(open('BGP.py').read())
        exec(open('Backup.py').read())
    elif config=='3' or config=='Tunnel':
        exec(open('Diff.py').read())
        exec(open('Tunnel.py').read())
        exec(open('Backup.py').read())
    if config=='0' or config=='Exit':
        break
    os.system('cls')
    print('\t1 OSPF')
    print('\t2 BGP')
    print('\t3 Tunnel')
    print('\t0 Exit')
    config= input ('Select the configuration to repair or apply:')
    

  

    