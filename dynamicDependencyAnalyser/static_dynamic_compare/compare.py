import json

# compare a dynamic and a static url
# (!) : in dynamic urls, path params have real values, in static urls we see only the name of the path param 
def same_urls(dynamic_url, static_url):
    if(dynamic_url.split(" ")[0]!=static_url.split(" ")[0]):
        return False
    du = dynamic_url.split(" ")[1].split("/")
    su = static_url.split(" ")[1].split("/")
    if(len(du)!=len(su)):
        return False
    for i in range(len(du)):
        if du[i]!=su[i] and su[i][0]!=":":
            return False
    return True

# check if an endpoint is a key of dict (using the comparison method above)
def search_for_same_endpoint(dict, endpoint):
    for key in dict:
        if same_urls(endpoint, key):
            return key
    return False



dynamic_dependencies = eval(open('./dependencies/withQueryNoGetMethod/dynamic.json', 'r').read(), {'true':True, 'false':False})
static_dependencies = eval(open('./dependencies/withQueryNoGetMethod/static.json', 'r').read(), {'true':True, 'false':False})

dynamic_dependencies_endpoints = dynamic_dependencies['endpoints']
static_dependencies_endpoints = static_dependencies['endpoints']

# for each endpoint, make the set of its dynamic or static dependencies
dynamic_dependencies_per_endpoint = {}
for item in dynamic_dependencies_endpoints:
    if item['name'] not in dynamic_dependencies_per_endpoint:
        dynamic_dependencies_per_endpoint[item['name']]=set()
    for dependency in item['dependencies']:
        dynamic_dependencies_per_endpoint[item['name']].add(dependency['name'])

static_dependencies_per_endpoint = {}
for item in static_dependencies_endpoints:
    if item['url'] not in static_dependencies_per_endpoint:
        static_dependencies_per_endpoint[item['url']]=set()
    for dependency in item['dependencies']:
        static_dependencies_per_endpoint[item['url']].add(dependency['url'])

# compare the common endpoints (i.e. those having both dynamic and static dependencies)
compare_per_endpoint = {}
for endpoint in dynamic_dependencies_per_endpoint:
    static_endpoint = search_for_same_endpoint(static_dependencies_per_endpoint, endpoint)
    if static_endpoint:
        dynamic_dependencies_set=dynamic_dependencies_per_endpoint[endpoint]
        static_dependencies_set=static_dependencies_per_endpoint[static_endpoint]
        compare_per_endpoint[endpoint]={'static_endpoint': static_endpoint,'numberOfDynamicDeps': len(dynamic_dependencies_set), 'numberOfStaticDeps': len(static_dependencies_set), 'intersectionOfDepsLength': len(dynamic_dependencies_set.intersection(static_dependencies_set)), 'dynamicAndNotStatic': len(dynamic_dependencies_set-static_dependencies_set), 'staticAndNotDynamic': len(static_dependencies_set-dynamic_dependencies_set)}

# print(compare_per_endpoint)
output_file = open("./compare_results/compare_no_get.json", "w")
output_file.write(str(json.dumps(compare_per_endpoint)))
output_file.close()
# print(sorted(dynamic_dependencies_per_endpoint.keys()), '\n\n\n',sorted(static_dependencies_per_endpoint.keys()))