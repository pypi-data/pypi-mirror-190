from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

with open("README.md", "r") as fh:
    readme = fh.read()

long_description = readme

cmds = ["cmd/*.txt"]

setup(
    name='ez_docs',
    version='1.1.0',
    author="""
        Bruno Ribeiro,
        Bruno Martins,
        Diógenes Dantas,
        Igor Penha,
        Lucas Gobbi e Rafael Nobre
    """,
    author_email='ezdocsteam@gmail.com',
    url='https://github.com/fga-eps-mds/2022-2-ez-docs',
    description='A python package to quick doc generation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords=['ez_docs', 'ez-docs'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'ez_docs': cmds},
    entry_points={
            'console_scripts': [
                'ez-docs=ez_docs.main:main'
            ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),

    install_requires=requirements
)
