from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="a-game",
    version="1.0.0",
    author="Anderson777",
    description="Jogue um jogo da velha direto pelo seu sistema python!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["a-game"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[],
    dependency_links=['https://github.com/ShadowLOL00/a-game']
)