import json
import torch
import numpy as np

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if torch.is_tensor(obj):
            print("--------ENCODE SUCCESS----------")
            return {
                    '__type__':'__Tensor__',
                    'data': obj.tolist()
            }
        else:
            print("-------ENCODE FAIL--------------")
            return json.JSONEncoder.default(self, obj)

def my_decoder(obj):
    if '__type__' in obj:
        if obj['__type__'] == '__Tensor__': 
            print("--------DECODE SUCCESS----------")
            return torch.FloatTensor(obj['data'])
    print("-------DECODE FAIL---------------")
    return obj #If is null, return as well

# Encoder function      
def my_dumps(data1):
    return json.dumps(data1, cls=MyEncoder)

# Decoder function
def my_loads(obj):
    return json.loads(obj, object_hook=my_decoder)
