from setuptools import setup, find_packages

setup(
    name='convert-thai-to-arabic',
    version='0.0.1',
    description='Convert Thai numbers in file names to Arabic numbers',
    author='jaytrairat',
    author_email='jaytrairat@outlook.com',
    url='https://github.com/jaytrairat/convert_thai_to_arabic',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'convert_thai_to_arabic = convert_thai_to_arabic.convert_thai_to_arabic:main'
        ],
    },
)
