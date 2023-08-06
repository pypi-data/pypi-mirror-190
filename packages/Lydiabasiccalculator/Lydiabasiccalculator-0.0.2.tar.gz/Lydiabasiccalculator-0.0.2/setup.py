from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Lydiabasiccalculator',
    version='0.0.2',
    description='A very basic caluclator',
    long_description=open('README.mp').read() + '\n\n' + open('CHANGELOG.mp').read(),
    url='',
    author='Lydia Whittaker',
    author_email='lydwhitt7@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packaages=find_packages(),
    install_requires=['']
)