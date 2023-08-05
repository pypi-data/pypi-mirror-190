from setuptools import setup, find_packages
setup(
    name='eon_fms_client',
    version='0.1.3',
    license='MIT',
    author="Ahmad Salameh",
    author_email='a.salameh@eonaligner.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://bitbucket.org/eon-mes/broker_utilities/src/master',
    keywords='eon fms client',
    install_requires=[
        "python-magic==0.4.27",
        "requests==2.25.1",
    ],
)
