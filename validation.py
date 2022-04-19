import glob
import json
from pprint import pp, pprint
from tqdm import tqdm

def try_to_run(func):
    imports = '\n'.join(func['imports'])
    text = func['text']
    func_name = text[3:text.find('(')].strip()

    func_text_with_imports = imports + '\n' + text
    try:
        exec(func_text_with_imports)
        for args in func['args']:
            retval = args['return_value']
            arg_list = args['func_args']
            arg_text = ""
            for key, val in arg_list.items():
                arg_text += f"{key}={val},"
            if not eval(f'{func_name}({arg_text}) == {retval}'):
                print("ERROR IN VALIDATION!")
                return False

    except Exception as e:
        print(f"Cannot compile function {func_name}. Exception: {e}")
        return False
    
    return True



with open('outv2.json') as r_file:
    total_funcs = json.load(r_file)

good_funcs = []
bad_funcs = []

for func in tqdm(total_funcs):
    if try_to_run(func):
        good_funcs.append(func)
    else:
        bad_funcs.append(func)

with open('good_funcs.json', 'w') as w_file:
    json.dump(good_funcs, w_file)

with open('bad_funcs.json', 'w') as w_file:
    json.dump(bad_funcs, w_file)
