from utils import is_nested_obj, parse_nested_obj, compute_dependency_graph, produce_output

input_path = '../mim logs/paypal api/'

# read list of requests stored by mim
input_list = eval(open(input_path + 'mim.requests.json', 'r').read(), {'true':True, 'false':False})

# reqs_per_usecase['<use case number>']=<list of requests for this use case>
reqs_per_usecase={}
for req in input_list:
    if req['tag'] not in reqs_per_usecase:
        reqs_per_usecase[req['tag']]=[]
    reqs_per_usecase[req['tag']].append(req)


#   reqbody_values (resbody_values) : 
#       dict with key=<attribute value> and value=<list of endpoints (+ metadata) into the req (res) body of which this value was found>
reqbody_values={}
resbody_values={}
for usecase in reqs_per_usecase:
    for i in range(0, len(reqs_per_usecase[usecase])):
        request = reqs_per_usecase[usecase][i]
        if 'body' in request:
            req_body = request['body']
            if is_nested_obj(req_body):
                reqbody_values=parse_nested_obj(req_body,'req',{'endpoint':request['endpoint'], 'method': request['method'], 'seq_number': i},reqbody_values,resbody_values,[])['reqbody_values']
        if 'response' in request:
            res_body = request['response']
            res_body_schema = res_body['requestSchema']
            if is_nested_obj(res_body_schema):
                resbody_values=parse_nested_obj(res_body_schema,'res',{'endpoint':request['endpoint'], 'method': request['method'], 'seq_number': i},reqbody_values,resbody_values,[])['resbody_values']

produce_output(compute_dependency_graph(reqbody_values,resbody_values))

