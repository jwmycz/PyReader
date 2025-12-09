from utils.retry import *
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
}
class HttpRule:
    def __init__(self, rule=None,proxy=None):
        self.client=httpx.AsyncClient(
            http2=True,
            proxy=proxy,  # type: ignore[arg-type]
            timeout=httpx.Timeout(120.0),

        )
        self.rule=rule

    @async_retry(retries=3, backoff=2)
    async def get(self, url, headers=None):
        if headers is None:
            headers = headers
        response = await self.client.get(url, headers=headers)
        response.raise_for_status()
        return response

    @async_retry(retries=3, backoff=2)
    async def post(self, url, headers=None, data=None, json=None):
        if headers is None:
            headers = headers
        response = await self.client.post(url,headers = headers, data=data, json=json)
        response.raise_for_status()
        return response




