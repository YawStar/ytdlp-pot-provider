from __future__ import annotations

import functools
import json
import time

from yt_dlp.extractor.youtube.pot.provider import (
    PoTokenProvider,
    PoTokenProviderError,
    PoTokenProviderRejectedRequest,
    PoTokenRequest,
    PoTokenResponse,
    PoTokenContext,
    register_preference,
    register_provider,
)
from yt_dlp.extractor.youtube.pot.utils import WEBPO_CLIENTS, get_webpo_content_binding
from yt_dlp.networking.common import Request
from yt_dlp.networking.exceptions import HTTPError, TransportError
from yt_dlp.utils import js_to_json
from yt_dlp.utils.traversal import traverse_obj

__version__ = '0.1.0'

class YawStarPTPBase(PoTokenProvider):
    PROVIDER_VERSION = __version__
    _SUPPORTED_CLIENTS = WEBPO_CLIENTS
    _SUPPORTED_CONTEXTS = (
        PoTokenContext.GVS,
        PoTokenContext.PLAYER,
        PoTokenContext.SUBS,
    )
    _GETPOT_TIMEOUT = 2.0

    def _get_attestation(self, webpage: str | None):
        if not webpage:
            return None
        raw_cd = (
            traverse_obj(
                self.ie._search_regex(
                    r'''(?sx)window\s*\.\s*ytAtN\s*\(\s*
                        (?P<js>\{.+?}\s*)
                    \s*\)\s*;''', webpage, 'ytAtP challenge', default=None),
                ({js_to_json}, {json.loads}, 'R'))
            or traverse_obj(
                self.ie._search_regex(
                    r'''(?sx)window\.ytAtR\s*=\s*(?P<raw_cd>(?P<q>['"])
                        (?:
                            \\.|
                            (?!(?P=q)).
                        )*
                    (?P=q))\s*;''', webpage, 'ytAtR challenge', default=None),
                ({js_to_json}, {json.loads})))

        if att_txt := traverse_obj(raw_cd, ({json.loads}, 'bgChallenge')):
            return att_txt
        return None


@register_provider
class YawStarHTTPPTP(YawStarPTPBase):
    PROVIDER_NAME = 'yawstar:http'
    DEFAULT_BASE_URL = 'http://127.0.0.1:8080'  # Go Server ရဲ့ Port 8080 ကို ချိတ်ရန်
    _GET_SERVER_VSN_TIMEOUT = 2.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_server_check = 0
        self._server_available = None

    @functools.cached_property
    def _base_url(self):
        base_url = self._configuration_arg('base_url', default=[None])[0]
        if base_url:
            return base_url
        return self.DEFAULT_BASE_URL

    def is_available(self):
        # Go Server ပွင့်နေခြင်း ရှိမရှိ အမြန်စစ်ဆေးမည် (မပွင့်ထားပါက False ပြန်ပေးပြီး ဤ Provider ကို ကျော်သွားမည်)
        if self._last_server_check + 30 > time.time() and self._server_available is not None:
            return self._server_available

        self._server_available = False
        try:
            req = Request(f'{self._base_url}/version', extensions={'timeout': self._GET_SERVER_VSN_TIMEOUT}, proxies={'all': None})
            with self._request_webpage(req, note=False) as res:
                if res.status == 200:
                    self._server_available = True
        except Exception:
            self._server_available = False
        finally:
            self._last_server_check = time.time()

        return self._server_available

    def _real_request_pot(
        self,
        request: PoTokenRequest,
    ) -> PoTokenResponse:
        challenge = self._get_attestation(request.video_webpage)

        try:
            # Go Server ဆီသို့ POST Request ဖြင့် PO Token လှမ်းတောင်း
            response = self._request_webpage(
                request=Request(
                    f'{self._base_url}/get_pot', data=json.dumps({
                        'bypass_cache': request.bypass_cache,
                        'challenge': challenge,
                        'content_binding': get_webpo_content_binding(request)[0],
                        'disable_tls_verification': not request.request_verify_tls,
                        'proxy': request.request_proxy,
                        'innertube_context': request.innertube_context,
                        'source_address': request.request_source_address,
                    }).encode(), headers={'Content-Type': 'application/json'},
                    extensions={'timeout': self._GETPOT_TIMEOUT}, proxies={'all': None}),
                note=f'Generating a {request.context.value} PO Token via YawStar Go server',
            )
        except Exception as e:
            raise PoTokenProviderError(f'Error reaching YawStar server: {e!r}') from e

        try:
            response_json = json.load(response)
        except Exception as e:
            raise PoTokenProviderError(f'Error parsing response JSON: {e!r}') from e

        if not isinstance(response_json, dict) or 'po_token' not in response_json:
            raise PoTokenProviderError('Server did not respond with a po_token')

        return PoTokenResponse(po_token=response_json['po_token'])


@register_preference(YawStarHTTPPTP)
def yawstar_HTTP_getpot_preference(provider, request):
    return 150


__all__ = [YawStarHTTPPTP.__name__, yawstar_HTTP_getpot_preference.__name__]