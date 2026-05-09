import os
from http import HTTPStatus
import dashscope
from dashscope import Generation
from dotenv import load_dotenv

class LLMClient:
    """Qwen2.5 远程API调用（支持中英文生成）"""
    def __init__(self, llm_type="qwen"):
        self.llm_type = llm_type
        self._init_client()

    def _init_client(self):
        """初始化百炼API（强制读取.env）"""
        # 强制指定.env路径
        PROJECT_ROOT = "/Users/iriscandy/Desktop/literature_agent"
        env_path = os.path.join(PROJECT_ROOT, ".env")
        load_dotenv(dotenv_path=env_path)
        
        # 读取密钥
        self.api_key = os.getenv("QWEN_API_KEY")
        print(f"📝 从.env读取的API-KEY：{self.api_key[:8]}..." if self.api_key else "❌ 未读到.env中的密钥")
        
        # 校验密钥
        if not self.api_key or not (self.api_key.startswith("sk-") or self.api_key.startswith("ms-")):
            raise RuntimeError(
                f"❌ .env文件配置错误\n"
                f"检查：1. .env路径是否为 {env_path}\n"
                f"      2. QWEN_API_KEY是否为有效百炼密钥（sk-/ms-开头）"
            )
        
        dashscope.api_key = self.api_key
        self.model = os.getenv("QWEN_MODEL", "qwen-turbo")

    def generate(self, prompt, temperature=0.1, is_english=False):
        """
        调用百炼API生成文本
        :param prompt: 提示词
        :param temperature: 随机性
        :param is_english: 是否强制输出英文
        :return: 生成结果
        """
        # 英文输出强制提示
        if is_english:
            prompt = f"{prompt}\n\n重要要求：所有输出内容必须使用英文，禁止使用任何中文。"
        
        try:
            response = Generation.call(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=2000,
                result_format='message',
                stream=False
            )
            
            if response.status_code != HTTPStatus.OK:
                raise RuntimeError(f"Qwen2.5调用失败：{response.code} - {response.message}")
            
            return response.output.choices[0].message.content.strip()

        except Exception as e:
            raise RuntimeError(f"LLM调用失败：Qwen2.5调用失败：{str(e)}")