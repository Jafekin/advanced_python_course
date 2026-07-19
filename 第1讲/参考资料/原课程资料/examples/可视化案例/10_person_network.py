import networkx as nx
import matplotlib.pyplot as plt

# 创建一个空的无向图
G = nx.Graph()

# 添加节点
nodes = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
G.add_nodes_from(nodes)

# 添加边
edges = [('Alice', 'Bob'), ('Alice', 'Charlie'), ('Bob', 'Charlie'),
         ('David', 'Eve'), ('Charlie', 'Eve')]
G.add_edges_from(edges)

# 绘制网络图
pos = nx.spring_layout(G)  # 节点布局

# 绘制节点
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)

# 绘制边
nx.draw_networkx_edges(G, pos, edge_color='gray')

# 绘制节点标签
labels = {node: node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=12)

# 设置图的标题
plt.title("Social Network")

# 显示网络图
plt.axis('off')
plt.show()