from agents.base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    """任务规划Agent（定义plan方法+自定义Prompt）"""
    def __init__(self):
        # 初始化父类，指定LLM类型
        super().__init__(name="PlannerAgent", llm_type="qwen")
        # 自定义规划Prompt
        self.plan_prompt = """
        请为「carbon policy」相关的文献分析任务规划执行流程：
        1. 流程需包含4个核心步骤，逻辑清晰；
        2. 每个步骤说明具体任务和目标；
        3. 输出简洁明了，不超过100字；
        4. 所有输出使用中文（仅用于任务规划）。
        """

    def plan(self):
        """
        生成任务规划
        :return: 中文任务规划结果
        """
        # 调用LLM生成规划（中文输出）
        plan_result = self.llm_client.generate(self.plan_prompt, temperature=0.1)
        
        # 若LLM返回空，使用默认规划
        if not plan_result:
            plan_result = "流程：检索相关文献 → 分析文献核心内容 → 总结研究趋势与空白 → 生成英文分析报告"
        
        return plan_result