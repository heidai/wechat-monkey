import os
import sae
import web

from handle import Handle
from cron import RefreshAccessToken

sae.add_vendor_dir('vendor')


urls = (
    '/', 'Handle',
    '/cron/accesstoken', 'RefreshAccessToken'
)
app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)
