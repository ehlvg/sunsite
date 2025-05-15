from setuptools import setup, find_packages

setup(
    name="sunsite",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "markdown",
        "python-frontmatter",
        "pyyaml",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "sunsite=sunsite.cli:main",
        ],
    },
)
