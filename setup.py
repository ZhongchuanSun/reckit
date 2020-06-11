import os
import shutil
import numpy as np
from Cython.Build import cythonize
from setuptools.extension import Extension
from setuptools import setup
import setuptools
from functools import wraps


def get_include_dirs(workspace):
    include_dirs = [np.get_include()]
    for root, dirs, files in os.walk(workspace):
        for file in files:
            if file.endswith("h") or file.endswith("hpp"):
                include_dirs.append(root)

    return list(set(include_dirs))


def get_extensions(workspace):
    extensions = []

    for root, dirs, files in os.walk(workspace):
        for file in files:
            if file.endswith("pyx"):
                pyx_file = os.path.join(root, file)
                pyx_path = pyx_file[:-4].split(os.sep)
                pyx_path = pyx_path[1:] if pyx_path[0] == '.' else pyx_path[1:]
                name = ".".join(pyx_path)

                extension = Extension(name, [pyx_file],
                                      extra_compile_args=["-std=c++11"])
                extensions.append(extension)
    return extensions


def clean(func):
    """clean intermediate file
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        def _clean_file():
            new_dirs = set()
            new_files = set()
            for root, dirs, files in os.walk("."):
                new_dirs.update([os.path.join(root, d) for d in dirs])
                new_files.update([os.path.join(root, f) for f in files])

            for new_dir in new_dirs:
                if os.path.exists(new_dir) and new_dir not in old_dirs \
                        and "dist" not in new_dir.split(os.path.sep):
                    shutil.rmtree(new_dir)
            for new_file in new_files:
                if os.path.exists(new_file) and new_file not in old_files \
                        and "dist" not in new_file.split(os.path.sep):
                    os.remove(new_file)

        old_dirs = set()
        old_files = set()
        for root, dirs, files in os.walk("."):
            old_dirs.update([os.path.join(root, d) for d in dirs])
            old_files.update([os.path.join(root, f) for f in files])

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            _clean_file()
            raise e

        _clean_file()
        return result

    return wrapper


@clean
def setup_package():
    extensions = get_extensions(".")
    include_dirs = get_include_dirs(".")
    module_list = cythonize(extensions, language="c++", annotate=False)
    setup(name="reckit",
          ext_modules=module_list,
          include_dirs=include_dirs,
          packages=setuptools.find_packages()
          )


if __name__ == '__main__':
    setup_package()