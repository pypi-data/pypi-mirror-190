from setuptools import setup, find_packages

setup(
    name='antm',
    version='0.0.5',
    author='Hamed Rahimi',
    author_email='hamed.rahimi@sorbonne-universite.fr',
    description='Aligned Neural Topic Model for Exploring Evolving Topics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hamedR96/ANTM',
    project_urls={
        'Bug Tracker': 'https://github.com/hamedR96/ANTM/issues'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6'
)