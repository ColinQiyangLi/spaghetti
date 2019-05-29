import torch.nn as nn
import spaghettini
from spaghettini import register, quick_register, load, check

quick_register(nn.Linear)
register("relu")(nn.ReLU)
quick_register(nn.Sequential)
print(check())

net = load("assets/pytorch.yaml")
print(net)
