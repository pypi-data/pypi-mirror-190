"""
@filename:setup.py
@author:Chen Kunxu
@time:2023-02-07
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FedDCM",
    version="0.0.2",
    author="hejunshu,chenkunxu",
    author_email="2676133653@qq.com",
    description="Federated Discrete Choice Model",
    long_description=long_description,
    # long_description_content_type="README.md",
    url="https://github.com/kx-36/FedDCM",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
