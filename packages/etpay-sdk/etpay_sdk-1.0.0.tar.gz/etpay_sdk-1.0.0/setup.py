from setuptools import find_packages, setup
setup(
    name='etpay_sdk',
    packages=find_packages(include=['etpay_sdk']),
    version='1.0.0',
    description='Etpay SDK for Python',
    license='BSD',
    install_requires=["requests", "pyjwt"]
)