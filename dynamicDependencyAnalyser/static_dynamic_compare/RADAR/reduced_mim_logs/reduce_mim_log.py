import glob
import json
from colorama import Fore, Style


# ask user to provide the name of the initial mim log 
while True:
    user_input = input('Enter the name of the .json input file (mim log): ')
    if len(user_input.split("."))==1:
        print(Fore.RED+'add the file extension ')
        print(Style.RESET_ALL)
    elif not user_input.endswith('json'):
        print(Fore.RED+'wrong file format:', user_input.split(".")[-1], 'instead of json')
        print(Style.RESET_ALL)
    else:
        input_path_list = glob.glob("../../../../mim logs/*/{}".format(user_input), recursive=True)
        if len(input_path_list)==0:
            print(Fore.RED+'file not found')
            print(Style.RESET_ALL)
        elif len(input_path_list)>1:
            print(Fore.RED+'this filename is not unique',input_path_list)
            print(Style.RESET_ALL)
        else:
            input_path = input_path_list[0]
            break

# read list of requests stored by mim (i.e. json file exported from MongoDB)
input_list = eval(open(input_path, 'r').read().replace('"true"', '"True"'), {'true':True, 'false':False})

requests_per_usecase = {}
for request in input_list:
    if request['tag'] not in requests_per_usecase:
        requests_per_usecase[request['tag']]=[]
    requests_per_usecase[request['tag']].append(request)

for tag in requests_per_usecase:
    output_file = open("./mim.requests{}.json".format(tag), "w")
    output_file.write(str(json.dumps(requests_per_usecase[tag])))
    output_file.close()