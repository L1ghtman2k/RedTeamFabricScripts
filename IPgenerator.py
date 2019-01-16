import argparse


def host(user, skip_user, net, number_of_teams, first_team_start_address, lan, dmz, lan_list, dmz_list, wan_ip, gateway_user, *args, **kwargs):
    hosts_list = []
    la = [lan, lan_list]
    dm = [dmz, dmz_list]
    for team_number in range(first_team_start_address, first_team_start_address+number_of_teams):
        for zone in [la, dm]:
            if zone[1]:
                single = f"{user}@"
                if skip_user:
                    single=""
                for fourth_octet in zone[1].split(','):
                    hosts_list.append(single+f"{net}.{team_number}.{zone[0]}."+fourth_octet)
        if wan_ip:
            hosts_list.append(gateway_user + "@" + wan_ip.replace("X", str(team_number)))
    return hosts_list


def output(hosts_list, file_name):
    with open(file_name, "w") as file:
        file.write("\n".join(hosts_list))


class Formatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


parser = argparse.ArgumentParser(description="Please follow the format:\n"
                                             "user@(net).(X: number of teams).(dmz/lan).(ip of the machine) \n"
                                             "example: IPgenerator.py --user sysadmin --net 10 --number_"
                                             "of_teams 15 --first_team_start_address 1 --lan 1 --dmz 2 --lan_list 5,6,"
                                             "7 --dmz_list 10,11,12 --wan_ip 178.X.3.56 --output IPs.txt",
                                             formatter_class=Formatter)
parser.add_argument("--user", help="the user to which you will ssh", default="sysadmin")
parser.add_argument("--skip_user", help="Specify If you would like username to be attached to IP address", default=False, type=bool)
parser.add_argument("--net", help="the first octet for any machine in your network" , default="10")
parser.add_argument("--number_of_teams", help="The total number of teams in the competition", default="15", type=int)
parser.add_argument("--first_team_start_address", help="The second octet of the first team", default="1", type=int)
parser.add_argument("--lan", help="the third octet for any machine in lan", default="1")
parser.add_argument("--dmz", help="the third octet for any machine in dmz", default="2")
parser.add_argument("--lan_list", help="List Of Fourth Octets in lan(comma separated)", default=None)
parser.add_argument("--dmz_list", help="List Of Fourth Octets in dmz(comma separated)", default=None)
parser.add_argument("--wan_ip", help="WAN Address with X as one of the Octets(X stand for team number)", default=None)
parser.add_argument("--gateway_user", help="User of the gateway", default="root")
parser.add_argument("--output", help="Output file to which IPs should be saved", default="output.txt")

args = parser.parse_args()
output(host(**vars(args)), args.output)





