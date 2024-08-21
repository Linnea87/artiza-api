# ARTiza API

## Table of contents

- [Purpose of the API](#purpose-of-the-api)
- [Testing](#testing)
    - [Manual Testing](#manual-testing)
- [Deployment](#deployment)
    - [JWT tokens](#jwt-tokens)
    - [Root Route](#root-route)

## Purpose of the API

The purpose of the API is to serve as the Back-end for the Front-end of the 5th project for code institute. This is needed for posting and getting data from endpoints and to perform Create, Read, Update and Delete operations to objects entered by Users via Front-end.

## Testing

### Manual Testing

All the testing was completed during each step. Going into the framework of the local server and typing in profiles, posts, likes, comments, and followers at the end of the link, as this example; *8000-linnea87-artizaapi-ng62e7lgk70.ws.codeinstitute-ide.net/profiles*

* A list of all profiles is displayed regardless of whether users are logged in or not


![Profile Testing- signed out](readmedoc/profile-testing5.png)

![Profile Testing- signed in](readmedoc/profile-testing-1.png)

* When users visit other users' profiles, it says that the visiting user is not the owner of that profile. The CRUD form is also not displayed if the users are not authorized

![Profile Testing- not authorized](readmedoc/profile-testing2.png)

* If the user is the owner of the profile, this is also displayed. As well as the CRUD form is displayed if the user is authorized

![Profile Testing- authorized](readmedoc/profile-testing3.png)

* if users try to access a profile or page that does not exist, a 404 error is displayed

![Profile Testing- 404 error](readmedoc/profile-testing4-error.png)

## Deployment
### JWT tokens
The first step of deployment is setting up the JWT tokens:

* First install the package in the terminal window, using the command:

    ```
    pip install dj-rest-auth
    ```

* In the settings.py file add the following to the "Installed Apps" section.

    ```
    'rest_framework.authtoken',
    'dj_rest_auth',
    ```

* Next, add the following URLs to the urlpatterns list:

    ```
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    ```

* In the command terminal, migrate the database just added by typing:

    ```
    python manage.py migrate
    ```

* Next we want to add the feature to enable the registration of users. Type the following into the terminal:

    ```
    pip install 'dj-rest-auth[with_social]'
    ```

* Add the following to the "Installed Apps" section in the settings.py file:

    ```
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    ```

Finally, add JWT tokens functionality:

* Install the djangorestframework-simplejwt package by typing the following into the terminal command window:

    ```
    pip install djangorestframework-simplejwt
    ```

* In the env.py file, create a session authentication value (differentiates between Dev and Prod mode):

    ```
    os.environ['DEV'] = '1'
    ```

* In the settings.py file, use the Dev value above to differentiate between Dev and Prod Modes & add pagination which is placed under SITE_ID:

    ```
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [( 
            'rest_framework.authentication.SessionAuthentication' 
            if 'DEV' in os.environ 
            else 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
        )]
    }
    ```

* To enable token authentication, put the following under the above step:
    
    ```
    REST_USE_JWT = True
    ```

* To ensure tokens are sent over HTTPS only, add the following:

    ```
    JWT_AUTH_SECURE = True
    ```

* Next, declare cookie names for the access and refresh tokens by adding:
    
    ```
    JWT_AUTH_COOKIE = 'my-app-auth'
    JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
    ```

Now we need to add the profile_id and profile_image to fields returned when requesting logged in user’s details:

* Create a new serializers.py file in the api folder. Then import the following files at the top of the new serializers file and create the profile_id and profile_image fields:

    ```
    from dj_rest_auth.serializers import UserDetailsSerializer
    from rest_framework import serializers

    class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )
    ```

* In settings.py, overwrite the default USER_DETAILS_SERIALIZER, below the JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token' :

    ```
    REST_AUTH_SERIALIZERS = {'USER_DETAILS_SERIALIZER': '<your appname>.serializers CurrentUserSerializer'}
    ```

* Next, in the terminal command window:

    1: Run migrations

    ```
    python manage.py migrate
    ```
    2: Update the requirements text file:

    ```
    pip freeze > requirements.txt
    ```
    
    3: git add, commit and push.

Bug Fix - dj-rest-auth doesn’t allow users to log out:

* In the <projectname>_api/views.py, import JWT_AUTH settings from settings.py

    ```
    from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
    )
    ```

* Write a logout view. It can be found [here](https://github.com/Linnea87/artiza-api/blob/main/artiza_api/views.py)

* Import the logout view in the <projectname>_api/urls.py

    ```
    from .views import root_route, logout_route
    ```

* Include it in the urlpatterns list, above the default dj-rest-auth urls, so that it is matched first.

    ```
    urlpatterns = [
        path('', root_route),
        path('admin/', admin.site.urls),
        path('api-auth/', include('rest_framework.urls')),
        path('dj-rest-auth/logout/', logout_route),
        path('dj-rest-auth/', include('dj_rest_auth.urls')),
        ...
    ]
    ```

    Add, Commit and Push your code to GitHub.

### Root Route

* Create a views.py file in the API folder. Set up the imports in the views.py file:

    ```
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    ```

* Create root route and return custom message:

    ```
    @api_view()
    def root_route(request):
        return Response({"message": "Welcome to my API!"})
    ```

* In the urls.py file, import:

    ```
    from .views import root_route
    ```

* Add the URL to urlpatterns list:

    ```
    urlpatterns = [
    path('', root_route)
    ]
    ```

* In the root route, no longer displays the 404 Error



