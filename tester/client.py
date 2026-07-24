import time
import requests

class ApiClient:
    def __init__(self, base_url, timeout=2, max_retries=1):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    def get(self, path="", params=None):
        url = self.base_url + path
        attempt = 0
        last_exc = None
        while attempt <= self.max_retries:
            start = time.monotonic()
            try:
                resp = requests.get(url, params=params, timeout=self.timeout)
                latency_ms = round((time.monotonic() - start) * 1000, 2)
                if resp.status_code == 429 and attempt < self.max_retries:
                    time.sleep(1)  # backoff simple avant retry
                    attempt += 1
                    continue
                return {
                    "ok": True,
                    "status_code": resp.status_code,
                    "headers": resp.headers,
                    "text": resp.text,
                    "latency_ms": latency_ms,
                }
            except requests.exceptions.RequestException as e:
                last_exc = e
                attempt += 1
        return {"ok": False, "error": str(last_exc), "latency_ms": None}
