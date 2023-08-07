from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="picorg",
    version="0.2.9",
    description="A script that helps you organize your pictures.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[
        "picorg",
        "timestamp_finder",
        "rename",
        "duplicates",
        "settings",
        "find_new",
    ],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pillow", "exifread", "pydantic"],
    url="https://github.com/frangiz/picorg",
    author="Björn Olsson Jarl",
    author_email="frangiz@gmail.com",
    entry_points={"console_scripts": ["picorg = picorg:main"]},
    python_requires=">=3.8",
)
