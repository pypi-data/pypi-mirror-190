from setuptools import setup, find_packages

setup(
    name='PyCMSRCryptor',
    version='1.0.0',
    url='',
    license='MIT Licence',
    keywords = 'testing testautomation',
    author='yujingrong',
    platforms = 'any',
    python_requires = '>=3.7.*',
    author_email='jakubik@126.com',
    description='',
    install_requires=[
        'rsa==4.8',
        'pyDes==2.0.1',
        'cryptography==37.0.2',
        'pycryptodome==3.14.1',
        'gmssl==3.2.1'
    ],
    package_dir = {'': 'src'},
    packages = find_packages('src')
)
