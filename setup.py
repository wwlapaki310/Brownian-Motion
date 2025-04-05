from setuptools import setup, find_packages

setup(
    name="brownian_robot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "pygame": ["pygame>=2.0.0"],
    },
    author="Satoru Akita",
    description="A Python module for simulating Brownian motion of a robot",
    python_requires=">=3.6",
)