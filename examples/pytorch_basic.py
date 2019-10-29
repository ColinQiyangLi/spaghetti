import torch.nn as nn
import spaghettini
from spaghettini import register, quick_register, load, check, check_registered

quick_register(nn.Linear)
register("relu")(nn.ReLU)
quick_register(nn.Sequential)
print(check())
print(check_registered())

net = load("examples/assets/pytorch.yaml", verbose=True)
print(net)
