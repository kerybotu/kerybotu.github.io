import os

# 遍历目录中的所有 HTML 文件
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        # 生成标题和描述
        title = filename.replace('.html', '').capitalize() + " - 奇怪的小马维基"
        description = f"探索奇怪的小马维基的 {filename.replace('.html', '')} 页面内容"
        
        # 读取原始文件内容
        with open(filename, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 添加 Front Matter
        front_matter = f"""---
layout: default
title: "{title}"
description: "{description}"
---
"""
        # 检查是否已包含 Front Matter，避免重复添加
        if not original_content.startswith('---'):
            new_content = front_matter + original_content
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已处理: {filename}")
        else:
            print(f"跳过: {filename} (已包含 Front Matter)")