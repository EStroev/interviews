from scapy.all import *
import subprocess

pcap_reader = PcapReader(r'/Users/Jenya/Downloads/key.pcap')
raw_data_list = list()
for packet_iter in pcap_reader:
    pkt_raw = packet_iter.getlayer(Raw)
    if pkt_raw:
        raw_data_list.append(pkt_raw.load)

raw_data = ''.join(raw_data_list)

raw_data_part_1 = 'Password>:TnZGFjo+k4/vaiYaQcTD8sr8vPSh'
raw_data_part_2 = 'THAWEzhslIntbnBOIpaq'
raw_data_part_3 = 'FNG8Hf4vzfxRlsrB/Ek/wpWX0xDdECEiKrAKqER/LTAJ3sJ7aco=:<Encrypted_flag'

password = raw_data_part_1.split('Password>:')[1]
flag = raw_data_part_3.split(':<Encrypted_flag')[0]

command = "echo '%s' | openssl enc -d -base64 -aes-128-ctr -nopad -nosalt -k '%s'" % (flag, password)

process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, error = process.communicate()

print(output)