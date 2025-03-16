import os
import re
import sys

def process_file(filename):
    """为单个 HTML 文件添加 Front Matter 并清理多余标签"""
    # 生成标题和描述
    base_name = os.path.splitext(filename)[0]  # 去掉 .html 后缀
    title = f"{base_name.capitalize()} - 奇怪的小马维基"
    description = f"探索奇怪的小马维基的 {base_name} 页面内容，了解更多关于小马知识和技术博客的信息。"

    # 读取文件内容
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"错误: {filename} 编码不是 UTF-8，尝试其他编码")
        with open(filename, 'r', encoding='latin1') as f:
            content = f.read()
    except Exception as e:
        print(f"错误: 无法读取 {filename} - {e}")
        return

    # 检查是否已包含 Front Matter
    if content.strip().startswith('---'):
        print(f"跳过: {filename} (已包含 Front Matter)")
        return

    # 清理多余的 HTML 标签，保留 <body> 内的内容
    body_content = re.search(r'<body[^>]*>([\s\S]*?)</body>', content, re.IGNORECASE)
    if body_content:
        cleaned_content = body_content.group(1).strip()
    else:
        # 如果没有 <body> 标签，移除头部和尾部标签
        cleaned_content = re.sub(r'<!DOCTYPE html>[\s\S]*?<html[^>]*>[\s\S]*?<head>[\s\S]*?</head>', '', content, flags=re.IGNORECASE)
        cleaned_content = re.sub(r'</html>', '', cleaned_content, flags=re.IGNORECASE)
        cleaned_content = cleaned_content.strip()

    # 如果内容为空，添加默认提示
    if not cleaned_content:
        cleaned_content = f"<p>欢迎访问 {base_name} 页面，内容待更新。</p>"

    # 生成 Front Matter
    front_matter = f"""---
layout: default
title: "{title}"
description: "{description}"
---
"""

    # 写入新内容
    new_content = front_matter + cleaned_content
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"已处理: {filename}")
    except Exception as e:
        print(f"错误: 无法写入 {filename} - {e}")

def main():
    """主函数，处理目录下所有 HTML 文件"""
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"正在处理目录: {current_dir}")

    # 遍历所有 .html 文件
    html_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.html')]
    if not html_files:
        print("错误: 当前目录下没有找到 .html 文件")
        sys.exit(1)

    for filename in html_files:
        process_file(filename)

    print(f"处理完成，共处理 {len(html_files)} 个文件")

if __name__ == "__main__":
    main()