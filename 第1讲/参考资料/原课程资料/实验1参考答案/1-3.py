import json
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (5,3)

with open('airports.json','r',encoding='utf-8') as f:
    data = json.load(f)
latitude = []
longitude = []
height = []
for code in data:
    airport = data[code]
    latitude.append(airport['lat'])
    longitude.append(airport['lon'])
    height.append(airport['elevation']*0.3048)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(longitude,latitude,height)
ax.set_xlabel('经度')
ax.set_ylabel('纬度')
ax.set_zlabel('海拔')
ax.set_xlim(-200, 200)
ax.xaxis.set_major_locator(MultipleLocator(50))
ax.set_ylim(-75,75)
ax.yaxis.set_major_locator(MultipleLocator(25))
ax.set_zlim(0,4000)
ax.zaxis.set_major_locator(MultipleLocator(1000))
plt.title('机场分布')
ax.view_init(elev=30, azim=45)  # 调整为仰角30度，方位角45度
plt.show()