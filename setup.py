from setuptools import setup, find_packages

setup(
    name="kappacrypt",
    version="0.1",
    packages=find_packages(),
    url="https://github.com/pikulak/kappacrypt",
    license="GPLv3",
    author="pikulak",
    author_email="pikulak1@gmail.com",
    requires=["pycrypto"],
    description="File crypting utility using RSA + AES"
)