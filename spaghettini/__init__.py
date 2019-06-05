__version__ = "0.0.6"

import oyaml as yaml
import types
from .template import expand

MODULES = {}

def check():
    return {
        "num_modules": len(MODULES),
        "keys": list(MODULES)
    }

def quick_register(module):
    name = module.__name__
    assert name not in MODULES, "the module with {} is already registered".format(name)
    MODULES[name] = module
    return module

def register(name=None):
    assert name not in MODULES, "the module with {} is already registered".format(name)
    names = [name]
    def core(module):
        name = names[0]
        if name is None:
            name = module.__name__
        MODULES[name] = module
        return module
    return core

def get(name):
    return MODULES[name]

def configure(d, record_config=False):
    if type(d) == dict:
        new_d = {}
        for key, value in d.items():
            if key.startswith("[") and key.endswith("]"):
                for k, v in value.items():
                    assert k not in new_d
                    new_d[k] = v
            else:
                new_d[key] = value
        d = new_d
                
        assert "<type>" in d, d
        m = get(d["<type>"])
        def core(*args, **kwargs):
            extra_kwargs = {k: configure(d[k]) for k in filter(lambda x: 
                (not x.endswith(">") and not x.startswith("<")), d)}
            if "<list>" in d:
                extra_args = list(map(configure, d["<list>"]))
            else:
                extra_args = []
            v = m(*args, *extra_args, **kwargs, **extra_kwargs)
            if record_config:
                v.__config__ = d
            return v

        if "<init>" in d and d["<init>"]:
            return core()
        return core
    if type(d) == list:
        return list(map(configure, d))
    return d

def load(path):
    if path.endswith("yaml"):
        with open(path, "r") as f:
            x = yaml.load(f, Loader=yaml.FullLoader)
        return configure(x, record_config=True)
    return None
