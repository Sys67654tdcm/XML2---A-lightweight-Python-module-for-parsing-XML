from setuptools import setup, find_packages

setup(
    name="xml2",
    version="1.0.0",
    description="""XML2 (official name) / xml2 (module name) - An XML parser I made.
I was bored. It is LIGHTWEIGHT, and doesn't even use any external modules that aren't in the standard library.
It is designed to be SUPER FAST, for a Python lexer. It won't beat lxml or the actual xml module, BUT it can
go really fast. Hence the lexing in the __init__.""",
    author="Sys",
    packages=find_packages(),
    py_modules=["xml2"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
