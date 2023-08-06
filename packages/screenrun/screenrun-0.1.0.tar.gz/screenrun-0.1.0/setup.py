'''
Setup script for the package.
'''

from setuptools import setup, find_packages


setup(
    name='screenrun',
    author='Philip Orange',
    email='pypi@philiporange.com',
    url='https://www.github.com/philiporange/screenrun',
    version='0.1.0',
    description='''
Simple process management. Keep a process running in a screen session forever.
''',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['screenrun'],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'screenrun = screenrun.__main__:main',
        ],
    },
    classifiers=[
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
)
