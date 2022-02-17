from configparser import ConfigParser

from setuptools import find_packages, setup


config = ConfigParser()
config.read('setup.cfg')

setup(
    name=config.get('project', 'name'),
    version=config.get('project', 'version'),
    description=config.get('project', 'description'),
    author='Giuseppe Mascellaro',
    author_email='giuseppe.mascellaro@mail.polimi.it',
    license='',
    url=config.get('github', 'repository_url'),
    packages=find_packages(where='src', exclude=('tests.*', 'tests')),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        'python-decouple==3.5',
        'fastapi==0.70.0',
        'uvicorn==0.16.0',
        'numpy==1.21.4',
        'pandas==1.3.4',
        'scipy==1.8.0rc1',
        'matplotlib==3.5.1',
        'nltk==3.7',
        'scikit-learn==1.0.2',
        'fasttext==0.9.2',
        'flask==2.0.2',
        'aiohttp==3.8.1',
        'pillow==9.0.1',
        'getch==1.0',
        'blessings==1.7',
    ],
    extras_require={
        'dev': [
            'ipython==7.18.1',
            'notebook==6.4.6',
        ],
        'lint': [
            'flake8-builtins<2.0.0',
            'flake8-commas<3.0.0',
            'flake8-comprehensions<2.0.0',
            'flake8-debugger<4.0.0',
            'flake8-import-order<1.0.0',
            'flake8-mypy<18.0.0',
            'flake8-quotes<1.0.0',
            'flake8-todo<1.0',
            'flake8<4.0.0',
            'pep8-naming<1.0.0',
        ],
        'test': [
            'pytest<4.0.0',
            'pytest-cov<3.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'assist = typing_assistant.assist:main',
        ],
    },
)
