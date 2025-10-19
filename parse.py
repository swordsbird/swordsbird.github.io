#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理 d3 树结构，为所有节点添加 numLeafs 和 id 信息
叶子节点的 numLeafs = 0
非叶子节点的 numLeafs 是其 children 的长度
每个节点都有唯一的 id
"""

import json
import sys


class NodeProcessor:
    """节点处理器类，用于维护全局 ID 计数器"""
    
    def __init__(self):
        self.node_id = 0
    
    def process_node(self, node):
        """
        递归为树的每个节点添加 numLeafs 和 id 字段
        
        参数:
            node: 树节点字典
        
        返回:
            修改后的节点
        """
        # 为当前节点分配唯一 ID
        node['id'] = self.node_id
        self.node_id += 1
        
        if 'children' in node and node['children']:
            # 非叶子节点：numLeafs 等于 children 的长度
            node['numLeafs'] = len(node['children'])
            # 递归处理所有子节点
            for child in node['children']:
                self.process_node(child)
        else:
            # 叶子节点：numLeafs = 0
            node['numLeafs'] = 0
        
        return node


def process_tree_file(input_file):
    """
    处理 d3 树 JSON 文件，直接覆盖原文件
    
    参数:
        input_file: 输入文件路径
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
    
    # 创建处理器并处理树结构
    processor = NodeProcessor()
    processor.process_node(tree_data)
    
    # 保存结果（覆盖原文件）
    try:
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(tree_data, f, ensure_ascii=False, indent=2)
        print(f"处理完成！已更新文件：{input_file}")
        print(f"共处理了 {processor.node_id} 个节点")
    except Exception as e:
        print(f"错误：保存文件失败 - {e}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python parse.py <输入文件>")
        print("示例：python parse.py hierarchies/tsinghua_tree.json")
        print("注意：会直接修改原文件！")
        return
    
    input_file = sys.argv[1]
    process_tree_file(input_file)


if __name__ == '__main__':
    main()

