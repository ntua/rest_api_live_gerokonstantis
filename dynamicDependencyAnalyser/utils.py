import json

# checks if an object is nested so as to continue parsing
def is_nested_obj(obj):
    for attribute, value in obj.items():
        if type(value)==dict and attribute!='format':
            return True
    return False



# parse obj (i.e. request or response body) and store information about the 
# values of each attribute
# returns :
#   reqbody_values (resbody_values) : 
#       for each new value encountered in a request (response) body, 
#       we store the corresponding endpoint in the req (res) body of which that value was found 
# path_list stores the path of the attribute into the req (res) body
def parse_nested_obj(obj, flag, request_info, reqbody_values, resbody_values, path_list):
    for attribute, attribute_value in obj.items():
        if is_nested_obj(attribute_value):
            parse_nested_obj(attribute_value, flag, request_info, reqbody_values, resbody_values, path_list+[attribute])
        else:
            attribute_info={}
            attribute_info['name'] = attribute
            attribute_info['path'] = '->'.join(path_list+[attribute])
            path_list=[]
            attribute_info['type'] = attribute_value['name']
            if 'format' in attribute_value:
                attribute_info['format'] = attribute_value['format']
            if flag=='req':
                if attribute_value['value'] not in reqbody_values:
                    reqbody_values[attribute_value['value']]=[]
                reqbody_values[attribute_value['value']].append({'request_info': request_info, 'attribute_info': attribute_info})
            elif flag=='res':
                if attribute_value['value'] not in resbody_values:
                    resbody_values[attribute_value['value']]=[]
                resbody_values[attribute_value['value']].append({'request_info': request_info, 'attribute_info': attribute_info })
    return {'reqbody_values': reqbody_values, 'resbody_values': resbody_values}
    


# dependency_graph[<(endpoint E1, endpoint E2)>]=<set of tuples (fromKey, toKey, type) for which E1, E2 are dependent>  
# (i.e. the value of fromKey attribute of E1's response body gives its value to the value of toKey attribute of E2's request body)
# using sets ensures that each tuple (fromKey, toKey, type) is unique for a specific pair of endpoints
# IMPORTANT note : each response body is compared only to the request bodies of subsequent requests of the use case 
#                  only these dependencies make sense
def compute_dependency_graph(reqbody_values, resbody_values):
    dependency_graph={}
    for value in resbody_values:
        if type(value)!=bool and value in reqbody_values:
            for res in resbody_values[value]:
                res_info = res['request_info']
                res_attribute_info = res['attribute_info']
                res_endpoint = res_info['endpoint']
                res_method = res_info['method']
                full_res_endpoint = res_method+' '+res_endpoint
                res_seq_number = res_info['seq_number']
                for req in reqbody_values[value]:
                    req_info = req['request_info']
                    req_attribute_info = req['attribute_info']
                    req_endpoint = req_info['endpoint']
                    req_method = req_info['method']
                    full_req_endpoint = req_method+' '+req_endpoint
                    req_seq_number = req_info['seq_number']
                    if full_req_endpoint!=full_res_endpoint and req_seq_number>res_seq_number:
                        if (full_res_endpoint, full_req_endpoint) not in dependency_graph:
                            dependency_graph[(full_res_endpoint, full_req_endpoint)]=set()
                        dependency_graph[(full_res_endpoint, full_req_endpoint)].add((res_attribute_info['name'],req_attribute_info['name'],req_attribute_info['type']))
    return dependency_graph


# transformed_dependency_graph[<endpoint E1>]=<list of dictionaries each one of the contains the dependent endpoint E2 and a list of attributes related to this dependency>
# just a transformation of the dependency graph created above so as to produce the output json file
def transform_dependency_graph(dependency_graph):
    transformed_dependency_graph={}
    for endpoint_pair in dependency_graph:
        if endpoint_pair[0] not in transformed_dependency_graph:
            transformed_dependency_graph[endpoint_pair[0]]=[]
        dep_attributes=[]
        for tuple in dependency_graph[endpoint_pair]:
            dep_attributes.append({"fromKey": tuple[0], "toKey": tuple[1], "type": tuple[2]})
        transformed_dependency_graph[endpoint_pair[0]].append({'dependent_endpoint_name': endpoint_pair[1], 'attributes':dep_attributes})
    return transformed_dependency_graph


def produce_output(dependency_graph):
    dependency_graph=transform_dependency_graph(dependency_graph)

    output_dict={}
    metadata_dict={}
    endpoints = []

    edges = 0
    for endpoint in dependency_graph:
        edges = edges + len(dependency_graph[endpoint])
        endpoint_dict = {}
        endpoint_dict["name"]=endpoint
        endpoint_dict["method"]=endpoint.split(" ")[0]
        dependencies=[]
        for dep in dependency_graph[endpoint]:
            dep_dict={}
            dep_dict["name"]=dep['dependent_endpoint_name']
            dep_dict["method"]=dep['dependent_endpoint_name'].split(" ")[0]
            dep_dict["attributes"]=dep['attributes']
            dependencies.append(dep_dict)
        endpoint_dict["dependencies"]=dependencies
        endpoints.append(endpoint_dict)

    metadata_dict["nodes"]=len(dependency_graph)
    metadata_dict["edges"]=edges

    output_dict["info"]=metadata_dict
    output_dict["endpoints"]=endpoints

    output_file = open("./output_files/dependencies.json", "w")
    output_file.write(str(json.dumps(output_dict)))
    output_file.close()