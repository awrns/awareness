from setuptools import setup, find_packages

setup(
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,

    install_requires=[
          'Theano==0.9.0',
    ],

    name='awareness',
    version='25.2',
    description='The new architecture of co-computation for data processing and machine learning.',
    author='Aedan Cullen',
    author_email='aedancullen@gmail.com',
    url='https://github.com/awrns/awareness',
    keywords = ['networking', 'ai', 'machine', 'learning', 'software', 'architecture', 'library', 'python', 'module', 'cocomputation', 'protocol', 'cloud', 'computing', 'iot']
)


