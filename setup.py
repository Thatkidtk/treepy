# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rptree",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A directory tree generator with multiple output formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rptree",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "rptree=rptree.cli:main",
        ],
    },
)

# requirements.txt
pathlib>=1.0.1

# requirements-dev.txt
pytest>=7.0.0
pytest-asyncio>=0.18.0
pytest-cov>=3.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.900
