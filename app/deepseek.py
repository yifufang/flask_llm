import httpx

class Deepseek_llm():
    """
    Deepseek LLM的简易封装类, 用于与Deepseek API进行交互和对AI回答的内容进行处理
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=60.0)

    async def get_response(self, content, memory, settings, intents, assistant="请根据用户的提问进行回答"):
        """
        调用DeepSeeker API获取AI的回答
        """
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个育儿助手\n"+ settings + memory},
                {"role": "assistant", "content": assistant },
                {"role": "user", "content": f"[Intent:{intents}]" + content},
            ],
            "stream": False,
        }
        response = await self.client.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            res = response.json()["choices"][0]["message"]["content"]
        else:
            res = None
        return res

    def close(self):
        """
        关闭HTTP连接
        """
        self.client.aclose()
    
