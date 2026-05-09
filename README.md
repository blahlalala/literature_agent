基于多智能体的学术文献分析与选题推荐系统
本项目实现了一个由 5 个智能体（Planner、Retriever、Reader、Analyst、Writer） 协作完成的文献自动分析系统。
系统支持两种输入模式：关键词检索 与 PDF 文献精读，能够自动生成结构化文献综述与研究缺口分析。
主要功能
自动识别输入类型并规划工作流
调用 arXiv / Semantic Scholar 免费 API 获取最新文献
抽取 PDF 文本并进行结构化解析
多智能体协作归纳研究趋势、分析研究空白
生成符合学术规范的报告，抑制大模型幻觉
支持引用标注，保证内容可追溯
技术特点
模块化多智能体架构
严格的 Prompt 约束与事实校验
无付费 API，完全开源可用
支持近 3 年文献时间过滤
English
Multi-Agent Based Academic Literature Analysis & Topic Recommendation System
This project implements an automatic literature analysis system powered by five cooperative agents: Planner, Retriever, Reader, Analyst, and Writer.
The system supports two input modes:
Keyword-based literature retrieval and PDF document deep reading, and can generate structured literature reviews with research gap analysis.
Features
Automatic input type detection and workflow planning
Free academic API integration (arXiv, Semantic Scholar)
PDF text extraction and structured parsing
Multi-agent collaboration for trend analysis and research gap identification
Hallucination suppression with strict prompt constraints
Traceable output with citation support
Characteristics
Modular multi-agent architecture
Fact-checking and strong constraint mechanisms
No paid APIs, fully open-source
Time filtering for recent 3-year literature
