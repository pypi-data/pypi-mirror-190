import os

import pkg_resources
from setuptools import setup, find_namespace_packages

setup(
    name="centernet2",
    version="1.0.post20221121",
    url="https://github.com/xingyizhou/CenterNet2",
    description="CenterNet2 python package",
    long_description="## CenterNet2 python package\n\n"
                     "Note: This is unofficial. I add a setup.py to publish this package including "
                     "add commit date to version and etc.",
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(include=["centernet*"]),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    include_package_data=True,
    extras_require={'dev': ['pytest']},
)
