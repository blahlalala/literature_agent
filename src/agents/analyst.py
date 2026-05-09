from agents.base_agent import BaseAgent

class AnalystAgent(BaseAgent):
    """文献分析Agent（自定义Prompt+输出明细+英文）"""
    def __init__(self):
        super().__init__(name="AnalystAgent", llm_type="qwen")
        # 自定义分析Prompt（可根据需求修改）
        self.analysis_prompt = """
        请分析以下AI Agent相关文献，完成3项任务：
        1. 总结3-5个核心研究趋势（Research Trends）；
        2. 指出2-3个当前研究空白/不足（Research Gaps）；
        3. 提出3-5个可行的研究选题方向（Research Directions）；
        4. 重点部分必须标注准确的原文引用，格式为[1]、[2]（序号对应文献列表中的序号）；
        文献数据：
        {papers}
        
        输出格式要求：
        - 分3个部分清晰列出，每个部分用项目符号（-）展示；
        - 每个要点简洁明了，不超过2句话；
        - 所有内容必须使用英文。
        """

    def analyze(self, papers):
        """
        分析文献并输出明细
        :param papers: 检索到的文献列表
        :return: 英文分析结果
        """
        # 构建文献文本（纯英文）
        papers_text = ""
        for i, paper in enumerate(papers, 1):
            papers_text += f"{i}. Title: {paper['title']}\n"
            papers_text += f"   Abstract: {paper['abstract'][:200]}...\n\n"
        
        # 填充Prompt
        prompt = self.analysis_prompt.format(papers=papers_text)
        print(f"💡 分析Prompt（关键部分）：{prompt[:100]}...")
        
        # 调用LLM生成分析结果（强制英文）
        analysis_result = self.llm_client.generate(prompt, is_english=True)
        
        # 输出分析明细
        print("📊 文献分析明细：")
        print(analysis_result)
        print("\n" + "-"*50)
        
        return analysis_result