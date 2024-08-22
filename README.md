# ARTiza API


The purpose of the API is to serve as the Back-end for the Front-end of the 5th project for code institute. This is needed for posting and getting data from endpoints and to perform Create, Read, Update and Delete operations to objects entered by Users via Front-end.
## Table of contents

- [Testing](#testing)
    - [Manual Testing](#manual-testing)
- [Project Setup](#project-setup)
- [Deployment](#deployment)
    - [JWT tokens](#jwt-tokens)
    - [Preparing the API for deployment](#preparing-the-api-for-deployment)
        - [Root Route](#root-route)
        - [Pagination](#pagination)
        - [JSON Renderer](#json-renderer)
        - [Date and Time formatting - General Formatting](#date-and-time-formatting---general-formatting)
        - [Date and Time formatting - Comments and Post](#date-and-time-formatting---comments-and-post)
    - [Create PostgreSQL Database](#create-postgresql-database)
    - [Create Heroku App](#create-heroku-app)
    - [Project preparation for IDE](#project-preparation-for-ide)
    - [Install package to run the project on Heroku](#install-package-to-run-the-project-on-heroku)
- [Heroku deployment](#heroku-deployment)


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

## Project Setup

* Create a new repository using the Code Institute template repository.

* To install Django, run the command:

    ```
     pip3 install 'django<4'
    ```


* To create a new app, run the command:

    ```
    django-admin startproject my_api .
    ``` 

* To create a new superuser, run the command: 
    
    ```
    python3 manage.py createsuperuser  
    ```

* To install Cloudinary Storage, run the command:
   
   ```
    pip install django-cloudinary-storage 
    ```

* To add the image processing capabilities thats are neede in the project, run the command:

    ```
    pip install Pillow 
    ```


* Once these dependencies are installed we need to add them to the "Installed apps" section in settings.py:

    *Note the placement and terms used for this input into installed apps*

    ```
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    ```

* Create an env.py file in the top directory.

    * Inside the env.py file, import the os module and set up the os.environ with the Cloudinary URL you can retrieve from the account you've set up.

* In the settings.py file, set up a variable called "CLOUDINARY_STORAGE" and use the environment variable used to set up in the env.py file to declare this value.

* Next, define the setting called "MEDIA_URL" and set it to "/media/" so the settings know where to store our image files.

* Finally, define a variable called "DEFAULT_FILE_STORAGE" and set it to "MediaCloudinaryStorage".

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

### Preparing the API for deployment
#### Root Route

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

#### Pagination

* In the settings.py file, inside the REST_FRAMEWORK object, add Pagination:

    ```
    REST_FRAMEWORK = {
    ...,
    'DEFAULT_PAGINATION_CLASS':  'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    }
    ```

#### JSON Renderer

* In the settings.py file, set JSON Renderer if Dev environment is not present. Placed below, but separate from, the REST_FRAMEWORK list:
    ```
    REST_FRAMEWORK = {
    ...
    }
    if 'DEV' not in os.environ:
        REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
            'restframework.renderers.JSONRenderer'
        ]
    ```

#### Date and Time formatting - General Formatting

* In the settings.py file, format the Date and time in REST_FRAMEWORK list:

    ```
    REST_FRAMEWORK = {
    ...
    'DATETIME_FORMAT': '%d %b %Y'
    }
    ```

#### Date and Time formatting - Comments and Post

* In the Comment app, inside the serializers.py file. Then set the imports up in the file:

    ```
    from django.contrib.humanize.templatetags.humanize import naturaltime
    ````

* Set fields within the Serializer class:

    ```
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    ```

* Set methods, which are placed underneath fields:

    ```
    def get_created_at(self, obj):
        return naturaltime(obj.created_at)
    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)
    ```

* Next add, commit, and push the new additions.

### Create PostgreSQL Database

* Log in to ElephantSQL.com to access your dashboard

* Click “Create New Instance”

* Set up your plan

    * Give your plan a Name (this is commonly the name of the project)
    * Select the Tiny Turtle (Free) plan
    * You can leave the Tags field blank
    * Select “Select Region”

* Select a data center near you

* Then click “Review”

* Check your details are correct and then click “Create instance”

* Return to the ElephantSQL dashboard and click on the database instance name for this project

* In the URL section, click the copy icon to copy the database URL

### Create Heroku App

* Log into Heroku, and create a new app. (The name must be unique)

* Click “Select Region”, then click “Review” and then click "Create instance".

* Go back to the ElephantSQL dashboard and click on the database instance name for this project.

* Copy your ElephantSQL database URL using the Copy icon. It will start with postgres://

* Open the Settings tab, and click "Reveal config vars".

* Add a Config Var DATABASE_URL, and for the value, copy in your database URL from ElephantSQL (do not add quotation marks)

### Project preparation for IDE

* In the terminal, install dj_database_url and psycopg2, both of these are needed to connect to your external database:

    ```
    pip3 install dj_database_url==0.5.0 psycopg2
    ```

* In settings.py file, import dj_database_url underneath the import for os:

    ```
    import os import dj_database_url
    ```

* Update the DATABASES section to the following:

    ```
    if 'DEV' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    else:
        DATABASES = {
            'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
        }
    ```

This ensures that when you have an environment variable for DEV in your environment the code will connect to the sqlite database here in your IDE. Otherwise it will connect to your external database, provided the DATABASE_URL environment variable exist.

* In the env.py file, add a new environment variable with the key set to DATABASE_URL, and the value to your ElephantSQL database URL:

    ```
    os.environ['DATABASE_URL'] = "<your PostgreSQL URL here>"
    ```

* Temporarily comment out the DEV environment variable so that the IDE can connect to my external database

* Migrate your database models to your new database:

    ```
    python3 manage.py migrate
    ```

* Create a superuser for your new database and follow the steps to create your superuser username and password:

    ```
    python3 manage.py createsuperuser
    ```

* Confirming database:

    * On the ElephantSQL page for your database, in the left side navigation, select “BROWSER”

    * Click the Table queries button, select auth_user

    * Click “Execute”, it should display the new created superuser details. This confirms the tables have been created and can add data to the database

### Install package to run the project on Heroku

* In the terminal of your IDE workspace, install gunicorn:

    ```
    pip3 install gunicorn django-cors-headers
    ```

* Update your requirements.txt:

    ```
    pip freeze --local > requirements.txt
    ```

* Create Procfile (noting the capital "P"). Inside the file add:

    ```
    release: python manage.py makemigrations && python manage.py migrate
    web: gunicorn drf_api.wsgi 
    ```

* In the settings.py, update the value of "ALLOWED_HOSTS" to:

    ```
    ALLOWED_HOSTS = ['localhost', '<your_app_name>.herokuapp.com']
    ```

* In the command terminal, install CORS, by typing: 
    
    ```
    pip install django-cors-headers
    ```

* Add corsheaders to INSTALLED_APPS:

    ```
    INSTALLED_APPS = [
    ...
    'dj_rest_auth.registration',
    'corsheaders',
    ...
    ]
    ```

* Add to MIDDLEWARE list: (place at the top of the MIDDLEWARE list)

    ```
    MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
    ]
    ```

* Set the ALLOWED_ORIGINS for the network requests made to the server: (placed under MIDDLEWARE_LIST)

    ```
    if 'CLIENT_ORIGIN' in os.environ:
        CORS_ALLOWED_ORIGINS = [
            os.environ.get('CLIENT_ORIGIN')
    ]
    else:
        CORS_ALLOWED_ORIGIN_REGEXES = [
            r"^https://.*\.gitpod\.io$",
    ]
    ```

* Enable sending cookies in cross-origin requests so that users can get authentication functionality:

    ```
    else:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https://.*\.gitpod\.io$",
    ]
    CORS_ALLOW_CREDENTIALS = True
    ```

*   Allow Cookies and allow front end app and API be deployed to different platforms:
    ```
    JWT_AUTH_COOKIE = 'my-app-auth'
    JWT_AUTH_REFRESH_COOKE = 'my-refresh-token'
    JWT_AUTH_SAMESITE = 'None'
    ```

* Remove the value for SECRET_KEY and replace with the following code to use an environment variable instead:

    **SECURITY WARNING: keep the secret key used in production secret!**

    ```
    SECRET_KEY = os.getenv('SECRET_KEY')
    ```

* Set a NEW value for your SECRET_KEY environment variable in env.py, do NOT use the same one that has been published to GitHub in your commits:

    ```
    os.environ.setdefault("SECRET_KEY", "CreateANEWRandomValueHere")
    ```

* Replace the DEBUG Setting to be only true in Dev and False in Prod Modes:

    ```
    DEBUG = 'DEV' in os.environ
    ```

* Comment DEV back in env.py

* Ensure the project requirements.txt file is up to date:

    ```
    pip freeze --local > requirements.txt
    ```

* Add, commit and push your code to GitHub

## Heroku deployment

* In Heroku - Add your config vars i.e. copy and paste values from env.py into Heroku Config Vars, and add the DISABLE_COLLECTSTATIC var:

    ***CLOUDINARY_URL***

    ***SECRET_KEY***

    ***DISABLE_COLLECTSTATIC = 1***

* In the deploy tab:

    * Select the Deployment Method (GitHub), select the project repository name from Github, and connect. Next in the Manual deploy section, choose the Master Branch, then click Deploy Branch.

* Once complete, click "Open App" to view