import networkx as nx
import matplotlib.pyplot as plt
from numpy.ma.extras import average
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (5,3)



G = nx.read_gml("karate.gml",label='id')
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color='y', width=3.0,
with_labels=True)
plt.show()
# 求取图中节点数，边数，图的平均度数，绘制每个节点到其他所有节点度数的柱状图。
N = G.number_of_nodes()
E = G.number_of_edges()
G_average = 2*E/N
print(N,E,G_average)
shortest_path_lengths = dict(nx.shortest_path_length(G))
print(shortest_path_lengths)
average_shortest_path_lengths = [np.mean(list(spl.values())) for spl in shortest_path_lengths.values()]
plt.bar(range(1,N+1),average_shortest_path_lengths)
plt.xlabel('节点')
plt.ylabel('对应节点到图中其他所有节点的平均最短路径长度')
plt.show()

# 绘制10号节点到其他节点的距离分布直方图，在图上标注出平均值
shortest_path_lengths_10 = nx.shortest_path_length(G, source=10)
del shortest_path_lengths_10[10]
plt.hist(shortest_path_lengths_10.values(),max(shortest_path_lengths_10.values()))
plt.xticks(range(1,max(shortest_path_lengths_10.values())+1))
plt.xlabel("节点 10 到其他可达节点的最短路径长度")
plt.ylabel("具有对应距离的节点数量")
plt.show()

# 在图上可视化显示[1, 10]间的最短路径（可使用edge_colors属性个性化定义边的颜色）
target_path = nx.shortest_path(G,source=1,target=10)
print(target_path)
path_edges = set(zip(target_path[:-1],target_path[1:]))
edge_colors = ['red' if (u, v) in path_edges or (v, u) in path_edges else 'grey' for u, v in G.edges()]
nx.draw(G, pos, node_color='y', width=3.0, with_labels=True, edge_color=edge_colors)
plt.show()
