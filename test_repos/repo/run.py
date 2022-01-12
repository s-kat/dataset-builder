import importlib
import runpy
import subprocess

import tox
from viztracer import VizTracer

tracer = VizTracer(log_func_args=True, log_func_retval=True)
tracer.start()
runpy.run_module(mod_name='tox')
#subprocess.run('tox')
print("BOOBA")
# Something happens here
tracer.stop()
tracer.save() # also takes output_file as an optional argument