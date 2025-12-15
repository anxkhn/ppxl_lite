"""
Setup script for ppxl_lite - Lightweight Perplexity AI client
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ppxl_lite",
    version="2.0.0",
    author="Anas Ghani",
    author_email="your-email@example.com",
    description="A lightweight Python client for Perplexity AI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/perplexity-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="perplexity ai search api client lightweight",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/perplexity-ai/issues",
        "Source": "https://github.com/yourusername/perplexity-ai",
    },
)