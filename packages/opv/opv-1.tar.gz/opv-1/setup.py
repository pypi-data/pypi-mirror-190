# This file is placed in the Public Domain.


"Big Object"


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="opv",
    version="1",
    author="Bart Thate",
    author_email="operbot100@gmail.com",
    url="http://github.com/operbot/opv",
    zip_safe=True,
    description="object programming interface",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["opv"],
    scripts=["bin/opv"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
