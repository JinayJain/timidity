import setuptools

with open("README.md") as fh:
    long_desc = fh.read()

setuptools.setup(
    name="timidity",
    version="0.1.2",
    description="A lightweight Python MIDI player",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/JinayJain/timidity",
    author="Jinay Jain",
    packages=setuptools.find_packages(),
    install_requires=[
        "simpleaudio",
        "numpy",
        "scipy"
    ]
)
