from setuptools import setup

setup(
    name='py8583',
    description='ISO8583 python library',
    long_description=open('README.md').read(),
    keywords='ISO8583 banking protocol library',

    url='https://github.com/insigmo/py8583',
    author='Betal Berbekov',
    author_email='qwantone@gmail.com',

    license='LGPLv2',
    packages=['py8583'],
    zip_safe=True
)