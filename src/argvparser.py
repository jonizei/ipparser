
PARAM_TOKEN = '-'

parameters = {
    'INPUT' : {
        'token' : '-I',
        'pair' : True
    },
    'OUTPUT' : {
        'token' : '-O',
        'pair' : True
    },
    'MIN' : {
        'token' : '-min',
        'pair' : True
        , 'weight' : 2
    },
    'NET' : {
        'token' : '-net',
        'pair' : False
        , 'weight' : 1
    },
    'MULTI_PROCESS' : {
        'token' : '-mp',
        'pair' : False
    },
    'COUNT' : {
        'token' : '-count',
        'pair' : False
    }
}

# Finds all parameters from input
def find_parameters(argv):
    params = []
    arg_count = len(argv);
    for i in range(0, arg_count):
        if is_param(argv[i]):

            param_value = ''
            next_idx = i + 1

            if next_idx < arg_count:
                if not is_param(argv[next_idx]):
                    param_value = argv[next_idx]

            params.append({
                'index' : i,
                'token' : argv[i],
                'value' : param_value
            })

    return params

# Creates dictionary of parameters
def parse(argv):
    parsed_params = {}
    found_params = find_parameters(argv)

    for param in found_params:
        key = get_param_key(param['token'])

        if not key == None:
            parsed_params[key] = param['value']

    return parsed_params

def get_param_key(token):

    param_key = None

    for key in parameters.keys():
        if parameters[key]['token'] == token:
            param_key = key
            break

    return param_key

def required_params_exists(params):
    if 'INPUT' in params and 'OUTPUT' in params:
        return True
    
    return False

def is_param(txt):
    if len(txt) > 1:
        if txt[0] == PARAM_TOKEN:
            return True
        
    return False