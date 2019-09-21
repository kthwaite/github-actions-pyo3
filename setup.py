# coding: utf-8

from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="sum_as_string",
    version="0.0.4",
    rust_extensions=[RustExtension("sum_as_string._string_sum", binding=Binding.PyO3)],
    packages=["sum_as_string"],
    zip_safe=False,
)
