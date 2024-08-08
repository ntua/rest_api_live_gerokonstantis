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
            attribute_info['type_of_param'] = "body"
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
    path_list=[]
    return {'reqbody_values': reqbody_values, 'resbody_values': resbody_values}
    


# dependency_graph[<(endpoint E1, endpoint E2)>]=<set of tuples (fromKey, toKey, type) for which E1, E2 are dependent>  
# (i.e. the value of fromKey attribute of E1's response body gives its value to the value of toKey attribute of E2's request body)
# using sets ensures that each tuple (fromKey, toKey, type) is unique for a specific pair of endpoints
# IMPORTANT note : each response body is compared only to the request bodies of subsequent requests of the use case 
#                  only these dependencies make sense
def compute_and_analyse_dependency_graph(reqbody_values, resbody_values, get_method_flag, include_boolean_flag):
    dependency_graph={}
    full_set_of_endpoints=set() # all endpoints (even if they do not participate in a dependency)
    dependency_endpoints = set() # endpoints participating in a dependency
    dependent_nodes = set() # endpoints which are dependent to some others
    derive_nodes = set() # nodes having dependencies (i.e. some other endpoints are dependent to these nodes)
    body_dependencies = 0
    query_dependencies = 0 
    total_attribute_dependencies = 0
    for value in resbody_values:
        flag = False
        if(not include_boolean_flag):
            flag = type(value)==bool
        if not flag and value in reqbody_values:
            for res in resbody_values[value]:
                res_info = res['request_info']
                res_attribute_info = res['attribute_info']
                res_endpoint = res_info['endpoint']
                res_method = res_info['method']
                res_usecase = res_info['usecase']
                full_res_endpoint = res_method+' '+res_endpoint
                res_seq_number = res_info['seq_number']
                # full_set_of_endpoints.add(full_res_endpoint)
                for req in reqbody_values[value]:
                    req_info = req['request_info']
                    req_attribute_info = req['attribute_info']
                    req_endpoint = req_info['endpoint']
                    req_method = req_info['method']
                    req_usecase = req_info['usecase']
                    full_req_endpoint = req_method+' '+req_endpoint
                    req_seq_number = req_info['seq_number']
                    # full_set_of_endpoints.add(full_req_endpoint)
                    sameFormat=True
                    format="{}"
                    if 'format' in res_attribute_info and 'format' in req_attribute_info:
                        sameFormat=res_attribute_info['format']==req_attribute_info['format']
                        format=res_attribute_info['format']
                    if full_req_endpoint!=full_res_endpoint and req_seq_number>res_seq_number and req_usecase==res_usecase and sameFormat and res_attribute_info['type']==req_attribute_info['type']:
                        if get_method_flag==False or res_method=="GET":
                            if (full_res_endpoint, full_req_endpoint) not in dependency_graph:
                                dependency_graph[(full_res_endpoint, full_req_endpoint)]=set()
                            dependency_graph[(full_res_endpoint, full_req_endpoint)].add((res_attribute_info['name'],req_attribute_info['name'],res_attribute_info['path'],req_attribute_info['path'], value, req_attribute_info['type'],res_attribute_info['type_of_param'],req_attribute_info['type_of_param'], str(format), req_usecase, res_seq_number, req_seq_number))
                            if(res_attribute_info['type_of_param']=='body' and req_attribute_info['type_of_param']=='body'):
                                body_dependencies+=1
                            elif(res_attribute_info['type_of_param']=='query' or req_attribute_info['type_of_param']=='query'):
                                query_dependencies+=1
                            dependency_endpoints.add(full_res_endpoint)
                            dependency_endpoints.add(full_req_endpoint)
                            dependent_nodes.add(full_req_endpoint)
                            derive_nodes.add(full_res_endpoint)
                            total_attribute_dependencies+=1
    for value in resbody_values:
        for res in resbody_values[value]:
            res_info = res['request_info']
            full_set_of_endpoints.add(res_info['method']+' '+res_info['endpoint'])
    for value in reqbody_values:
        for req in reqbody_values[value]:
            req_info = req['request_info']
            full_set_of_endpoints.add(req_info['method']+' '+req_info['endpoint'])
    return {'dependency_graph': dependency_graph, 'extra_info': {'full_set_of_endpoints': full_set_of_endpoints, 'dependency_endpoints':dependency_endpoints, 'dependent_nodes': dependent_nodes, 'derive_nodes': derive_nodes, 'total_attribute_dependencies':total_attribute_dependencies, 'body_dependencies': body_dependencies, 'query_dependencies': query_dependencies, 'edges': len(dependency_graph), 'get_method_flag':get_method_flag }}


