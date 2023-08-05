from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='convert-thai-to-arabic',
    version='0.0.7',
    description='Convert Thai numbers in file names to Arabic numbers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='jaytrairat',
    author_email='jaytrairat@outlook.com',
    url='https://github.com/jaytrairat/python-connvert-thai-to-arabic',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'convert-thai-to-arabic = convert_thai_to_arabic.convert_thai_to_arabic:main'
        ],
    },
)
