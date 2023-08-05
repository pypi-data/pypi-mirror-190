from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Django field permission package'


def read(f):
    return open(f, 'r', encoding='utf-8').read()


# Setting up
setup(
    name="df-permission",
    version=VERSION,
    author="Maxmudov Asliddin",
    author_email="<asliddin750750@gmail.com>",
    description=DESCRIPTION,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(include=['df_permission']),
    install_requires=['django>=3', 'djangorestframework'],
    keywords=['python', 'field', 'permission', 'field permission', 'django field'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
