# Appwrite Middleware for Django

[![Build Status](https://travis-ci.org/appwrite/django.svg?branch=master)](https://travis-ci.org/appwrite/django)
[![PyPI version](https://badge.fury.io/py/appwrite.svg)](https://badge.fury.io/py/appwrite)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/appwrite.svg)](https://pypi.org/project/appwrite/)
[![PyPI - License](https://img.shields.io/pypi/l/appwrite.svg)]

[![Build Status](https://travis-ci.org/appwrite/drf.svg?branch=master)](https://travis-ci.org/appwrite/drf)
[![PyPI version](https://badge.fury.io/py/appwrite.svg)](https://badge.fury.io/py/appwrite)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/appwrite.svg)](https://pypi.org/project/appwrite/)
[![PyPI - License](https://img.shields.io/pypi/l/appwrite.svg)]

A Django middleware to authenticate users with Appwrite.

## Installation

To install `django_appwrite`, simply run:

```bash
$ pip install django-appwrite
```

## Usage

1. In your Django project's `settings.py` file, add `django_appwrite` to your MIDDLEWARE list:

```python
MIDDLEWARE = [
    ...,
    'django_appwrite.middleware.AppwriteMiddleware',
    ...
]
```
2. Configure the Appwrite client settings in your Django settings file:
```python
APPWRITE = {
    'PROJECT_ENDPOINT': 'https://example.com/v1',
    'PROJECT_ID': 'PROJECT_ID',
    'PROJECT_API_KEY': 'PROJECT_API_KEY',
    'USER_ID_HEADER': 'USER_ID',
}
```
| Setting | Default                                                         | Description                                                                                                |
| --- |-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| `PROJECT_ENDPOINT` |                                                                 | The endpoint of your Appwrite project. You can find this in the Appwrite console under Settings > General. |
| `PROJECT_ID` |                                                                 | The ID of your Appwrite project. You can find this in the Appwrite console under Settings > General.       |
| `PROJECT_API_KEY` |                                                                 | The API key of your Appwrite project. You can find this in the Appwrite console under Settings > API Keys. |
| `USER_ID_HEADER` | USER_ID | The header name that will be used to store the user ID.                                                    |

## How it works
This middleware class will get the user ID from the header specified in the `USER_ID_HEADER` setting.
It will then use this user ID to retrieve the user information from Appwrite using the `Users` service.
If a user is found, it will create a Django user if it doesn't exist, and authenticate the user.

Please note that this middleware is intended to be used in conjunction with the Appwrite client-side SDK to authorize users on the frontend, and does not provide any APIs for user authentication on its own.

## License
The appwrite-drf package is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.