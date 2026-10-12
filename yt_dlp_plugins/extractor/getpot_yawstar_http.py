import json
import urllib.request
import urllib.error

from yt_dlp.extractor.youtube.pot.provider import POTProvider


class YawStarHTTPProvider(POTProvider):
    """
    YawStar HTTP PO Token Provider for yt-dlp.
    Communicates with the Go-based HTTP server to generate and supply PO Tokens.
    """
    name = 'yawstarhttp'
    SUPPORTED_CONTEXTS = {'gvs', 'player', 'subs'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Extract base_url from extractor arguments, default to localhost:8080
        self.base_url = self._get_extractor_arg('base_url') or 'http://127.0.0.1:8080'
        self.base_url = self.base_url.rstrip('/')

    def get_pot(self, context: str, client: str = None) -> str:
        url = f"{self.base_url}/get_pot"
        payload = {
            'context': context,
            'client': client,
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST',
            )
            # Timeout ကို ၂ စက္ကန့်လောက်ပဲထားလို့ Server မရှိရင် အကြာကြီးမစောင့်ဘဲကျော်သွားပါမယ်
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return data.get('po_token')
        except (urllib.error.URLError, ConnectionRefusedError, TimeoutError):
            # Server မရှိရင် သို့မဟုတ် ချိတ်လို့မရရင် Warning တစ်ကြိမ်လောက်ပြပြီး ကျော်သွားမယ် (Silent ဖြစ်စေချင်ရင် pass ပြောင်း)
            return None
        except Exception as e:
            return None

        return None