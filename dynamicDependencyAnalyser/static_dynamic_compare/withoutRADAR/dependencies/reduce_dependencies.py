# keep the dependencies of some desired endpoints

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

desired_endpoints = input('Provide the desired endpoints (separated by &): ').split("&")

dependencies = eval(open(input_path, 'r').read(), {'true':True, 'false':False, 'null': {}})

result = {}
result['info']=dependencies['info']
result['endpoints']=[]
for endpoint in dependencies['endpoints']:
    if 'url' in endpoint and endpoint['url'] in desired_endpoints:
        result['endpoints'].append(endpoint)
    if endpoint['name'] in desired_endpoints:
        result['endpoints'].append(endpoint)

output_file = open("./filtered_dependencies.json", "w")
output_file.write(str(json.dumps(result)))
output_file.close()