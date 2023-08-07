from setuptools import setup, find_packages

setup(
    name="rustylib",
    version='1.5.6',
    author="ZeyaTsu",
    description="Rusty or rustylib is a useful python library containing tools such as HTTP requests, mathematics, and more. https://github.com/ZeyaTsu/rustylib",
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['requests'],
)