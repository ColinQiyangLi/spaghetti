import torch.nn as nn
import spaghettini
from spaghettini import register, quick_register, load, check

quick_register(nn.Linear)
quick_register(nn.ReLU)


@quick_register
class MLP(nn.Module):
    def __init__(self, units, activation, linear_module):
        super().__init__()
        model = []
        for index, (in_units, out_units) in enumerate(zip(units[:-1], units[1:])):
            if index != 0:
                model.append(activation)
            model.append(linear_module(in_units, out_units))
        self.model = nn.Sequential(*model)

    def forward(self, x):
        return self.model(x)


print(check())
net = load("assets/pytorch_mlp.yaml")
print(net)
