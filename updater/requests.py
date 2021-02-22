import requests
import logging
import sys

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


LOG = logging.getLogger(__name__)


def _retry_session(retries=5, backoff_factor=0.1, status_forcelist=(500, 502, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        method_whitelist=frozenset(['GET', 'POST']),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def send_request(method, url, payload, headers, auth):
    session = _retry_session()
    try:
        r = session.request(method, url, data=payload, headers=headers, auth=auth)
        r.raise_for_status()
        return r
    except requests.RequestException as e:
        LOG.error(e)
        sys.exit(1)
