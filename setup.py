import os
from setuptools import setup, find_packages
import mocap2d


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='unity-2dmocap',
    version=mocap2d.__version__,
    description="Python application for Unity Asset of 2D motion capture",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords=["python", "motion capture", "unity"],
    author='SeBeom Lee',
    author_email='slee5@oberlin.edu',
    url='http://www.github.com/k2sebeom/unity-2dmocap',
    license="MIT",
    entry_points={
        'console_scripts': [
            "2dmocap-unity=mocap2d.detect:main",
            "2dmocap-edit=mocap2d.editor:main"
        ]
    },
    install_requires=read('requirements.txt').splitlines(),
    packages=find_packages(include=['mocap2d']),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    project_urls={
        'Maintainer': 'https://github.com/k2sebeom',
        'Source': 'https://github.com/unity-2dmocap',
        'Tracker': 'https://github.com/k2sebeom/unity-2dmocap/issues'
    },
)