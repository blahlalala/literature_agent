import os
import re
import pdfplumber
from agents.base_agent import BaseAgent

class ReaderAgent(BaseAgent):
    """PDF阅读Agent：仅提取abstract/keywords/future work核心内容（复用原有类）"""
    def __init__(self):
        super().__init__(name="ReaderAgent", llm_type="qwen")
        # 【仅修改这里】增强正则，适配更多论文章节标题
        self.extract_patterns = {
            "abstract": r"(?i)abstract[:\s](.*?)(?:1\.|introduction|keywords|conclusion|results|discussion|$)",
            "keywords": r"(?i)(keywords|key words)[:\s](.*?)(?:abstract|1\.|introduction|results|conclusion|$)",
            "conclusion": r"(?i)(conclusion|conclusions)[:\s](.*?)(?:reference|bibliography|future work|$)",
            "results": r"(?i)(results|results and analysis)[:\s](.*?)(?:discussion|conclusion|future work|$)",
            "discussion": r"(?i)discussion[:\s](.*?)(?:results|conclusion|limitation|$)",
            "limitation": r"(?i)(limitation|limitations|challenge|challenges)[:\s](.*?)(?:discussion|conclusion|future work|reference|$)",
            "future work": r"(?i)(future work|future research|limitation and future work|conclusion and future work)[:\s](.*?)(?:reference|bibliography|$)"
        }

    def read_pdf_core_content(self, pdf_path):
        """
        复用ReaderAgent提取PDF核心内容
        """
        # 1. 基础校验（完全不变）
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在：{pdf_path}")
        if not pdf_path.endswith(".pdf"):
            raise ValueError(f"非PDF文件：{pdf_path}")
        
        # 2. 读取PDF文本（完全不变）
        full_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:20]:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
        
        # 3. 正则提取（仅新增章节，逻辑不变）
        extracted = {"title": os.path.basename(pdf_path)}
        extract_details = []
        for section, pattern in self.extract_patterns.items():
            match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip() if section == "abstract" else match.group(2).strip()
                content = re.sub(r"\s+", " ", content)
                extracted[section] = content
                display_content = content[:100] + "..." if len(content) > 100 else content
                extract_details.append(f"✅ {section.capitalize()}: {display_content}")
            else:
                extracted[section] = ""
                extract_details.append(f"❌ {section.capitalize()}: 未提取到内容")
        
        # 4. 【仅修改这里】优化兜底LLM提示词，支持更多章节
        if not any([extracted["abstract"], extracted["keywords"], extracted["future work"], extracted["conclusion"], extracted["results"], extracted["limitation"]]):
            print("\n⚠️  正则提取效果不足，调用LLM辅助提取...")
            prompt = """
            Extract the following content from the academic paper text.
            If the section does not exist, leave it blank.
            
            Requirements:
            - All output MUST be in English.
            - Strictly follow the output format.
            - Do not add extra explanations.
            
            Text:
            """ + full_text[:2000] + """
            
            Output format:
            Abstract: [content]
            Keywords: [content]
            Results: [content]
            Discussion: [content]
            Conclusion: [content]
            Limitation: [content]
            Future Work: [content]
            """
            
            llm_result = self.llm_client.generate(prompt, is_english=True)
            for line in llm_result.split("\n"):
                if line.startswith("Abstract:"):
                    extracted["abstract"] = line.replace("Abstract:", "").strip()
                elif line.startswith("Keywords:"):
                    extracted["keywords"] = line.replace("Keywords:", "").strip()
                elif line.startswith("Results:"):
                    extracted["results"] = line.replace("Results:", "").strip()
                elif line.startswith("Discussion:"):
                    extracted["discussion"] = line.replace("Discussion:", "").strip()
                elif line.startswith("Conclusion:"):
                    extracted["conclusion"] = line.replace("Conclusion:", "").strip()
                elif line.startswith("Limitation:"):
                    extracted["limitation"] = line.replace("Limitation:", "").strip()
                elif line.startswith("Future Work:"):
                    extracted["future work"] = line.replace("Future Work:", "").strip()
        
        return extracted, extract_details