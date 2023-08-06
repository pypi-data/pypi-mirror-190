import os

import pkg_resources
from setuptools import setup, find_namespace_packages

setup(
    name="detic-fast",
    version="1.0.post20230203",
    url="https://github.com/wikiwen/Detic",
    description="Fork of https://github.com/facebookresearch/Detic",
    packages=find_namespace_packages(include=["detic*"]),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    include_package_data=True,
    extras_require={'dev': ['pytest']},
)
