import os

from setuptools import Command, find_packages, setup


class Clean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


setup(
    name='messengerwrapper',
    version='0.0.1.dev1',
    license='LICENSE',
    description='An unofficial Facebook Messenger Wrapper for Python.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/brian41005/Python-Messenger-Wrapper.git',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests>=2.18.4',
        'bs4>=0.0.1',
        'lxml>=4.2.3',
    ],
    python_requires='>=3.5.2',
    cmdclass={
        'clean': Clean
    },
    classifiers=(
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications :: Chat'
    ),
)
