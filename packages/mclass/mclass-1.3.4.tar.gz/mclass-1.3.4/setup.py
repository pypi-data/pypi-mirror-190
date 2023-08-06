from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mclass",
    version="1.3.4",
    author="Moses Dastmard",
    description="converts python dictoinary to class object",
    long_description=long_description,
    long_description_content_type='text/markdown'
)