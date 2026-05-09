# 对照实验脚本：交互式输入 + 无引用 + 无记忆独立生成
from agents.base_agent import BaseAgent

class CompareExperiment(BaseAgent):
    def __init__(self):
        super().__init__(name="CompareExp", llm_type="qwen")

    def generate_by_keyword(self, keyword):
        prompt = f"""
请基于关键词 "{keyword}" 生成一份专业的文献分析报告。
报告结构：
1. Background
2. Related Work
3. Research Trends
4. Research Gaps
5. Research Directions

要求：
- 全文使用标准学术英文
- 字数控制在 800–1000 词
- 内容严谨，不编造信息
- 重要内容引用标记 [1][2]

"""
        return self.llm_client.generate(prompt, is_english=True)

    def generate_by_pdf(self, pdf_path):
        prompt = f"""
请根据路径 "{pdf_path}" 的学术论文内容，生成一篇单篇论文分析报告。
报告结构：
1. Research Overview
2. Methods and Key Findings
3. Limitations and Challenges
4. Future Research Directions

要求：
- 全文使用标准学术英文
- 字数控制在 800-1000 词
- 内容严格依据论文内容
- 不编造信息

"""
        return self.llm_client.generate(prompt, is_english=True)


if __name__ == "__main__":
    exp = CompareExperiment()

    print("===== 对照实验生成 =====")
    print("1 关键词生成")
    print("2 PDF 文件生成")

    choice = input("请选择输入方式（1 或 2）：").strip()

    if choice == "1":
        kw = input("请输入关键词：").strip()
        print("\n正在生成报告...\n")
        res = exp.generate_by_keyword(kw)
        print("=" * 50)
        print(res)

    elif choice == "2":
        path = input("请输入 PDF 文件路径：").strip()
        print("\n正在生成报告...\n")
        res = exp.generate_by_pdf(path)
        print("=" * 50)
        print(res)

    else:
        print("输入无效，请输入 1 或 2")