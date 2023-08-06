from setuptools import setup, find_packages

setup(
    name='django-appwrite',
    version='0.0.1',
    description='Django Middleware to authenticate users with Appwrite',
    packages=find_packages(),
    package_dir={'django_appwrite': 'django_appwrite'},
    install_requires=['appwrite', 'django']
)
