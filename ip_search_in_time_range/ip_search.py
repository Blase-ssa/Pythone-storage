#!/usr/bin/python3
import sys
import re

StarTime = re.compile('18:\d\d:\d\d')
ip_pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
ip_list = []
max_ip_count=0
max_ip_place=0

if len(sys.argv) < 2:
    sys.exit("file not specified")
else:
    #print (sys.argv[1])
    with open(sys.argv[1]) as infile:
        for line in infile:
            if StarTime.search(line) :
                t_ip=ip_pattern.search(line)
                if not bool(ip_list):
                    ip_list.append([t_ip.group(), 1])
                else:
                    flag_match=False
                    for i in range(0, len(ip_list)):
                        if t_ip.group() == ip_list[i][0]:
                            ip_list[i][1] = ip_list[i][1]+1
                            flag_match=True
                            break
                    if not flag_match:
                        ip_list.append([t_ip.group(), 1])

for i in range(0, len(ip_list)):
    if max_ip_count < ip_list[i][1]:
        max_ip_place=i
        max_ip_count=ip_list[i][1]
    
print ("IP: ", ip_list[max_ip_place][0], " occurs ", ip_list[max_ip_place][1], "times.")
