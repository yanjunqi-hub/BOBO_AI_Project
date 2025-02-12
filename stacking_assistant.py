import plotly.graph_objects as go
import numpy as np

class Box:
    def __init__(self, position, size, color):
        self.position = np.array(position)
        self.size = np.array(size)
        self.color = color  # 存储为RGBA数组

class StackSystem:
    def __init__(self):
        self.boxes = []
        # 使用20个颜色
        self.colors = [
            'rgba(255, 99, 71, 0.6)',  # Red
            'rgba(70, 130, 180, 0.6)',  # SteelBlue
            'rgba(34, 139, 34, 0.6)',  # Green
            'rgba(255, 165, 0, 0.6)',  # Orange
            'rgba(238, 130, 238, 0.6)',  # Violet
            'rgba(255, 105, 180, 0.6)',  # HotPink
            'rgba(0, 255, 255, 0.6)',  # Cyan
            'rgba(255, 0, 255, 0.6)',  # Magenta
            'rgba(255, 140, 0, 0.6)',  # DarkOrange
            'rgba(50, 205, 50, 0.6)',  # LimeGreen
            'rgba(240, 128, 128, 0.6)',  # LightCoral
            'rgba(135, 206, 235, 0.6)',  # SkyBlue
            'rgba(255, 255, 0, 0.6)',  # Yellow
            'rgba(64, 224, 208, 0.6)',  # Turquoise
            'rgba(255, 99, 71, 0.6)',  # Tomato
            'rgba(186, 85, 211, 0.6)',  # MediumOrchid
            'rgba(255, 69, 0, 0.6)',  # RedOrange
            'rgba(102, 205, 170, 0.6)',  # MediumAquamarine
            'rgba(138, 43, 226, 0.6)',  # BlueViolet
        ]
        
    def add_box(self, size, base_position=(0, 0, 0)):
        """添加新立方体"""
        new_color = self.colors[len(self.boxes) % len(self.colors)]
        new_box = Box(
            position=base_position,
            size=size,
            color=new_color  # 直接存储RGBA数组
        )
        self.boxes.append(new_box)
        
    def remove_box(self, box_idx):
        """删除指定索引的纸箱"""
        if 0 <= box_idx < len(self.boxes):
            del self.boxes[box_idx]  # 删除指定索引的纸箱
        else:
            print("纸箱索引无效")

    def stack_boxes(self, box1_idx, box2_idx, axis='z', offset=0):
        """堆叠两个立方体（去除重叠检查）"""
        base_box = self.boxes[box1_idx]
        target_box = self.boxes[box2_idx]
        
        # 计算新位置
        new_position = base_box.position.copy()
        if axis.lower() == 'x':
            new_position[0] += base_box.size[0] + offset
        elif axis.lower() == 'y':
            new_position[1] += base_box.size[1] + offset
        else:  # 默认z轴
            new_position[2] += base_box.size[2] + offset
            
        # 更新目标立方体位置
        target_box.position = new_position
        
    def visualize(self):
        """生成3D可视化图形（使用plotly）"""
        fig = go.Figure()

        for i, box in enumerate(self.boxes):
            self._add_box_to_plot(fig, box, f"Box {i+1}")

        # 更新布局设置
        fig.update_layout(
            scene=dict(
                xaxis=dict(title='X Axis'),
                yaxis=dict(title='Y Axis'),
                zaxis=dict(title='Z Axis'),
            ),
            title='3D Stacked Boxes',
            margin=dict(r=0, l=0, b=0, t=30),  # 设置图表边距
            showlegend=True
        )
        return fig
        
    def _add_box_to_plot(self, fig, box, label):
        """在plotly图表中添加单个立方体"""
        x, y, z = box.position
        dx, dy, dz = box.size
        
        # 使用立方体的八个顶点来定义一个立方体
        vertices = [
            [x, y, z],
            [x + dx, y, z],
            [x + dx, y + dy, z],
            [x, y + dy, z],
            [x, y, z + dz],
            [x + dx, y, z + dz],
            [x + dx, y + dy, z + dz],
            [x, y + dy, z + dz]
        ]
        
        # 定义立方体的边
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # 底面
            [4, 5], [5, 6], [6, 7], [7, 4],  # 顶面
            [0, 4], [1, 5], [2, 6], [3, 7],  # 连接上下的边
        ]
        
        # 从边列表创建边界线
        for edge in edges:
            fig.add_trace(go.Scatter3d(
                x=[vertices[edge[0]][0], vertices[edge[1]][0]],
                y=[vertices[edge[0]][1], vertices[edge[1]][1]],
                z=[vertices[edge[0]][2], vertices[edge[1]][2]],
                mode='lines',
                line=dict(color=box.color, width=4),
                showlegend=False  # 不在图例中显示每条边
            ))

        # 在图例中显示箱子的颜色
        fig.add_trace(go.Scatter3d(
            x=[None], y=[None], z=[None],
            mode='markers',
            marker=dict(
                color=box.color,
                size=25  # 增大marker大小
            ),
            name=label  # 在图例中显示箱子名称
        ))
