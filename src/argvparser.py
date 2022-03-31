
parameters = {
    '-I' : {
        'pair' : True
    },
    '-O' : {
        'pair' : True
    },
    '-all' : {
        'pair' : False
    },
    '-min' : {
        'pair' : True
    },
    '-net' : {
        'pair' : False
    },
    '-mp' : {
        'pair' : False
    }
}

# Finds all parameters from input
def find_parameters(argv):
    params = []
    for i in range(0, len(argv)):
        if argv[i][0] == '-':
            params.append((i, argv[i]))

    return params

# Creates dictionary of parameters
def parse(argv):
    parsed_params = {}
    found_params = find_parameters(argv)

    for p in found_params:
        if p[1] in parameters.keys():
            if parameters[p[1]]['pair']:
                if p[0] + 1 < len(argv):
                    value = argv[p[0] + 1]
                    if value[0] != '-':
                        parsed_params[p[1]] = value
            else:
                parsed_params[p[1]] = ''

    return parsed_params

