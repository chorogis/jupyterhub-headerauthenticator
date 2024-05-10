import re

from jupyterhub.auth import LocalAuthenticator
from jupyterhub.handlers.base import BaseHandler
from tornado import web
from traitlets import Bool, Unicode


class HeaderLoginHandler(BaseHandler):
    async def get(self):
        data = self.authenticator.headers_to_user(self.request.headers)
        if data is None:
            raise web.HTTPError(401)

        user = await self.login_user(data)

        if user:
            u = self.authenticator.redirect_url
            if u:
                self.redirect(u)
            self.redirect(self.get_next_url(user))
        else:
            raise web.HTTPError(401)


class HeaderAuthenticator(LocalAuthenticator):
    create_system_users = Bool(True).tag(config=True)
    header_name = Unicode().tag(config=True)
    header_pattern = Unicode().tag(config=True)
    redirect_url = Unicode().tag(config=True)
    _re = None

    def headers_to_user(self, headers):
        username = headers.get(self.header_name, "")
        if self.header_pattern is not None:
            if self._re is None:
                self._re = re.compile(self.header_pattern)
            m = self._re.search(username)
            if m:
                username = m.group(1)
        return dict(username=username)

    def get_handlers(self, app):
        return [
            (r"/login", HeaderLoginHandler),
        ]

    async def authenticate(self, handler, data):
        return data.get("username", "")
