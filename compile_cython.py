from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy as np
import os
import shutil

pyx_dirs = ["reckit.evaluator.src", "reckit.random.src", "reckit.util.src"]
cpp_dirs = ["reckit.include", "reckit.evaluator.src", "reckit.util.src"]

pyx_dirs = [os.path.join(*d.split(".")) for d in pyx_dirs]
cpp_dirs = [os.path.join(*d.split(".")) for d in cpp_dirs]

extensions = [
    Extension(
        '*',
        ["*.pyx"],
        extra_compile_args=["-std=c++11"])
]

pwd = os.getcwd()

additional_dirs = [os.path.join(pwd, d) for d in cpp_dirs]

for t_dir in pyx_dirs:
    # t_dir = os.path.join(*t_dir.split())
    t_dir = os.path.join(pwd, t_dir)
    os.chdir(t_dir)
    ori_files = set(os.listdir("."))
    setup(
        ext_modules=cythonize(extensions,
                              language="c++",
                              # annotate=True
                              ),
        include_dirs=[np.get_include()]+additional_dirs
    )

    new_files = set(os.listdir("."))
    for n_file in new_files:
        if n_file not in ori_files and n_file.split(".")[-1] in ("c", "cpp"):
            os.remove(n_file)
        if n_file not in ori_files and n_file == "build":
            shutil.rmtree(n_file)
    os.chdir(pwd)
