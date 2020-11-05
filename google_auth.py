import functools
import os

import flask

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

from medic2medic.models.user import UserModel

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

AUTHORIZATION_SCOPE ='openid email profile'

AUTH_REDIRECT_URI = os.environ.get("FN_AUTH_REDIRECT_URI", default=False)
BASE_URI = os.environ.get("FN_BASE_URI", default=False)
CLIENT_ID = os.environ.get("FN_CLIENT_ID", default=False)
CLIENT_SECRET = os.environ.get("FN_CLIENT_SECRET", default=False)
DEBUG = int(os.environ.get("FLASK_DEBUG", default=0))

AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'

app = flask.Blueprint('google_auth', __name__)

def CheckLogin(passUserInfo=False, redirect=False, requiredPermissions=('Read','Write')):
    """ Method decorator, adds a login check for a flask route.

    Must be used on the line following `@app.route()`, otherwise the route won't register.

    Parameters
    ----------
    `passUserInfo` : `bool` | `str`
        When method is called, pass the value of get_user_info() as the last arg.
        If the value is a string, pass the value as the corrisponding kwarg.
    `redirect` : `bool`
        If the user is not logged in, redirect them to the login page.
    `requiredPermission` : `str`
        The required permission for the user to access this resorce. If None, all permission types acepted.
    """
    def decorator(foo):
        def wrapper(*args, **kwargs):
            if is_logged_in():
                email = get_user_info().get('email')
                if requiredPermissions is None or is_authorized(email, requiredPermissions):
                    if passUserInfo:
                        if type(passUserInfo) is str:
                            kwargs[passUserInfo] = get_user_info()
                        else:
                            args = (*args, get_user_info())
                    return foo(*args, **kwargs)
                else:
                    return flask.Response(status=401, response='User does not have required permission.')
            elif redirect:
                return flask.redirect('/google/login')
            else:
                return flask.Response(status=401, response='User is not logged in.')
        # Avoid view name conflicts in app.add_url_rule
        wrapper.__name__ = foo.__name__
        if DEBUG:
            return foo
        else:
            return wrapper
    return decorator

def is_logged_in():
    return True if AUTH_TOKEN_KEY in flask.session else False

def is_authorized(email, permissions):
    user = UserModel.query.filter(UserModel.email == email).all()
    if user:
        upermissions = eval(user[0].permissions)
        if sum((1 for p in permissions if p in upermissions)) is len(permissions):
            return True
    return False

def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens = flask.session[AUTH_TOKEN_KEY]
    
    return google.oauth2.credentials.Credentials(
                oauth2_tokens['access_token'],
                refresh_token=oauth2_tokens['refresh_token'],
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                token_uri=ACCESS_TOKEN_URI)

def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
                        'oauth2', 'v2',
                        credentials=credentials, cache_discovery=False)

    return oauth2_client.userinfo().get().execute()

def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache_impl, view)

@app.route('/google/login')
@no_cache
def login():
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            redirect_uri=AUTH_REDIRECT_URI)
  
    uri, state = session.authorization_url(AUTHORIZATION_URL)

    flask.session[AUTH_STATE_KEY] = state
    flask.session.permanent = True

    return flask.redirect(uri, code=302)

@app.route('/google/auth')
@no_cache
def google_auth_redirect():
    req_state = flask.request.args.get('state', default=None, type=None)

    if req_state != flask.session[AUTH_STATE_KEY]:
        response = flask.make_response('Invalid state parameter', 401)
        return response
    
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            state=flask.session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(
                        ACCESS_TOKEN_URI,            
                        authorization_response=flask.request.url)

    flask.session[AUTH_TOKEN_KEY] = oauth2_tokens

    return flask.redirect(BASE_URI, code=302)

@app.route('/google/logout')
@no_cache
def logout():
    flask.session.pop(AUTH_TOKEN_KEY, None)
    flask.session.pop(AUTH_STATE_KEY, None)

    return flask.redirect(BASE_URI, code=302)
