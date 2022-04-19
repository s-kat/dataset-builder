import re

from dataset_builder.logger import log


def split_imports(imports):
    total = set()
    for cur_import in imports:
        for token in re.split("from | import | as |,", cur_import):
            token = token.strip()
            if len(token) > 0:
                total.add(token)
    return total


def check_value_serialization(val, imports):
    try:
        exec(f"x = {val}")
        return True
    except:
        tokens = split_imports(imports)
        for token in tokens:
            if token in val:
                return True
    return False


def filter_args(arg_ret_list, imports):
    none_ret_count = 0
    for cur_args_ret in arg_ret_list:
        # check if class method
        if "self" in cur_args_ret["func_args"].keys():
            return False

        arg_list = cur_args_ret["func_args"]
        ret_val = cur_args_ret.get("return_value", "None")

        # check return value
        if not check_value_serialization(ret_val, imports):
            return False

        none_ret_count += 1 if ret_val == "None" else 0
        # check all args
        for arg in arg_list.values():
            if not check_value_serialization(arg, imports):
                return False

    if none_ret_count == len(arg_ret_list):
        return False

    return True


def filter_functions(total_functions):
    # total functions
    funcs = {}

    for cur_funcs in total_functions.values():
        for func_name in cur_funcs:
            if filter_args(
                cur_funcs[func_name]["args"], cur_funcs[func_name].get("imports", [])
            ):
                funcs[func_name] = cur_funcs[func_name]
    log.info(f"Extract {len(funcs)} functions")
    return funcs
