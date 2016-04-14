"""
Configuration file for settings
"""

SECRET_KEY = '<SECRET KEY>'

ALLOWED_HOSTS = ['*']

DB_NAME = 'idc_profile'

DB_USERNAME = 'idc_profile'

DB_PASSWORD = 'idc_profile'

DB_HOST_NAME = 'localhost'

DB_PORT = '5432'

ADMINS_EMAIL_LIST = [
    # ('Name', 'email@example.com'),
]

CLIENT_SECRET = 'CLIENT_SECRET'

CLIENT_ID = 'CLIENT_ID'

OAUTH_BASE_URL = 'https://gymkhana.iitb.ac.in/sso/'

MINIMUM_SCOPES = ['basic', 'profile', 'ldap']

DEFAULT_REDIRECT_URI = ''

DEFAULT_FIELDS = ['id']
