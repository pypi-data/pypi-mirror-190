# This file is placed in the Public Domain.
# pylint: disable=C0116


"botlib's setuptools setup.py"


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="botlib",
    version="202",
    url="https://github.com/bthate/botlib",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="The Python3 bot Namespace",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["bot", "bot.modules", "bot.runtime"],
    zip_safe=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
