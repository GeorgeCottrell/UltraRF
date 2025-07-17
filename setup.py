#!/usr/bin/env python3
"""
UltraRF Protocol Setup Script
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Extract version from __init__.py
version = "0.1.0"

setup(
    name="ultrarf-protocol",
    version=version,
    author="UltraRF Contributors",
    author_email="",
    description="Ultra high-speed RF networking protocol for amateur radio SHF bands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ultrarf-protocol",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Communications :: Ham Radio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
        "sdr": [
            "pyrtlsdr>=0.2.91",
            "soapysdr>=0.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ultrarf=ultrarf.cli:main",
            "ultrarf-beacon=ultrarf.beacon:main",
            "ultrarf-monitor=ultrarf.monitor:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ultrarf": ["config/*.yaml", "data/*.json"],
    },
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ultrarf-protocol/issues",
        "Source": "https://github.com/yourusername/ultrarf-protocol",
        "Documentation": "https://ultrarf-protocol.readthedocs.io/",
    },
)