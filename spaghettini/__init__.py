__version__ = "0.0.7"

import oyaml as yaml
import types
from .template import expand
import traceback
from pprint import pprint
import functools
from reprlib import repr

MODULES = {}


def check():
    return {
        "num_modules": len(MODULES),
        "keys": list(MODULES)
    }


def check_registered():
    print("################################################################")
    print("Printing registered modules: ")
    for module_key, module in sorted(MODULES.items(), key=lambda kv: kv[0]):
        print(f"{module_key:24}{module}")
    print("################################################################")


def quick_register(module):
    name = module.__name__
    assert name not in MODULES, "The module with {} is already registered. ".format(name)
    try:
        MODULES[name] = module
    except Exception as e:
        print("Exception: \n{}".format(e))
        print("Traceback: \n{}".format(traceback.print_exc()))
        print("Message: Couldn't find module named {} to load".format(name))

    return module


def register(name=None):
    assert name not in MODULES, "The module with {} is already registered. ".format(name)
    names = [name]

    def core(module):
        name = names[0]
        if name is None:
            name = module.__name__
        MODULES[name] = module
        return module

    return core


def get(name):
    try:
        return MODULES[name]
    except Exception as e:
        print("\nSpaghettini Message: Module '{}' not registered. \n".format(name))
        raise


def configure(d, record_config=False, verbose=False):
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
            configure_fn = functools.partial(configure, record_config=record_config, verbose=verbose)
            extra_kwargs = {k: configure_fn(d[k]) for k in filter(lambda x:
                                                               (not x.endswith(">") and not x.startswith("<")), d)}
            if "<list>" in d:
                extra_args = tuple(map(configure_fn, d["<list>"]))
            else:
                extra_args = tuple()
            try:
                v = m(*args, *extra_args, **kwargs, **extra_kwargs)
            except Exception as e:
                print(e)
                print("\nException occured while loading {}.\n".format(d["<type>"]))
                raise

            if record_config:
                v.__config__ = d
            if verbose:
                print(">>>>  Instantiating module: {}".format(m))
                print("Arguments:")
                for i, arg in enumerate(tuple(args + extra_args)):
                    print("\tArgument {}: {}".format(i, arg))
                print("Keyword arguments:")
                for curr_key, curr_value in sorted(dict(**kwargs, **extra_kwargs).items(), key=lambda kv: kv[0]):
                    print("\tKey: {}\n\t\t Value: {}".format(curr_key, repr(curr_value)))
                print("<<<<")
            return v

        if "<init>" in d and d["<init>"]:
            return core()
        return core
    if type(d) == list:
        return list(map(configure, d))
    return d


def load(path, verbose=False):
    if path.endswith("yaml"):
        with open(path, "r") as f:
            x = yaml.safe_load(f)
        if verbose:
            print(">>>>>>>>  Configuring from '{}'. ".format(path))
        return configure(x, record_config=True, verbose=verbose)
    return None