# transformed_dependency_graph[<endpoint E1>]=<list of dictionaries each one of the contains the dependent endpoint E2 and a list of attributes related to this dependency>
# just a transformation of the dependency graph created above so as to produce the output json file
def transform_dependency_graph(dependency_graph):
    transformed_dependency_graph={}
    for endpoint_pair in dependency_graph:
        if endpoint_pair[0] not in transformed_dependency_graph:
            transformed_dependency_graph[endpoint_pair[0]]=[]
        dep_attributes=[]
        for tuple in dependency_graph[endpoint_pair]:
            dep_attributes.append({"fromKey": tuple[0], "toKey": tuple[1], "fromPath": tuple[2], "toPath": tuple[3], "value": tuple[4], "type": tuple[5], "fromParamType": tuple[6], "toParamType": tuple[7], "format": eval(tuple[8]), "use_case": tuple[9], "fromSeqNumber": tuple[10], "toSeqNumber": tuple[11]})
        transformed_dependency_graph[endpoint_pair[0]].append({'dependent_endpoint_name': endpoint_pair[1], 'attributes':dep_attributes})
    return transformed_dependency_graph


# input = {'dependency_graph': dependency_graph, 'extra_info': {'full_set_of_endpoints': full_set_of_endpoints, 'dependency_endpoints':dependency_endpoints, 'dependent_nodes': dependent_nodes, 'derive_nodes': derive_nodes, 'total_attribute_dependencies':total_attribute_dependencies }}
def produce_output(input):
    dependency_graph = transform_dependency_graph(input['dependency_graph'])
    extra_info = input['extra_info']
    set_of_endpoints_without_dependencies = extra_info['full_set_of_endpoints'] - extra_info['derive_nodes']
    output_dict={}
    metadata_dict={}
    endpoints = []
    for endpoint in dependency_graph:
        endpoint_dict = {}
        endpoint_dict["name"]=endpoint
        endpoint_dict["method"]=endpoint.split(" ")[0]
        endpoint_dict["description"]="not available"
        dependencies=[]
        for dep in dependency_graph[endpoint]:
            dep_dict={}
            dep_dict["name"]=dep['dependent_endpoint_name']
            dep_dict["method"]=dep['dependent_endpoint_name'].split(" ")[0]
            dep_dict["description"]="not available"
            dep_dict["attributes"]=dep['attributes']
            dependencies.append(dep_dict)
        endpoint_dict["dependencies"]=dependencies
        endpoints.append(endpoint_dict)
    for endpoint in set_of_endpoints_without_dependencies:
        if not extra_info['get_method_flag'] or (extra_info['get_method_flag'] and endpoint.split(" ")[0]=="GET"):
            endpoints.append({"name": endpoint, "method": endpoint.split(" ")[0], "dependencies":[]})
    metadata_dict["nodes"]=str(len(extra_info['full_set_of_endpoints']) )# all endpoints (even if they do not participate in a dependency)
    metadata_dict["interdependencyNodes"]=str(len(extra_info['dependency_endpoints'])) # endpoints participating in a dependency
    metadata_dict["dependentOnlyNodes"]=str(len(extra_info['dependent_nodes']-extra_info['derive_nodes']))# endpoints which are dependent to others, but there is no endpoint dependent to them
    metadata_dict["derivingOnlyNodes"]=str(len(extra_info['derive_nodes']-extra_info['dependent_nodes'])) # endpoints on which other endpoints depend but which do not depend on any
    metadata_dict["bothDependentDerivingNodes"]=str(len(extra_info['derive_nodes'].intersection(extra_info['dependent_nodes'])))
    metadata_dict["edges"]=str(extra_info['edges']) # total dependencies between endpoints
    metadata_dict["dependenciesPerAttribute"]=str(extra_info['total_attribute_dependencies'])
    metadata_dict["bodyDependencies"]=str(extra_info['body_dependencies'])
    metadata_dict["queryDependencies"]=str(extra_info['query_dependencies'])
    metadata_dict["pathDependencies"]="0"
    output_dict["info"]=metadata_dict
    output_dict["endpoints"]=endpoints
    output_file = open("./output_files/dependencies.json", "w")
    output_file.write(str(json.dumps(output_dict)))
    output_file.close()