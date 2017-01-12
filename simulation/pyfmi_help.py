# Get state names and their values at given index
def get_state(fmu, results, index):
    # Identify states as variables with a _start_ value
    identifier = "_start_"
    keys = fmu.get_model_variables(filter=identifier + "*").keys()
    
    # Now, loop through all states, get their value and put it in x
    x = {}
    for name in keys:
         x[name] = results[name[len(identifier):]][index]
    
    # Return state
    return x

def create_result_obj(fmu):
    result_object = {key: [] for key in fmu.get_model_variables()}
    result_object['time'] = []
    return result_object

def append_to_result_obj(fmu, result_object, new_results):
    for key in fmu.get_model_variables():
        result_object[key].extend(new_results[key])
    result_object['time'].extend(new_results['time'])
    return result_object