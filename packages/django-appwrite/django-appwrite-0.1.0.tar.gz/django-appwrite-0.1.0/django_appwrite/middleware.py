from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.conf import settings
from appwrite.client import Client
from appwrite.services.users import Users

User = get_user_model()


class AppwriteMiddleware:
    def __init__(self, get_response):
        # Try to retrieve the required Appwrite settings from the Django settings file
        try:
            project_endpoint = settings.APPWRITE['PROJECT_ENDPOINT']
            project_id = settings.APPWRITE['PROJECT_ID']
            project_key = settings.APPWRITE['PROJECT_API_KEY']
            self.user_id_header = settings.APPWRITE['USER_ID_HEADER'] or 'USER_ID'
        except AttributeError:
            raise Exception("""
                Make sure you have the following settings in your Django settings file:
                APPWRITE = {
                    'PROJECT_ENDPOINT': 'https://example.com/v1',
                    'PROJECT_ID': 'PROJECT_ID',
                    'PROJECT_API_KEY': 'PROJECT_API_KEY',
                    'USER_ID_HEADER': '[USER_ID]',
                }
            """)

        self.get_response = get_response

        # Initialize Appwrite client
        self.client = (Client()
                       .set_endpoint(project_endpoint)
                       .set_project(project_id)
                       .set_key(project_key))

        # Initialize Appwrite Users service
        self.users = Users(self.client)

    def __call__(self, request):
        # Get the user ID from the header
        user_id = request.META.get(self.user_id_header, '')

        user_info = None
        # If the user ID header is present
        if user_id:
            try:
                # Get the user information from Appwrite
                user_info = self.users.get(user_id)
            except Exception as e:
                # Return the response without doing anything
                return self.get_response(request)

        # If the user information was retrieved successfully
        if user_info:
            # Get the Django user by its email
            user = User.objects.filter(username=user_info['email']).first()

            # If the user doesn't exist, create it
            if not user:
                user = User.objects.create_user(user_info['email'], password=None, email=user_info['email'])

            # Authenticate the user using the email as the username
            user = authenticate(request, username=user_info['email'], password=None)

            # If the authentication was successful, log the user in
            if user:
                login(request, user)
                request.user = user

        # Call the next middleware/view in the pipeline
        response = self.get_response(request)

        return response
