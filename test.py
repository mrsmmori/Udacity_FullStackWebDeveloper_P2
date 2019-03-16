from flask import Flask
from oauth2client.contrib.flask_util import UserOAuth2

app = Flask(__name__)

app.config['GOOGLE_OAUTH2_CLIENT_ID'] = '266875970319-r0so7u4a0qc2409s7t23v1fg4fa8gur5.apps.googleusercontent.com'
app.config['GOOGLE_OAUTH2_CLIENT_SECRET'] = 'w2tdxisx2JkwKiOKg3ImFyRI'

oauth2 = UserOAuth2(app)
# Note that app.route should be the outermost decorator.
@app.route('/needs_credentials')
@oauth2.required
def example():
    # http is authorized with the user's credentials and can be used
    # to make http calls.
    http = oauth2.http()

    # Or, you can access the credentials directly
    credentials = oauth2.credentials
