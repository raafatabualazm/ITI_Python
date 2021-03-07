import re

def open_log(file):
    try:
        global logs
        logs = open(file, 'r')
    except:
        print("Error loading file.")

def extract_ips(text):
    try:
        ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)
        ips_unique = set(ips)
        return ips_unique
    except:
        print("Error in File Handler")

def extract_uris(text):
    try:
        uris = re.findall(r'((\/[A-Za-z0-9.-]+)+)|(\/\s)', text)
        if uris[1][0] == "":
            return "/"
        return uris[1][0]
    except:
        print("Error in Extracting unique URIs")

def extract_methods(text):
    try:
        unique_methods = set(re.findall(r'\"(\w+)\s+\/\S+',text))
        return unique_methods
    except:
        print("Error in extracting METHODS")

def extract_agents(text):
    try:
        unique_agents = set(re.findall(r'\"(\w+\/[\w\.]+)', text))
        unique_agents.add('Mozilla / 5.0')
        return unique_agents
    except:
        print("Error in extracting user agents")

def search_ip():
    cnt = 0
    ip = input('Enter IP to search for its logs: ')
    code = input('Enter Status Code for the response: ')
    uris = []
    try:
        for line in logs:
            if line.startswith('{}'.format(ip)):
                if re.search('\"\s+{}\s+\d+'.format(code), line):
                    uri = extract_uris(line)
                    uris.append(uri)
                    cnt += 1
        return uris, cnt
    except:
        print("Error extracting requests for the IP")

open_log("access.log.txt")

uri_lst, cnt = search_ip()
for uri in uri_lst:
    print(uri)
