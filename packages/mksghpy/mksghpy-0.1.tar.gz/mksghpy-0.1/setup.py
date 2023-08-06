from setuptools import setup, find_packages


VERSION = '0.1'
DESCRIPTION = 'py packahe to test skill'

# Setting up
setup(
    name="mksghpy",
    version=VERSION,
    author="mksgh",
    author_email="<mksgh@hmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['argparse'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)