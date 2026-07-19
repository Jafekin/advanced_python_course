import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

# 绘制原始图
plt.rcParams['font.family'] = 'SimHei'

file = "karate.gml"
G = nx.read_gml(file, label='id')

pos = nx.spring_layout(G)

nx.draw(G, pos, node_color='y', width=3.0, with_labels=True)
plt.show()

# 图的平均度数
np.mean([d for d in G.degree()])
# 各节点到其他节点的平均路径长度
shortest_path_lengths = dict(nx.shortest_path_length(G))
average_shortest_path_lengths = [np.mean(list(spl.values())) for spl in shortest_path_lengths.values()]
# 绘制每个节点到其他节点的平均度数
plt.bar(range(1,G.number_of_nodes()+1),average_shortest_path_lengths)
plt.xlabel('节点')
plt.ylabel('对应节点到图中其他所有节点的平均最短路径长度')
plt.show()


# 计算节点7到其他节点的最短路径长度
shortest_path_lengths = nx.shortest_path_length(G, source=7)
# 移除节点7自身
del shortest_path_lengths[7]

farthest_distance = max(shortest_path_lengths.values())
plt.hist(list(shortest_path_lengths.values()), farthest_distance)
plt.xlabel("距离")
plt.ylabel("数目")
# 设置横轴刻度显示格式
plt.xticks(range(1, farthest_distance + 1))
plt.show()

# 显示[2, 5]间的最短路径
target_path = nx.shortest_path(G, 2, 5)
print(target_path)
# 设置指定路径的颜色
edge_colors = ['red' if (u, v) in zip(target_path[:-1], target_path[1:]) or (v, u) in zip(target_path[:-1], target_path[1:])else 'gray' for u, v in G.edges()]
nx.draw(G, pos, node_color='y', width=3.0, with_labels=True, edge_color=edge_colors)
plt.show()

