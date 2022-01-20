from dataset_builder.logger import log


def check_value_serialization(val):
    try:
        exec(f"x = {val}")
        return True
    except:
        return False


def filter_args(arg_ret_list):
    none_ret_count = 0
    for cur_args_ret in arg_ret_list:
        # check if class method
        if "self" in cur_args_ret["func_args"].keys():
            return False

        arg_list = cur_args_ret["func_args"]
        ret_val = cur_args_ret.get("return_value", "None")

        # check return value
        if not check_value_serialization(ret_val):
            return False

        none_ret_count += 1 if ret_val == "None" else 0
        # check all args
        for arg in arg_list.values():
            if not check_value_serialization(arg):
                return False

    if none_ret_count == len(arg_ret_list):
        return False

    return True


def filter_functions(total_functions):
    # total functions
    funcs = {}

    for cur_funcs in total_functions.values():
        for func_name in cur_funcs:
            if filter_args(cur_funcs[func_name]["args"]):
                funcs[func_name] = cur_funcs[func_name]
    log.info(f"Extract {len(funcs)} functions")
    return funcs
