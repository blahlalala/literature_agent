from agents.planner import PlannerAgent
from agents.retriever import RetrieverAgent
from agents.analyst import AnalystAgent
from agents.writer import WriterAgent
from agents.reader import ReaderAgent  # 复用原有ReaderAgent

class LiteratureAgentCoordinator:
    """多智能体协调器（增量扩展PDF流程，不改动关键词流程）"""
    def __init__(self):
        # 原有Agent保留，仅新增ReaderAgent
        self.planner = PlannerAgent()
        self.retriever = RetrieverAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()
        self.reader = ReaderAgent()  # 复用原有ReaderAgent

    # 原有关键词流程（完全保留，不改动）
    def run_keyword(self, query):
        print("\n【1/4】PlannerAgent：开始规划任务流程...")
        self.planner.plan_prompt = self.planner.plan_prompt.replace("carbon policy", query)
        plan = self.planner.plan()
        print(f"📋 PlannerAgent输出：{plan}")
        print("【1/4】PlannerAgent：执行计划 ✅")
        
        print("\n【2/4】RetrieverAgent：开始执行核心任务...")
        papers = self.retriever.retrieve(query)
        print(f"【2/4】RetrieverAgent：检索完成 ✅ 共找到{len(papers)}篇相关文献")
        
        print("\n【3/4】AnalystAgent：开始分析文献数据...")
        self.analyst.analysis_prompt = self.analyst.analysis_prompt.replace("AI Agent", query)
        analysis_result = self.analyst.analyze(papers)
        print("【3/4】AnalystAgent：分析完成 ✅")
        
        print("\n【4/4】WriterAgent：开始生成学术报告...")
        report = self.writer.write(papers, analysis_result)
        print("【4/4】WriterAgent：报告生成完成 ✅")
        
        return report

    # 新增PDF流程（复用ReaderAgent，不影响原有逻辑）
    def run_pdf(self, pdf_path):
        """PDF分析流程：复用ReaderAgent提取核心内容"""
        # 1. 规划阶段（仅修改Prompt，不改动逻辑）
        print("\n【1/4】PlannerAgent：开始规划PDF分析流程...")
        self.planner.plan_prompt = """
        请为PDF学术论文分析任务规划执行流程：
    1. 解析PDF文本，提取摘要、结论、结果、未来工作等核心章节；
    2. 结构化整理论文关键信息；
    3. 分析研究内容、创新点与不足；
    4. 生成专业学术分析报告。
    要求：步骤清晰，100字左右，中文输出。
        """
        plan = self.planner.plan()
        print(f"📋 PlannerAgent输出：{plan}")
        print("【1/4】PlannerAgent：执行计划 ✅")
        
        # 2. PDF提取阶段（复用ReaderAgent，替代原有RetrieverAgent）
        print("\n【2/4】ReaderAgent：开始提取PDF核心内容...")
        pdf_content, extract_details = self.reader.read_pdf_core_content(pdf_path)
        # 输出提取明细（可视化）
        print("📊 PDF核心内容提取结果：")
        print("\n".join(extract_details))
        print("【2/4】ReaderAgent：提取完成 ✅")
        
        # 3. 分析阶段（复用原有AnalystAgent，无需改动）
        print("\n【3/4】AnalystAgent：开始分析PDF核心内容...")
        self.analyst.analysis_prompt = """
        请分析这篇单篇学术论文：
        1. 总结研究目的与核心内容
        2. 说明研究方法与实验结果
        3. 指出创新点与不足之处
        4. 总结结论与未来工作
        论文内容：
        {papers}

        输出要求：
        - 分点清晰
        - 简洁专业
        - 全部使用英文
        """
        analysis_result = self.analyst.analyze([pdf_content])  # 包装为列表，适配原有逻辑
        print("【3/4】AnalystAgent：分析完成 ✅")
        
        # 4. 写作阶段（复用原有WriterAgent，无需改动）
        print("\n【4/4】WriterAgent：开始生成学术报告...")
        report = self.writer.write([pdf_content], analysis_result)
        print("【4/4】WriterAgent：报告生成完成 ✅")
        
        return report