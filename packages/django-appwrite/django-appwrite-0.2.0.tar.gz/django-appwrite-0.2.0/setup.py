from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='django-appwrite',
    version='0.2.0',
    description='Django Middleware to authenticate users with Appwrite',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_dir={'django_appwrite': 'django_appwrite'},
    install_requires=['appwrite', 'django'],
    license='MIT',
    author='Yusup Khasbulatov',
    readme='README.md',
)
