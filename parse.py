#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理 d3 树结构，为所有节点添加 numLeafs 信息
叶子节点的 numLeafs = 0
非叶子节点的 numLeafs 是其 children 的长度
"""

import json
import sys


def add_num_leafs(node):
    """
    递归为树的每个节点添加 numLeafs 字段
    
    参数:
        node: 树节点字典
    
    返回:
        修改后的节点
    """
    if 'children' in node and node['children']:
        # 非叶子节点：numLeafs 等于 children 的长度
        node['numLeafs'] = len(node['children'])
        # 递归处理所有子节点
        for child in node['children']:
            add_num_leafs(child)
    else:
        # 叶子节点：numLeafs = 0
        node['numLeafs'] = 0
    
    return node


def process_tree_file(input_file, output_file=None):
    """
    处理 d3 树 JSON 文件
    
    参数:
        input_file: 输入文件路径
        output_file: 输出文件路径，如果为 None 则覆盖输入文件
    """
    # 读取 JSON 文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            tree_data = json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
        return
    except json.JSONDecodeError as e:
        print(f"错误：JSON 解析失败 - {e}")
        return
    
    # 处理树结构
    add_num_leafs(tree_data)
    
    # 确定输出文件路径
    if output_file is None:
        output_file = input_file
    
    # 保存结果
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tree_data, f, ensure_ascii=False, indent=2)
        print(f"处理完成！输出文件：{output_file}")
    except Exception as e:
        print(f"错误：保存文件失败 - {e}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python parse.py <输入文件> [输出文件]")
        print("示例：python parse.py hierarchies/tsinghua_tree.json")
        print("     python parse.py hierarchies/tsinghua_tree.json hierarchies/tsinghua_tree_processed.json")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_tree_file(input_file, output_file)


if __name__ == '__main__':
    main()

