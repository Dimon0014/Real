import time
import  psutil
import subprocess

PROCNAME = 'casino.exe'
for proc in psutil.process_iter():
    # if proc.name() == PROCNAME:
    #     print('psutil_rabotaet nashel', proc.name)
        try:
            if proc.name() == PROCNAME:
                p = psutil.Process(proc.pid)
                print('psutil', p.username())
                time.sleep(1)
                print('psutil_rabotaet')
                #game.terminate()
                proc.kill()
        except:
            print('psutil_oshibka')
            pass