import arxiv
from agents.base_agent import BaseAgent
from datetime import datetime, timedelta

class RetrieverAgent(BaseAgent):
    """文献检索Agent（输出英文文献明细）"""
    def __init__(self):
        super().__init__(name="RetrieverAgent", llm_type="qwen")

    def retrieve(self, query, limit=5):
        """
        检索arXiv文献并输出明细（优先最新 + 最相关）
        """
        print(f"🔍 检索策略：使用arXiv API检索关键词「{query}」，返回{limit}篇【最新+最相关】文献")
        query_and = " AND ".join(query.split())
        precise_query = f"(title:{query_and}) OR (abstract:{query_and})"
        search = arxiv.Search(
            query=precise_query,
            max_results=limit * 3,
            sort_by=arxiv.SortCriterion.Relevance
        )

        three_years_ago = datetime.now() - timedelta(days=365*3)
        filtered = []

        for result in search.results():
            pub_time = result.published.replace(tzinfo=None)  # ✅ 修复时间报错
            if pub_time >= three_years_ago:
                filtered.append(result)

        filtered = filtered[:limit]

        papers = []
        paper_details = []
        for i, res in enumerate(filtered, 1):
            paper = {
                "title": res.title,
                "authors": [a.name for a in res.authors],
                "abstract": res.summary.strip(),
                "url": res.entry_id
            }
            papers.append(paper)
            paper_details.append(f"{i}. Title: {paper['title']}")
            paper_details.append(f"   Authors: {', '.join(paper['authors'])}")
            paper_details.append(f"   URL: {paper['url']}\n")

        print("📚 检索到的【最新+最相关】文献明细：")
        print("\n".join(paper_details))
        return papers