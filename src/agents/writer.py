from agents.base_agent import BaseAgent

class WriterAgent(BaseAgent):
    """报告生成Agent（输出英文报告）"""
    def __init__(self):
        super().__init__(name="WriterAgent", llm_type="qwen")
        # 自定义写作Prompt
        self.writing_prompt = """
        请基于以上文献分析结果，生成一份专业的《文献分析与选题建议报告》（Literature Analysis and Research Proposal Report）：
        1. 报告结构：研究背景（Background）、相关工作综述（Related Work）、研究趋势（Research Trends）、研究空白（Research Gaps）、选题建议（Research Directions）；
        2. 每个部分内容详实，逻辑清晰；
        3. 所有内容必须使用英文，语言符合学术规范；
        4. 报告总字数控制在800-1000词。

        【重要规则请遵守】
        1. 所有内容必须依据提供的文献内容和分析内容，不能虚构信息。
        2. 重要结论、观点、数据必须来自原文，不可自行扩展不存在的内容。
        文献分析结果：
        {analysis_result}
        """

    def write(self, papers, analysis_result):
        """
        生成英文报告
        :param papers: 检索到的文献列表
        :param analysis_result: 分析结果
        :return: 英文报告
        """
        # 填充写作Prompt
        prompt = self.writing_prompt.format(analysis_result=analysis_result)
        print(f"💡 写作Prompt（关键部分）：{prompt[:100]}...")
        
        # 调用LLM生成报告（强制英文）
        report = self.llm_client.generate(prompt, is_english=True)
        
        return report