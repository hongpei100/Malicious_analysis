import torch
import numpy
from torch import nn
from Malicious_app import app
from celery import current_task

# n_pkts = 8        # first n_pkts packets of the flow
# n_bytes = 80      # first n_bytes of the packet
# maltypes_amt = 10 # amount of the types of the malicious packets

class CNN_RNN(nn.Module):
    def __init__(self):
        super(CNN_RNN, self).__init__()
        self.layers1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=(2, 4)),
            nn.MaxPool2d( kernel_size = ( 2, 3 ), stride = 1 ),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=(2, 4)),
            nn.MaxPool2d( kernel_size = ( 2, 3 ), stride = 1 ),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )
        self.lstm5 = nn.LSTM(280, 100, batch_first = True)
        
        self.layers2 = nn.Sequential(
            nn.ReLU(),
            nn.Linear(6400, 100),
            nn.ReLU(),
            nn.Linear(100, 11),
        )
            
    def forward(self, x):
        x_in = x.view(x.size()[0], 1, x.size()[1], x.size()[2])
        x = self.layers1(x_in)
        x_in = x.view(x.size()[0], x.size()[1], -1)
        x_out, (h_n, c_n) = self.lstm5(x_in, None)
        x = x_out.contiguous().view(x_out.size()[0], -1)
        
        out = self.layers2(x)
        
        return out

@app.task
def do_classify(ft):
    PKT_CLASSIFIER = CNN_RNN()
    PKT_CLASSIFIER.load_state_dict(torch.load("pkt_classifier.pt", map_location=torch.device("cpu")))
    PKT_CLASSIFIER.eval() #set for batchnormalization

    print("*************DO CLASSIFYING********************")
    output = PKT_CLASSIFIER(ft)

    return output

