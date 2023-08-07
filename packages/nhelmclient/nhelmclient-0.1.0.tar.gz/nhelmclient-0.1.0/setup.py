import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nhelmclient",
    version="0.1.0",
    author="NMachine",
    description="Helm client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        exclude=[
            "nhelmclient.tests.*",
            "nhelmclient.tests",
            "nhelmclient.e2e_test.*",
            "nhelmclient.e2e_test",
        ]
    ),
    install_requires=[
        "typing-extensions",
        "inflection",
        "pyyaml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
