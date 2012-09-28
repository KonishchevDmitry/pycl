from setuptools import find_packages, setup

with open("README") as readme:
    setup(
        name = "pycl",
        version = "0.1",

        license = "GPL",
        description = readme.readline().strip(),
        long_description = readme.read().strip(),
        url = "https://github.com/KonishchevDmitry/pycl",

        author = "Dmitry Konishchev",
        author_email = "konishchev@gmail.com",

        packages = find_packages(),
    )
