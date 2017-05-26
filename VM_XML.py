import os
from xml.dom.minidom import parseString


def eth_device_file_write(file_name_and_path,ip,netmask,network):
    target_one = open(file_name_and_path, 'w')

    target_one.write("DEVICE=eth0")
    target_one.write("\n")
    target_one.write("BOOTPROTO=static")
    target_one.write("\n")
    target_one.write("BROADCAST="+broadcastip )
    target_one.write("\n")
    target_one.write("IPADDR="+ip)
    target_one.write("\n")
    target_one.write("NETMASK="+netmask)
    target_one.write("\n")
    target_one.write("NETWORK="+network)
    target_one.write("\n")
    target_one.write("ONBOOT=yes")

    target_one.close()


def network_device_file_write(file_name_and_path,gateway):
    target_two = open(file_name_and_path, 'w')

    target_two.write("NETWORKING=yes")
    target_two.write("\n")
    target_two.write("HOSTNAME=server.domain.com")
    target_two.write("\n")
    target_two.write("GATEWAY="+gateway)

    target_two.close()

def findXmlSection(dom, sectionName):
   sections = dom.getElementsByTagName(sectionName)
   return sections[0]

def getPropertyMap(ovfEnv):
   dom = parseString(ovfEnv)
   section = findXmlSection(dom, "PropertySection")
   propertyMap = {}
   for property in section.getElementsByTagName("Property"):
      key   = property.getAttribute("oe:key")
      value = property.getAttribute("oe:value")
      propertyMap[key] = value
   dom.unlink()
   return propertyMap




ovfEnv = open("/media/OVF ENV/ovf-env.xml", "r").read()

propertyMap = getPropertyMap(ovfEnv)

ip      = propertyMap["vami.ip0.HP_CMC"]
netmask = propertyMap["vami.netmask0.HP_CMC"]
gateway = propertyMap["vami.gateway.HP_CMC"]
broadcastip = "10.207.0.255"
network = "10.207.0.0"

print(ip)
print(netmask)
print(gateway)

eth_device_file_write("/etc/sysconfig/network-scripts/ifcfg-eth0",ip,netmask,network)
network_device_file_write("/etc/sysconfig/network",gateway)
#os.system("ifconfig eth0 %s netmask %s up" % (ip, netmask))
os.system("service network restart")
os.system("route add default gw %s eth1" % (gateway))

