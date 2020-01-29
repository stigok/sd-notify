from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="sd-notify",
    version="0.1.0",
    py_modules=["sd_notify"],
    author="stigok",
    author_email="stig@stigok.com",
    description="Simple sd_notify client library for Python 3",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="sd-notify systemd python3 watchdog",
    url="http://github.com/stigok/sd-notify/",
    project_urls={
        "Bug Tracker": "http://github.com/stigok/sd-notify/issues",
        "Documentation": "http://github.com/stigok/sd-notify/",
        "Source Code": "http://github.com/stigok/sd-notify/",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.5",
)
