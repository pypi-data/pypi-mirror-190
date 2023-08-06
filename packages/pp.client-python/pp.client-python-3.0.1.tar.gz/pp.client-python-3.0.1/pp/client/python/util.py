################################################################
# pp.client - Produce & Publish Python Client
# (C) 2013, ZOPYX Ltd, Tuebingen, Germany
################################################################

try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse, urlunparse


def mask_url(url):
    parts = list(urlparse(url))
    netloc = parts[1]
    if "@" in netloc:
        user_pw, host_port = netloc.split("@")
        username, password = user_pw.split(":")
        netloc = f"{username}:***@{host_port}"
        parts[1] = netloc
    return urlunparse(parts)
