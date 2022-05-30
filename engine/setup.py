import sys
sys.argv = ["setup.py", "build_ext", "--inplace"]

from setuptools import setup
from Cython.Build import cythonize
from pathlib import Path

directory_path = Path(__file__).parent.resolve()
module_list = [directory_path / 'render.pyx']

setup(
    ext_modules=cythonize(module_list, annotate=True),
)