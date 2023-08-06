from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='MyClickUp',
    packages=find_packages(include=['MyClickUp']),
    version='0.1.1',
    description='The MyClickUp class allows you to encapsulate the integration with the ClickUp API',
    description_content_type='text/plain',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Jose Cordeiro',
    license='MIT',
    setup_requires=['requests'],
)
