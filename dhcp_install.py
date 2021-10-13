#!/usr/bin/python3
import os
import threading
import termcolor

interface = "eth0"
sever_name = "dhcp.monreseau.tg"
ip_add = "192.168.100.1"
subnet_mask = "255.255.255.0"
ip_dns_server = "192.168.100.1"
domain_name = "monreseau.tg"
add_router = "192.168.100.254"
broadcast = "192.168.100.255"
sub_net = "192.168.100.0"
rang_min = "192.168.100.50"
rang_max = "192.168.100.55"


cmd = ["apt-get update && apt-get upgrade",
       "apt-get install isc-dhcp-server",
       f"echo 'INTERFACES=\"{interface}\"' >> /etc/default/isc-dhcp-server",
       "conf_file",
       f"ifconfig {interface} {ip_add} netmask {subnet_mask}"]


line = ["#",
        "# Sample configuration file for ISC dhcpd for Debian",
        "#",
        f" server-name \"{sever_name}\";",
        f" option subnet-mask {subnet_mask};",
        f" option domain-name-servers {ip_dns_server};",
        f" option domain-name \"{domain_name}\";",
        f" option routers {add_router};",
        f" option broadcast-address {broadcast};",
        " default-lease-time 7200;",
        " max-lease-time 7200;",
        f" subnet {sub_net} netmask {subnet_mask}" + " {",
        f"	range {rang_min} {rang_max};",
        "}"]


comment = ["Updating of the system ...",
           "Downloading of isc-dhcp-server ...",
           "Setting of listening interface ...",
           "configuration of dhcpd.conf file ...",
           "ip address setting"]


def execute(cmd, comment):
    if cmd == "conf_file":
        dhcpd_conf()
    else:
        try:
            answer_cmd = os.system(cmd)
            if answer_cmd == 0:
                print(termcolor.colored(comment + "done. ", "green"))
            else:
                print(termcolor.colored(comment + "failed.", "red"))
        except:
            print(termcolor.colored(comment + "failed.", "red"))

        # cmd = os.system(cmd)
        # print(cmd.read())
        # print(termcolor.colored("done.", "green"))


# except:
# print(termcolor.colored(comment +"failed.", "red"))
# return print(cmd)


def exec_cmd(cmds, comment):
    for ind, cmd in enumerate(cmds):
        print(comment[ind])
        thr = threading.Thread(target=execute(cmd, comment[ind]))
        thr.start()
        thr.join()


def dhcpd_conf():
    # clean dhcd.conf file
    os.system("echo '' > /etc/dhcp/dhcpd.conf")
    # rewrite it
    for elt in line:
        cmd = f"echo '{elt}' >> /etc/dhcp/dhcpd.conf"
        os.system(cmd)


def check_config():
    user_answer = ""
    while user_answer != "yes" or user_answer != "yes" or user_answer != "n" or user_answer != "no":
        user_answer = input("Do you want to check the configuration ?(y/n or yes/no)")
        if user_answer == "yes" or user_answer == "y":
            cmd = "dhcpd -t -cf /etc/dhcp/dhcpd.conf"
            try:
                answer_cmd = os.system(cmd)
                if answer_cmd == 0:
                    print(termcolor.colored("done. ", "green"))
                else:
                    print(termcolor.colored("check failed.", "red"))
            except:
                print(termcolor.colored("check failed.", "red"))
        else:
            pass
        break


def start():
    user_answer = ""
    while user_answer != "yes" or user_answer != "yes" or user_answer != "n" or user_answer != "no":
        user_answer = input("Do you want to start now the dhcp server ?(y/n or yes/no)")
        if user_answer == "yes" or user_answer == "y":
            cmd = "/etc/init.d/isc-dhcp-server start"
            try:
                answer_cmd = os.system(cmd)
                if answer_cmd == 0:
                    print(termcolor.colored("done. ", "green"))
                else:
                    print(termcolor.colored("check failed.", "red"))
            except:
                print(termcolor.colored("check failed.", "red"))
        else:
            print("dhcp server not start")
        break


exec_cmd(cmd, comment)
print("writing of dhcpd.conf file ...")
check_config()
start()
