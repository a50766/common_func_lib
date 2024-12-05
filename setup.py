from setuptools import setup, find_packages

setup(
    name="common_func_lib",
    version="0.1.0",
    description="Common library for Python reusable functions",
    author="Eduarda",
    packages=find_packages(),
    install_requires=[
        "django~=5.0",  # Django para transações
        "requests==2.31.0",  # Para requisições HTTP
        "xmltodict==0.13.0",  # Para parse de XML
    ],
)