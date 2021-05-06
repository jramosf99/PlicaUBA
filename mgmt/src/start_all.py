import os
import time
os.system("xhost +")
os.system("python3 /opt/plica/watchdog/src/sensor-watchdogUBA1.py /opt/plica/watchdog/src/watchdogconfUBA1.cfg &")
os.system("python3 /opt/plica/watchdog/src/sensor-watchdogUBA2.py /opt/plica/watchdog/src/watchdogconfUBA2.cfg &")
os.system("python3 /opt/plica/watchdog/src/sensor-watchdogUBA3.py /opt/plica/watchdog/src/watchdogconfUBA3.cfg &")
os.system("python3 /opt/plica/watchdog/src/sensor-watchdogUBA4.py /opt/plica/watchdog/src/watchdogconfUBA4.cfg &")
os.system("python3 /opt/plica/watchdog/src/sensor-watchdogUBA5.py /opt/plica/watchdog/src/watchdogconfUBA5.cfg &")
os.system("python3 /opt/plica/watchdog/src/sensor-watchdogUBA6.py /opt/plica/watchdog/src/watchdogconfUBA6.cfg &")
os.system("python3 /opt/plica/watchdog/src/sensor-watchdogUBA7.py /opt/plica/watchdog/src/watchdogconfUBA7.cfg &")
os.system("python3 /opt/plica/uba/src/general.py /opt/plica/uba/src/UBA.cfg &")
os.system("python3 /home/plica/mgmt/mgmt_daemon.py /home/plica/mgmt/mgmt_daemon_4_watchdog.cfg &")
while True:
    time.sleep(10)
