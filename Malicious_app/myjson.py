import json
import torch
import numpy as np

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if torch.is_tensor(obj):
            #print("--------ENCODE SUCCESS----------")
            return {
                    'type':'__Tensor__',
                    'data': obj
            }
        else:
            print("-------ENCODE FAIL--------------")
            #obj_replace = obj
            #return obj_replace
            return json.JSONEncoder.default(self, obj)

def my_decoder(obj):
    if torch.tensor(obj):
        print("--------DECODE SUCCESS----------")
        return obj
    print("-------DECODE FAIL---------------")
    return obj

# Encoder function      
def my_dumps(data1):
    return json.dumps(data1, cls=MyEncoder)

# Decoder function
def my_loads(obj):
    return json.loads(obj, object_hook=my_decoder)
