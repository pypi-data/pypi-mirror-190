from setuptools import setup, find_packages

setup(
    name='orders_pr_messaging',
    version='0.1.0',
    description='orders system common messaging',
    author='Viktor',
    author_email='test@mail.com',
    packages=find_packages(),
    install_requires=[
        'aio-pika==8.3.0',
        'pika==1.3.1'
    ],
)
