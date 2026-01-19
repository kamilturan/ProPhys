from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prophys",
    version="0.1.0",
    author="MkT",
    description="Protein Physicochemical Profiling Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kamilturan/ProPhys",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "requests>=2.25.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "prophys=prophys.cli:main",
            "prophys-server=prophys.server:run_server",
        ],
    },
)
