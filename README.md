# Medic to Medic Student Manager Server

## Running

To run the app, use `pip` to install all requerements listed in `requirements.txt`, and then use Python to run `run.py`. This app is made for Python 3.

## Setting users

To set users, make use of the `ADMIN_EMAIL` environment variable to set an email that will always have admin permissions on the server. To add other users and set permissions, run the app and go to the `/users` endpoint. From here you will be able to add and remove users and set permitions, although the user set in `ADMIN_EMAIL` will not retain any changes.

## Debuging

When debugging, the application can be set to debug mode by setting the environment variable `FLASK_DEBUG` to `1`. Setting this variable will both cause the application to log all requests, and disable authorization checks on endpoints.

## Environment Variables

| Variable Name | Usage |
| --- | --- |
| `FN_AUTH_REDIRECT_URI` | The URI that a user is returned to after logging in with their Google account. Must be configured to be accepted by google's OAuth API. |
| `FN_BASE_URI` | The root URI the server operates on, used in redirect responses. |
| `FN_CLIENT_ID` | Client ID used by Google OAuth. |
| `FN_CLIENT_SECRET` | Client secret used by Google OAuth. |
| `AWS_ACCESS_KEY_ID` | Amazon AWS S3 access key ID. |
| `AWS_SECRET_ACCESS_KEY` | Amazon AWS S3 secret access key. |
| `S3_BUCKET` | Name of the S3 bucket that uploaded files will be stored in. |
| `S3_REGION` | The region name of the server that the S3 bucket is stored on. |
| `ADMIN_EMAIL` | The email address of an admin. See [Setting users](#Setting-users). |
| `DATABASE_URL` | URL of the server's database (known to be compatible with PostgreSQL and SQLite). |
| `FLASK_DEBUG` | Wether or not the application is currently in debug mode. Should be either 0 or 1. |
| `SECRET_KEY` | Secret key used by flask for encryption. |
