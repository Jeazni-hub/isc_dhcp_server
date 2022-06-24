#!/usr/bin/python3
import os
import threading
import termcolor
import ip_calculate

interface = ""
ip_add = ""
subnet_mask = ""
broadcast = ""
sub_net = ""
rang_min = ""
rang_max = ""
ip_rang = ""
line = []


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
        if "ifconfig" in cmd:
            input("connect the host to the router (press enter keyboard to continuous...)")
        print(comment[ind])
        thr = threading.Thread(target=execute(cmd, comment[ind]))
        thr.start()
        thr.join()


def dhcpd_conf():
    global line
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
            print(termcolor.colored("DHCP server starting failed.", "red"))
            print("Please use external DHCP server.")
        break


def initialisation():
    global interface, ip_add, subnet_mask, broadcast, sub_net, rang_min, rang_max, ip_rang
    interface = input("listening interface (eth0 for None):\n ")
    if interface == "":
        interface = "eth0"
    ip_addr = input(" (network address /30 (192.168.100.1/30 for default):\n ")
    if ip_addr == "":
        ip_addr = "192.168.100.0/30"
    subnet_mask = ip_calculate.ip_calculator(ip_addr)[8]
    broadcast = ip_calculate.ip_calculator(ip_addr)[1]
    sub_net = ip_calculate.ip_calculator(ip_addr)[2]
    rang_min = ip_calculate.ip_calculator(ip_addr)[3]
    rang_max = ip_calculate.ip_calculator(ip_addr)[4]
    ip_add = ip_calculate.ip_calculator(ip_addr)[0]
    ip_rang = ip_calculate.ip_calculator(ip_addr)[6]


initialisation()
cmd = ["apt-get install isc-dhcp-server",
       f"echo 'INTERFACES=\"{interface}\"' >> /etc/default/isc-dhcp-server",
       "conf_file",
       f"ifconfig {interface} {ip_add} netmask {subnet_mask}"]

line = ["#",
        "# Sample configuration file for ISC dhcpd for Debian",
        "#",
        # f" server-name \"{sever_name}\";",
        f" option subnet-mask {subnet_mask};",
        # f" option domain-name-servers {ip_dns_server};",
        # f" option domain-name \"{domain_name}\";",
        # f" option routers {add_router};",
        f" option broadcast-address {broadcast};",
        " default-lease-time 7200;",
        " max-lease-time 7200;",
        f" subnet {sub_net} netmask {subnet_mask}" + " {",
        f"	range {rang_min} {rang_max};",
        "}"]

comment = ["Downloading of isc-dhcp-server ...",
           "Setting of listening interface ...",
           "configuration of dhcpd.conf file ...",
           "ip address setting"]


def start_install():
    global cmd, comment
    exec_cmd(cmd, comment)
    print("writing of dhcpd.conf file ...")
    check_config()
    start()