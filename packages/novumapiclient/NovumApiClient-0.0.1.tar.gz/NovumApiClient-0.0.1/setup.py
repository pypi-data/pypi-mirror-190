from setuptools import setup, find_packages

setup(
    name="NovumApiClient",
    version="0.0.1",
    description="This is an client API to access Novum Service Center",
    url="https://github.com/novum-engineering",
    author="Leonardo Biz",
    author_email="l.biz@novum-engineering.com",
    license="BSD 2-clause",
    packages=find_packages(),
    install_requires=["json", "requests", "urllib3", "http"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
    ],
)
