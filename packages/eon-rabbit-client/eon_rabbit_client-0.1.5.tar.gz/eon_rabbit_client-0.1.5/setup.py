from setuptools import setup, find_packages
setup(
    name='eon_rabbit_client',
    version='0.1.5',
    license='MIT',
    author="Ahmad Salameh",
    author_email='a.salameh@eonaligner.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://bitbucket.org/eon-mes/broker_utilities/src/master',
    keywords='eon broker project',
    package_data={"eon_rabbit_client": ["py.typed"]},
    install_requires=[
        "aio_pika==8.3.0",
      ],

)