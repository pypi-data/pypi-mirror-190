import setuptools

with open(r"README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LonginusAlpha",
    version="0.4.9",
    author="Example Author",
    author_email="team.longinus.project@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/projectlonginus/LonginusPYPI",
    install_requires=['pyCryptodome','asyncio','argon2-cffi','requests','pyCryptodomex'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.11',
)