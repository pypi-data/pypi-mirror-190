from setuptools import find_packages, setup
# read the contents of your README file
def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='etpay_sdk',
    packages=find_packages(include=['etpay_sdk']),
    version='1.0.1',
    description='Etpay SDK for Python',
    license='BSD',
    install_requires=["requests", "pyjwt"],
    long_description=readme(),
    long_description_content_type='text/markdown'
)