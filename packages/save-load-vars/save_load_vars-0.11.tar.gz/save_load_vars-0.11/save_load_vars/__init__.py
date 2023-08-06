from windows_filepath import make_filepath_windows_comp
import os
from cprinter import TC
import glob
import sys

nl1, nl2 = "\n", "\r"


def save_vars_pkl(g, folder, interface="dill", protocol=None):
    if interface.lower() == "cloudpickle":
        from cloudpickle import pickle
    if interface.lower() == "dill":
        import dill as pickle
    else:
        import pickle
    if protocol is None:
        protocol = pickle.HIGHEST_PROTOCOL
    if not os.path.exists(folder):
        os.makedirs(folder)
    for key, item in g.items():
        fp = make_filepath_windows_comp(
            filepath=key,
            fillvalue="_",  # replacement of any illegal char
            reduce_fillvalue=True,  # */<> (illegal chars) -> ____ (replacement) -> _ (reduced replacement)
            remove_backslash_and_col=True,  # important for multiple folders
            spaceforbidden=True,  # '\s' -> _
            other_to_replace=(),  # other chars you don't want in the file path
            slash_to_backslash=False,  # replaces / with \\ before doing all the other replacements
        )
        npath = os.path.normpath(os.path.join(folder, fp + ".pkl"))

        try:
            with open(npath, "wb") as f:
                pickle.dump(item, f, protocol)
            print(TC(f"Saved: {key}").bg_black.fg_green)
        except Exception as fe:
            if os.path.exists(npath):
                try:
                    os.remove(npath)
                except Exception:
                    pass
            print(
                TC(
                    f'Error: {key} - {str(fe).replace(nl1," ").replace(nl2," ")}'
                ).bg_black.fg_red
            )
            continue


def load_vars_pkl(folder, name, interface="dill"):
    if interface.lower() == "cloudpickle":
        from cloudpickle import pickle
    if interface.lower() == "dill":
        import dill as pickle
    else:
        import pickle

    def loadp(fi):
        with open(fi, "rb") as f:
            data = pickle.load(f)
        return data

    didi = {}
    allfi = glob.glob(folder.rstrip(os.sep) + os.sep + "*.pkl")
    for a in allfi:
        try:
            didi[(p := a.split(os.sep)[-1].replace(".pkl", ""))] = loadp(a)
            print(TC(f"Loaded: {p}").bg_black.fg_green)
        except Exception as fe:
            print(
                TC(
                    f'Error:  {a} - {str(fe).replace(nl1," ").replace(nl2," ")}'
                ).bg_black.fg_red
            )
            continue
    if name is not None:
        globals_from_dict(di=didi, name=name)
    else:
        return didi


def globals_from_dict(di, name):
    for key, item in di.items():
        setattr(sys.modules[name], key, item)
