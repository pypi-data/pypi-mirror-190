"""
this is the setup of this package.
"""

from setuptools import setup
from setuptools import find_packages

from just_because import VERSION

with open('just_because/requirements.txt', 'r', encoding='utf8') as file:
    install_requires = list(map(lambda x: x.strip(), file.readlines()))

with open('README.md', 'r', encoding='utf8') as file:
    long_description = file.read()

setup(
    name='just-because',
    version='.'.join(map(str, VERSION)),
    author='ikun',
    author_email='zqmillet@qq.com',
    url='https://github.com/zqmillet/just-because',
    description='鸡你太美',
    packages=find_packages(),
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data={
        'just_because': ['words/*.txt'],
    },
)
