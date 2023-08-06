# -----------------------------------------------------------------------------
# REQUIRED VALUES
# -----------------------------------------------------------------------------
# Environment choices: {DEV, TEST, PROD}
ENVIRONMENT = 'DEV'

# SECURITY WARNING: Change this and keep it a secret in production!
SECRET_KEY = '8fq8(uri7ioykvrgvz)99jo2zdc$-1!e4o2jp#tjxq34atd3&)'

# Name of machine running the application
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Debug mode (probably only true in DEV)
DEBUG = True

# SSO URL
CAS_SERVER_URL = 'https://sso-stage.oit.pdx.edu/idp/profile/cas/login'

# `````````````````
# FINTI
# `````````````````
# If you have the "PSU Key" file, Finti will be configured to access the test server.
# You MUST provide real Finti URL and token for access to your APIs
# Finti URLs (for reference)
# -  http://localhost:8888
# -  https://ws-test.oit.pdx.edu
# -  https://ws.oit.pdx.edu

# REQUIRED: Finti URL and Token (uncomment these):
FINTI_TOKEN = '2144402c-586e-44fc-bd0c-62b31e98394d'
FINTI_URL = 'http://localhost:8888'


# -----------------------------------------------------------------------------
# OPTIONAL VALUES
# -----------------------------------------------------------------------------

# You may want to disable elevated developer access while running locally
# ELEVATE_DEVELOPER_ACCESS = False

# You may want to extend session expiration during local development
# SESSION_COOKIE_AGE = 4 * 60 * 60  # 4 hours

