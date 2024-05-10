# jupyterhub-headerauthenticator

## Installation

```sh
pip install jupyterhub-headerauthenticator
```

## Configuration examples

Configurable within `jupyterhub_config.py`.

```python
c.JupyterHub.authenticator_class = "header"
c.HeaderAuthenticator.header_name = "X-USER"
```

Here's an example of using it behind an mTLS-enabled reverse proxy.

```python
c.JupyterHub.authenticator_class = "header"
c.HeaderAuthenticator.header_name = "X-TLS-CLIENT-SUBJECT"
# Group 1 from the matched pattern becomes the username
c.HeaderAuthenticator.header_pattern = "^CN=([^,]+)"
```

You can set the redirect_url as follows:

```
c.HeaderAuthenticator.redirect_url = "/services/shared-jupyterlab/"
```

If you do not wish to create system users, set `create_system_users` to False.

```
c.HeaderAuthenticator.create_system_users = False
```
