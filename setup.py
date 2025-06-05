"""
Setup script for VaahAI.
"""
from setuptools import setup, find_packages

setup(
    name="vaahai",
    version="0.1.0",
    description="VaahAI - AI Agent Framework",
    author="WebReinvent",
    author_email="info@webreinvent.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.3.5",
        "inquirerpy>=0.3.4",
    ],
    entry_points={
        "console_scripts": [
            "vaahai=vaahai.cli.main:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
