from setuptools import setup, find_packages
from farmer.configurator import s

setup(
    name="arknights-farmer-cv",
    version=s.version,
    author="Tree",
    author_email="treetreewu@hotmail.com",
    description="Automation of ArkNights the game.",
    url="https://github.com/Treetreewu/ArkNights-Farmer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6.0',
    license='MIT'
)
