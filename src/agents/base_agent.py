from core.llm_client import LLMClient

class BaseAgent:
    """
    所有Agent的基类（复用Hello-Agents的核心范式）
    核心流程：perceive（感知）→ think（决策）→ act（执行）
    """
    def __init__(self, name, llm_type="openai"):
        self.name = name  # Agent名称
        self.llm_client = LLMClient(llm_type=llm_type)  # 统一LLM客户端
        self.input_data = None  # 存储感知到的输入数据
        self.action = None      # 存储决策后的行动
        self.result = None      # 存储执行后的结果

    def perceive(self, input_data):
        """感知：接收并预处理输入数据（子类必须实现）"""
        raise NotImplementedError(f"{self.name}必须实现perceive方法")

    def think(self):
        """决策：根据输入数据规划行动（子类必须实现）"""
        raise NotImplementedError(f"{self.name}必须实现think方法")

    def act(self):
        """执行：执行决策并返回结果（子类必须实现）"""
        raise NotImplementedError(f"{self.name}必须实现act方法")

    def run(self):
        """Agent核心执行方法（子类需重写）"""
        raise NotImplementedError("子类必须实现run()方法")