import os
import sys
import subprocess

result=subprocess.run([sys.executable,'-c', 'ansible all -m ping'],capture_output=True, text= True)
with open('connectivilty-log','w') as f:
    f.write(result.stdout)