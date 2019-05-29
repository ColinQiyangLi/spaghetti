import oyaml as yaml
import types
from .template import expand

MODULES = {}


def register(module):
    name = module.__name__
    assert name not in MODULES, "the module with {} is already registered".format(name)
    MODULES[name] = module
    return module

def get(name):
    return MODULES[name]

def configure(d):
    if type(d) == dict:
        assert "<type>" in d
        extra_kwargs = {k: configure(d[k]) for k in filter(lambda x: x not in ["<type>", "<init>"], d)}
        m = get(d["<type>"])
        def core(*args, **kwargs):
            return m(*args, **kwargs, **extra_kwargs)
        if "<init>" in d and d["<init>"]:
            return core()
        return core
    if type(d) == list:
        return list(map(configure, d))
    return d

def load(path):
    if path.endswith("yaml"):
        with open(path, "r") as f:
            x = yaml.load(f)
        return configure(x)
    return None
