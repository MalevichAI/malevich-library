from setuptools import setup

requirements = open('requirements.txt').read().split()
version = open('VERSION').read().strip()

setup(
    name="malevich-library",
    version=version,
    description=(
        "Standalone SDK for building apps at Malevich (malevich.ai)",
    ),
    packages=['mosaic'],
    install_requires=requirements,
)
