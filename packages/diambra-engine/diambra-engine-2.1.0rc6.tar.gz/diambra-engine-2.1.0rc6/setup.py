from pathlib import Path
import os
import setuptools
import setuptools.command.build_py

setuptools.setup(
    name='diambra-engine',
    url='https://diambra.ai',
    version=os.environ.get('VERSION', '0.0.0'),
    author="DIAMBRA Team",
    author_email="info@diambra.ai",
    description="DIAMBRA™ Arena Engine API Client",
    long_description = (Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    license='Custom',
    install_requires=[
            'pip>=21'
    ] + os.environ.get('REQUIREMENTS', '').split(':'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Artificial Life',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Arcade',
        'Topic :: Education',
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
)
