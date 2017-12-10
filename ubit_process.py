import time

import subprocess


game= subprocess.Popen(["C:\Program Files (x86)\William Hill Casino\casino.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=False )
#subprocess.call('C:\"Program Files (x86)"\Google\Chrome\Application\chrome')terminate
time.sleep(10)
game.terminate()