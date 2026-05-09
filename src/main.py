# src/main.py（仅新增PDF输入分支，完善退出逻辑，原有关键词流程完全保留）
import os
import sys
from core.coordinator import LiteratureAgentCoordinator

# 新增PDF路径校验函数（不影响原有逻辑）
def validate_pdf_path(pdf_path):
    if not os.path.isabs(pdf_path):
        pdf_path = os.path.join(os.getcwd(), pdf_path)
    if not os.path.exists(pdf_path):
        print(f"❌ 错误：PDF文件不存在 → {pdf_path}")
        return None
    if not pdf_path.lower().endswith(".pdf"):
        print(f"❌ 错误：文件不是PDF格式 → {pdf_path}")
        return None
    return pdf_path

def main():
    print("="*60)
    print("      多智能体文献分析与选题辅助系统（基于Qwen2.5）")
    print("="*60)
    
    coordinator = LiteratureAgentCoordinator()
    
    while True:
        print("\n请选择输入类型：")
        print("1. 关键词/研究标题（建议用英文）")
        print("2. 本地PDF文件（仅提取abstract/keywords/future work）")
        print("3. 退出系统")
        
        choice = input("输入序号（1/2/3）：").strip()
        
        # 原有关键词流程（完全保留，不改动）
        if choice == "1":
            query = input("\n请输入检索关键词/研究标题（英文）：").strip()
            if not query:
                print("❌ 关键词不能为空！")
                continue
            print("\n🚀 开始执行文献分析（关键词模式）...")
            try:
                report = coordinator.run_keyword(query)
            except Exception as e:
                print(f"❌ 分析失败：{str(e)}")
                continue
            # 输出+保存报告（原有逻辑，不改动）
            print("\n" + "="*60)
            print("✅ 分析完成！最终报告如下：")
            print("-"*60)
            print(report)
            save_choice = input("\n是否保存报告到本地？（y/n）：").strip().lower()
            if save_choice == "y":
                report_path = os.path.join(os.getcwd(), f"Keyword_Report_{query.replace(' ', '_')}.txt")
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(report)
                print(f"📄 报告已保存到：{report_path}")
        
        # 新增PDF流程（增量扩展，不影响原有逻辑）
        elif choice == "2":
            pdf_path = input("\n请输入PDF文件路径（绝对/相对路径）：").strip()
            if not pdf_path:
                print("❌ PDF路径不能为空！")
                continue
            valid_pdf_path = validate_pdf_path(pdf_path)
            if not valid_pdf_path:
                continue
            print("\n🚀 开始执行文献分析（PDF模式）...")
            try:
                report = coordinator.run_pdf(valid_pdf_path)
            except Exception as e:
                print(f"❌ 分析失败：{str(e)}")
                continue
            # 输出+保存报告（复用原有逻辑，仅改文件名）
            print("\n" + "="*60)
            print("✅ 分析完成！最终报告如下：")
            print("-"*60)
            print(report)
            save_choice = input("\n是否保存报告到本地？（y/n）：").strip().lower()
            if save_choice == "y":
                pdf_name = os.path.basename(valid_pdf_path).replace(".pdf", "")
                report_path = os.path.join(os.getcwd(), f"PDF_Report_{pdf_name}.txt")
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(report)
                print(f"📄 报告已保存到：{report_path}")
        
        # 完善退出逻辑（新增，不影响原有流程）
        elif choice == "3":
            print("\n👋 感谢使用！所有生成的报告已保存在当前目录。")
            sys.exit(0)  # 正常退出
        
        else:
            print("❌ 输入无效，请选择1/2/3！")

if __name__ == "__main__":
    main()