import requests
from .settings import LOGGER
from typing import Dict
from .exceptions import UnsupportedException, ServiceError


class BaseApi:
    _api_key: str
    _exception_map: Dict[str, Exception]

    def __init__(self, api_key: str, exception_map: Dict[str, Exception]) -> None:
        self._api_key = api_key
        self._exception_map = exception_map
        self.LOGGER = LOGGER

    def _process_response(self, response: requests.Response):
        if 200 <= response.status_code < 300:
            data = response.json()
            payload = data.get('data', None)
            if payload is None:
                raise UnsupportedException('Empty service response')
            return payload
        if 400 <= response.status_code < 500:
            data = response.json()
            message = data.get('message', None)
            details = data.get('details', "No details were provided")
            raise self._exception_map.get(message, UnsupportedException)(details)

        if response.status_code >= 500:
            data = response.json()
            message = data.get('message', None)
            details = data.get('details', "No details were provided")

            raise ServiceError({"message": message, "details": details})

    def _request(self, method, url, **kwargs):
        """Constructs and sends a :class:`Request <Request>`.

        :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
            ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
            or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
            defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
            to add for the file.
        :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How many seconds to wait for the server to send data
            before giving up, as a float, or a :ref:`(connect timeout, read
            timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
                the server's TLS certificate, or a string, in which case it must be a path
                to a CA bundle to use. Defaults to ``True``.
        :param stream: (optional) if ``False``, the response content will be immediately downloaded.
        :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        header_params = kwargs.setdefault('headers', {})

        header_params.update({
            'x-api-key': self._api_key,
            'Content-Type': 'application/json'
        })
        try:
            response = requests.request(method, url, **kwargs)
            return self._process_response(response)
        except requests.exceptions.Timeout as err_timeout:
            self.LOGGER.exception("Timeout Error:", err_timeout)
            raise err_timeout
        except requests.exceptions.HTTPError as err_http:
            self.LOGGER.exception("Http Error:", err_http)
            raise err_http
        except requests.exceptions.ConnectionError as err_connection:
            self.LOGGER.exception("Error Connecting:", err_connection)
            raise err_connection
        except requests.exceptions.RequestException as err:
            SystemExit(err)
