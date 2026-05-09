# Multi-Agent Based Academic Literature Analysis and Topic Selection Recommendation System

## Project Introduction
This project designs and implements a literature analysis system based on a multi-agent collaborative framework. The whole research workflow is divided into five independent and functional agents: Planner Agent, Retriever Agent, Reader Agent, Analyst Agent and Writer Agent. Instead of relying on a single large language model to complete all tasks, each agent undertakes a specific module to improve system modularity, controllability and scalability.

The system supports two working modes: keyword-oriented academic literature retrieval and local PDF in-depth reading and analysis. It can automatically retrieve academic literature from arXiv and Semantic Scholar, extract core content from PDF files, summarize research trends, analyze existing research gaps, and finally generate standard academic literature reviews and feasible topic selection suggestions. Strict prompt constraints are adopted in all agents to ensure all generated content is based on real literature text, with standard reference numbers, effective suppression of LLM hallucination, and improved academic credibility and factual traceability.

## Main Features
- Automatic user intention recognition and adaptive workflow scheduling
- Integration with arXiv and Semantic Scholar API for latest literature retrieval with 3-year time filtering
- Long-text PDF parsing and structured academic information extraction
- Multi-agent collaborative analysis for research trend summary and research gap mining
- Standardized academic report generation with accurate citation marking
- Engineering-level prompt constraints to reduce model hallucination
- Good modularity, controllability and expandability

## Environment Setup
Fill in your LLM API Key, model endpoint, and model name in the `.env` file.

   
## How to Run
```bash
pip install -r requirements.txt
python main.py
