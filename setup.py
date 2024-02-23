from setuptools import find_packages, setup

requirements = open('requirements.txt').read().split()
version = open('VERSION').read().strip()

setup(
    name="malevich-library",
    version=version,
    description=(
        "Standalone SDK for building apps at Malevich (malevich.ai)",
    ),
    packages=find_packages('.', exclude=['lib']),
    install_requires=requirements,
)
