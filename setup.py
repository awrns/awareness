from setuptools import setup, find_packages

setup(
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,

    install_requires=[
          'Theano==0.9.0',
    ],

    name='awareness',
    version='0.7.3',
    description='A new way to think about data on the Internet, like nothing ever before.',
    author='Aedan Cullen',
    author_email='aedancullen@gmail.com',
    url='https://github.com/awrns/awareness-python',
    keywords = ['networking', 'ai', 'machine', 'learning', 'software', 'architecture', 'library', 'python', 'module', 'cocomputation', 'protocol', 'cloud', 'computing', 'iot']
)


