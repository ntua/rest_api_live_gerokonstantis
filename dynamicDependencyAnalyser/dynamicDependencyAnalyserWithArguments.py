import glob
from colorama import Fore, Style
from utils import is_nested_obj, parse_nested_obj, compute_and_analyse_dependency_graph, produce_output
import sys

input_path=glob.glob("../mim logs/*/{}".format(sys.argv[1]), recursive=True)[0] or glob.glob("./static_dynamic_compare/RADAR/reduced_mim_logs/{}".format(sys.argv[1]), recursive=True)[0]

includeQueryParams=False
include_path=False
get_method=False
include_boolean=False
strict_types=False

if(sys.argv[2] == 'True'):
    includeQueryParams = True

if(sys.argv[3] == 'True'):
    include_path = True

if(sys.argv[4] == 'True'):
    get_method = True

if(sys.argv[5] == 'True'):
    include_boolean = True

if(sys.argv[6] == 'True'):
    strict_types = True


# read list of requests stored by mim (i.e. json file exported from MongoDB)
input_list = eval(open(input_path, 'r').read().replace('"true"', '"True"'), {'true':True, 'false':False})

# add increasing sequence numbers to the requests of each use case
# so that we look for dependencies between req1 and req2, where req2 follows req1 in the use case
reqs_per_usecase={}
tag = None
seq_number = None
for req in input_list:
    if req['tag']!=tag:
        seq_number = 0
        tag=req['tag']
    req['seq_number'] = seq_number
    seq_number+=1

# store information about every attribute value encountered in a request or response : endpoint, method, attribute name, ...
#   req_values (res_values) : 
#       dict with key=<attribute value> and value=<list of endpoints (+ metadata) into the req (res) body (or params) of which this value was found>
req_values={}
res_values={} 
for request in input_list:
    if 'body' in request:
        req_body = request['body']
        if is_nested_obj(req_body):
            req_values=parse_nested_obj(req_body,'req',{'endpoint':request['endpoint'], 'method': request['method'], 'seq_number': request['seq_number'], 'usecase': request['tag']},req_values,res_values,[])['reqbody_values']
    if 'response' in request:
        res_body = request['response']
        res_body_schema = res_body['requestSchema']
        if is_nested_obj(res_body_schema):
            res_values=parse_nested_obj(res_body_schema,'res',{'endpoint':request['endpoint'], 'method': request['method'], 'seq_number': request['seq_number'], 'usecase': request['tag']},req_values,res_values,[])['resbody_values']
    # we can also store information about query params values
    if 'query' in request and includeQueryParams:
        queryParams = request['query']
        for queryParam in queryParams:
            attribute_info={}
            attribute_info['name'] = queryParam
            attribute_info['path'] = 'url->'+queryParam
            attribute_info['type_of_param'] = "query"
            attribute_info['type'] = "string"
            if queryParams[queryParam] not in req_values:
                req_values[queryParams[queryParam]]=[]
            req_values[queryParams[queryParam]].append({'request_info': {'endpoint':request['endpoint'], 'method': request['method'], 'seq_number': request['seq_number'], 'usecase': request['tag']}, 'attribute_info': attribute_info })
    if include_path:
        path = request['params']
        for param in path:
            attribute_info={}
            attribute_info['name'] = param
            attribute_info['path'] = 'url->'+param
            attribute_info['type_of_param'] = "path"
            attribute_info['type'] = "string"
            if param not in req_values:
                req_values[param]=[]
            req_values[param].append({'request_info': {'endpoint':request['endpoint'], 'method': request['method'], 'seq_number': request['seq_number'], 'usecase': request['tag']}, 'attribute_info': attribute_info })


# compute dependency graph and produce the output .json file
produce_output(compute_and_analyse_dependency_graph(req_values,res_values,get_method,include_boolean, strict_types))

