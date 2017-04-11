from setuptools import setup, find_packages

setup(
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,

    name='awareness-operator',
    version='0.9.1',
    description='A Python implementation of the Awareness operator, a new way to think about data transfer and processing on the Internet.',
    author='Aedan Cullen',
    author_email='aedancullen@gmail.com',
    url='https://github.com/awrns/operator',
    keywords = ['functionality', 'distribution', 'network', 'learning', 'processing', 'awareness', 'operator']
)


