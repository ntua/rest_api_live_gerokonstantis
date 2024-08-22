import subprocess
import json
import glob
from colorama import Fore, Style

# ask user to provide the path of the dependencies json file
while True:
    user_input = input('Enter the path of the dependencies json file: ')
    name = user_input.split('/')[-1]
    if len(name.split("."))==1:
        print(Fore.RED+'add the file extension ')
        print(Style.RESET_ALL)
    elif not name.endswith('json'):
        print(Fore.RED+'wrong file format:', name.split(".")[-1], 'instead of json')
        print(Style.RESET_ALL)
    else:
        input_path_list = glob.glob(user_input, recursive=True)
        if len(input_path_list)==0:
            print(Fore.RED+'file not found')
            print(Style.RESET_ALL)
        else:
            input_path = input_path_list[0]
            break

jwt = input('Enter your token: ')

dependencies = eval(open(input_path, 'r').read(), {'true':True, 'false':False, 'null': {}})
filename=input('Enter the name of the graph: ')+'.json'

# Define the URL and headers
url = 'https://radar.softlab.ntua.gr/api/graphs'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': '_ga=GA1.2.496286972.1722854675; _ga_BQ6WS9N7TV=GS1.2.1722854675.1.1.1722854794.0.0.0; g_state={"i_l":0}; user='+jwt,
    'Origin': 'https://radar.softlab.ntua.gr',
    'Referer': 'https://radar.softlab.ntua.gr/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Opera";v="112"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'If-None-Match': 'W/"163b3-bocp1t5fu3PLPv1X/5kI7PSZljE"'
}

# add dummy swaggerId and filename
body = {"info": dependencies['info'],"endpoints": dependencies['endpoints'],"swaggerId":"82a42501-7abd-4e57-889e-815d10e31ea9","name":filename}
output_file = open("./graph.json", "w")
output_file.write(str(json.dumps(body)))
output_file.close()

# Construct the curl command
curl_command = [
    'curl', url,
    '-H', f'Accept: {headers["Accept"]}',
    '-H', f'Accept-Language: {headers["Accept-Language"]}',
    '-H', f'Connection: {headers["Connection"]}',
    '-H', f'Content-Type: {headers["Content-Type"]}',
    '-H', f'Cookie: {headers["Cookie"]}',
    '-H', f'Origin: {headers["Origin"]}',
    '-H', f'Referer: {headers["Referer"]}',
    '-H', f'Sec-Fetch-Dest: {headers["Sec-Fetch-Dest"]}',
    '-H', f'Sec-Fetch-Mode: {headers["Sec-Fetch-Mode"]}',
    '-H', f'Sec-Fetch-Site: {headers["Sec-Fetch-Site"]}',
    '-H', f'User-Agent: {headers["User-Agent"]}',
    '-H', f'sec-ch-ua: {headers["sec-ch-ua"]}',
    '-H', f'sec-ch-ua-mobile: {headers["sec-ch-ua-mobile"]}',
    '-H', f'sec-ch-ua-platform: {headers["sec-ch-ua-platform"]}',
    '-H', f'If-None-Match: {headers["If-None-Match"]}',
    '--data-binary', '@graph.json'
]

# Run the command
try:
    result = subprocess.run(curl_command, capture_output=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed with exit code {e.returncode}")
    print(e.stderr)
