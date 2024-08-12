import json
import numpy as np 
import matplotlib.pyplot as plt

configurations = ['withQueryNoGetMethodNoPathNoStrictTypes', 'withQueryNoGetMethodNoPathStrictTypes', 'withQueryNoGetMethodWithPathNoStrictTypes', 'withQueryNoGetMethodWithPathStrictTypes', 'withQueryOnlyGetNoPathNoStrictTypes', 'withQueryOnlyGetNoPathStrictTypes', 'withQueryOnlyGetWithPathNoStrictTypes', 'withQueryOnlyGetWithPathStrictTypes']

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


for config in configurations:
    dynamic_dependencies = eval(open('./dependencies/{}/dynamic.json'.format(config), 'r').read(), {'true':True, 'false':False})
    static_dependencies = eval(open('./dependencies/{}/static.json'.format(config), 'r').read(), {'true':True, 'false':False})

    dynamic_dependencies_info = dynamic_dependencies['info']
    static_dependencies_info = static_dependencies['info']

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
    output_file = open("./compare_results/compare_{}.json".format(config), "w")
    output_file.write(str(json.dumps(compare_per_endpoint)))
    output_file.close()
    # print(sorted(dynamic_dependencies_per_endpoint.keys()), '\n\n\n',sorted(static_dependencies_per_endpoint.keys()))

    # comparative plots
    bar_width = 0.5
    figure, ax = plt.subplots(figsize=(15, 8), tight_layout=True) 

    x_axis = []
    dynamic_statistics = []
    static_statistics = []
    for stat in dynamic_dependencies_info:
        if stat=='bodyDependencies' or stat=='dependenciesPerAttribute' or stat=='edges':
            x_axis.append(stat+' /10')
            dynamic_statistics.append(int(dynamic_dependencies_info[stat])/10)
            static_statistics.append(int(static_dependencies_info[stat])/10)
        else:
            x_axis.append(stat)
            dynamic_statistics.append(int(dynamic_dependencies_info[stat]))
            static_statistics.append(int(static_dependencies_info[stat]))

    # Set the positions of bars and make the plots
    bar1positions = 3 * np.arange(len(dynamic_statistics))
    ax.bar(bar1positions, dynamic_statistics, color='teal', width=bar_width, label='dynamic')
    ax.bar(bar1positions + bar_width, static_statistics, color='coral', width=bar_width, label='static')
    ax.bar(bar1positions + 2 * bar_width, abs(np.subtract(dynamic_statistics, static_statistics)), color='palevioletred', width=bar_width, label='difference')
    #plt.plot(bar1positions + 2 * bar_width,abs(np.subtract(dynamic_statistics, static_statistics)), '--o', color='gray')

    plt.xticks(rotation=60)
    ax.set_xticks(bar1positions + bar_width)
    ax.set_xticklabels(x_axis)

    plt.xlabel('Metric', fontweight='bold', fontsize=10)
    plt.ylabel('Value', fontweight='bold', fontsize=10)
    plt.title(config, fontsize=12)

    ax.set_facecolor('lavender')
    plt.legend()
    plt.savefig("./compare_results/compare_{}.png".format(config))