from setuptools import setup, find_packages

setup(
    name='undidPyjl', 
    version='0.0.0',  
    description='Python wrapper for Undid.jl.',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    author='Eric Jamieson',  
    author_email='ericjamieson@cmail.carleton.ca',  
    url='https://github.com/ejamieson97/undidPyjl',  
    packages=find_packages(),  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
    install_requires=[
        'juliacall>=0.9.20'
    ],
)
