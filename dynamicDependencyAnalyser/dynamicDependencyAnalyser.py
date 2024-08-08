import glob
from colorama import Fore, Style
from utils import is_nested_obj, parse_nested_obj, compute_and_analyse_dependency_graph, produce_output


# ask user to provide the name of the json input file
while True:
    user_input = input('Enter the name of the .json input file: ')
    if len(user_input.split("."))==1:
        print(Fore.RED+'add the file extension ')
        print(Style.RESET_ALL)
    elif not user_input.endswith('json'):
        print(Fore.RED+'wrong file format:', user_input.split(".")[-1], 'instead of json')
        print(Style.RESET_ALL)
    else:
        input_path_list = glob.glob("../mim logs/*/{}".format(user_input), recursive=True)
        if len(input_path_list)==0:
            print(Fore.RED+'file not found')
            print(Style.RESET_ALL)
        elif len(input_path_list)>1:
            print(Fore.RED+'this filename is not unique',input_path_list)
            print(Style.RESET_ALL)
        else:
            input_path = input_path_list[0]
            break

# ask user whether to check for dependencies related to query params 
while True:
    user_input = input('Include query parameters? (yes / no): ')
    if user_input == "yes" or user_input == "y" or user_input == "":
        includeQueryParams = True
        break
    elif user_input == "no" or user_input == "n":
        includeQueryParams = False
        break

# ask user whether to check only for dependencies starting from GET requests
# (these dependencies are likely to make more sense) 
while True:
    user_input = input('Check only dependencies starting from endpoints with method "GET"? (yes / no): ')
    if user_input == "yes" or user_input == "y" or user_input == "":
        get_method = True
        break
    elif user_input == "no" or user_input == "n":
        get_method = False
        break

# ask user whether to take boolean values into consideration
# this can lead to misleading results
while True:
    user_input = input('Take boolean values into consideration? [this may produce misleading results] (yes / no) ')
    if user_input == "yes" or user_input == "y" or user_input == "":
        include_boolean = True
        break
    elif user_input == "no" or user_input == "n":
        include_boolean = False
        break


# read list of requests stored by mim (i.e. json file exported from MongoDB)
input_list = eval(open(input_path, 'r').read(), {'true':True, 'false':False})

# reqs_per_usecase['<use case number>']=<list of requests for this use case>
# (it only makes sense to look for dependencies within each one of the use cases and then combine the results)
reqs_per_usecase={}
for req in input_list:
    if req['tag'] not in reqs_per_usecase:
        reqs_per_usecase[req['tag']]=[]
    reqs_per_usecase[req['tag']].append(req)


# store information about every attribute value encountered in a request or response : endpoint, method, attribute name, ...
#   req_values (res_values) : 
#       dict with key=<attribute value> and value=<list of endpoints (+ metadata) into the req (res) body (or params) of which this value was found>
req_values={}
res_values={} 
for usecase in reqs_per_usecase:
    for i in range(0, len(reqs_per_usecase[usecase])):
        request = reqs_per_usecase[usecase][i]
        if 'body' in request:
            req_body = request['body']
            if is_nested_obj(req_body):
                req_values=parse_nested_obj(req_body,'req',{'endpoint':request['endpoint'], 'method': request['method'], 'seq_number': i},req_values,res_values,[])['reqbody_values']
        if 'response' in request:
            res_body = request['response']
            res_body_schema = res_body['requestSchema']
            if is_nested_obj(res_body_schema):
                res_values=parse_nested_obj(res_body_schema,'res',{'endpoint':request['endpoint'], 'method': request['method'], 'seq_number': i},req_values,res_values,[])['resbody_values']
        # we can also store information about query params values
        if 'query' in request and includeQueryParams:
            queryParams = request['query']
            for queryParam in queryParams:
                attribute_info={}
                attribute_info['name'] = queryParam
                attribute_info['path'] = queryParam
                attribute_info['type_of_param'] = "query"
                attribute_info['type'] = "string"
                if queryParams[queryParam] not in req_values:
                    req_values[queryParams[queryParam]]=[]
                req_values[queryParams[queryParam]].append({'request_info': {'endpoint':request['endpoint'], 'method': request['method'], 'seq_number': i}, 'attribute_info': attribute_info })

# compute dependency graph and produce the output .json file
produce_output(compute_and_analyse_dependency_graph(req_values,res_values,get_method,include_boolean))

