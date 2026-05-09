import fitz  # PyMuPDF
import os
import requests
import time
from functools import wraps

"""
通用工具函数：包含PDF解析、学术文献检索（arXiv，无严格限流）
适配Qwen2.5文献分析系统，解决Semantic Scholar 429限流问题
"""

# ===================== 重试装饰器（通用） =====================
def retry(max_retries=3, delay=2):
    """
    重试装饰器：请求失败时自动重试（指数退避）
    :param max_retries: 最大重试次数
    :param delay: 基础延迟时间（秒）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_retries - 1:
                        raise e
                    sleep_time = delay * (i + 1)
                    print(f"⚠️  操作失败，{sleep_time}秒后重试第{i+1}次...")
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

# ===================== PDF解析函数 =====================
def parse_pdf(pdf_path: str, max_text_length: int = 2000) -> str:
    """
    解析PDF文件，提取文本并截断（避免LLM上下文超限）
    :param pdf_path: PDF文件绝对路径
    :param max_text_length: 最大文本长度（默认2000字符）
    :return: 提取的文本字符串
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF文件不存在：{pdf_path}")
    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError(f"不是有效的PDF文件：{pdf_path}（后缀需为.pdf）")
    
    # 打开PDF并提取文本
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text().strip()
    doc.close()
    
    # 截断文本（保留核心信息）
    if len(text) > max_text_length:
        text = text[:max_text_length] + "\n\n[注：文本过长，已截断前2000字符]"
    
    return text

# ===================== arXiv文献检索函数（推荐） =====================
@retry(max_retries=3, delay=3)
def search_arxiv(query: str, limit: int = 5) -> list:
    """
    调用arXiv API检索学术文献（无严格限流，国内访问稳定）
    :param query: 检索关键词/研究标题
    :param limit: 返回文献数量（默认5篇）
    :return: 结构化的文献列表
    """
    # arXiv API基础配置
    api_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",  # 全文检索（标题/摘要/作者）
        "max_results": limit,
        "sortBy": "relevance",           # 按相关性排序
        "sortOrder": "descending"        # 降序（最相关在前）
    }

    try:
        # 添加请求延迟，避免触发限流
        time.sleep(1)
        # 发送请求
        response = requests.get(
            api_url,
            params=params,
            timeout=15,
            headers={"User-Agent": "LiteratureAgent/1.0 (Python)"}  # 标识客户端
        )
        response.raise_for_status()  # 抛出HTTP错误（4xx/5xx）

        # 解析XML响应（arXiv返回XML格式）
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.text)
        ns = {"arxiv": "http://www.w3.org/2005/Atom"}  # XML命名空间
        papers = []

        # 提取每篇文献的核心信息
        for entry in root.findall("arxiv:entry", ns)[:limit]:
            # 标题（去除换行符）
            title = entry.find("arxiv:title", ns).text.strip().replace("\n", " ") if entry.find("arxiv:title", ns) is not None else "无标题"
            # 摘要
            abstract = entry.find("arxiv:summary", ns).text.strip().replace("\n", " ") if entry.find("arxiv:summary", ns) is not None else "无摘要"
            # 作者列表
            authors = []
            for author in entry.findall("arxiv:author/arxiv:name", ns):
                authors.append(author.text.strip())
            # 发布年份
            published = entry.find("arxiv:published", ns).text if entry.find("arxiv:published", ns) is not None else ""
            year = published.split("-")[0] if published else "未知年份"
            # 文献URL
            url = entry.find("arxiv:id", ns).text.strip() if entry.find("arxiv:id", ns) is not None else ""

            # 构造结构化文献信息
            papers.append({
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "year": year,
                "url": url,
                "keywords": []  # arXiv无关键词字段，留空
            })

        return papers

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"arXiv API调用失败：{str(e)}\n"
            f"💡 排查：1. 检查网络是否能访问 http://export.arxiv.org\n"
            f"       2. 关键词是否包含特殊字符（建议用英文）"
        )