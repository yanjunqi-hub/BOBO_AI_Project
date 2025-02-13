import plotly.graph_objects as go
import numpy as np

class Box:
    def __init__(self, position, size, color, name="默认纸箱", z_cut_count=1):
        self.position = np.array(position)
        self.size = np.array(size)
        self.color = color  # 存储为RGBA数组
        self.name = name  # 存储纸箱名称
        self.z_cut_count = z_cut_count  # 切割块数

    def get_cut_positions(self):
        """计算切割位置并返回每一层的位置"""
        z_cut_positions = []
        dz = self.size[2] / self.z_cut_count  # Z轴上的每一层的高度
        for i in range(1, self.z_cut_count):
            z_cut_positions.append(self.position[2] + dz * i)
        return z_cut_positions

class StackSystem:
    def __init__(self):
        self.boxes = []
        self.size_to_color = {}  # 用于存储尺寸与颜色的映射

        self.colors = [
            'rgba(255, 99, 71, 1)',  # Red
            'rgba(70, 130, 180, 1)',  # SteelBlue
            'rgba(34, 139, 34, 1)',  # Green
            'rgba(255, 165, 0, 1)',  # Orange
            'rgba(238, 130, 238, 1)',  # Violet
            'rgba(255, 105, 180, 1)',  # HotPink
            'rgba(0, 255, 255, 1)',  # Cyan
            'rgba(255, 0, 255, 1)',  # Magenta
            'rgba(255, 140, 0, 1)',  # DarkOrange
            'rgba(50, 205, 50, 1)',  # LimeGreen
        ]

    def add_box(self, size, name, z_cut_count=1):
        """添加新纸箱，并为相同规格的纸箱分配相同颜色"""
        size_tuple = tuple(size)  # 使用尺寸的元组作为键
        if size_tuple not in self.size_to_color:
            color = self.colors[len(self.size_to_color) % len(self.colors)]
            self.size_to_color[size_tuple] = color
        else:
            color = self.size_to_color[size_tuple]

        new_box = Box(position=[0, 0, 0], size=size, color=color, name=name, z_cut_count=z_cut_count)
        self.boxes.append(new_box)
        
    def remove_box(self, box_name):
        """根据名称删除纸箱"""
        self.boxes = [box for box in self.boxes if box.name != box_name]

    def stack_box_to_position(self, box_idx, target_position):
        """将纸箱堆叠到目标坐标位置"""
        target_box = self.boxes[box_idx]
        
        # 更新目标纸箱的位置为目标坐标
        target_box.position = np.array(target_position)

    def visualize(self, is_solid):
        """生成3D可视化图形（使用plotly）"""
        fig = go.Figure()

        for i, box in enumerate(self.boxes):
            self._add_box_to_plot(fig, box, f"Box {i+1}", is_solid)

            # 绘制切割线
            cut_positions = box.get_cut_positions()
            for cut_z in cut_positions:
                self._add_cut_line(fig, box.position[0], box.position[1], cut_z, box.size[0], box.size[1])

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
        
    def _add_box_to_plot(self, fig, box, label, is_solid):
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
        
        if is_solid:
            # 使用 go.Mesh3d 来创建实心的立方体，并设置透明度为1（完全不透明）
            fig.add_trace(go.Mesh3d(
                x=[v[0] for v in vertices],
                y=[v[1] for v in vertices],
                z=[v[2] for v in vertices],
                opacity=1.0,  # 设置透明度为1，表示完全不透明
                color=box.color,  # 填充颜色
                alphahull=0,
                showscale=False
            ))
    
            # 在实心模式下绘制黑色边框
            for edge in edges:
                fig.add_trace(go.Scatter3d(
                    x=[vertices[edge[0]][0], vertices[edge[1]][0]],
                    y=[vertices[edge[0]][1], vertices[edge[1]][1]],
                    z=[vertices[edge[0]][2], vertices[edge[1]][2]],
                    mode='lines',
                    line=dict(color='black', width=2),  # 黑色边框
                    showlegend=False  # 不在图例中显示每条边
                ))
        else:
            # 使用 go.Scatter3d 来创建空心的立方体（仅绘制边），保持透明度为1
            for edge in edges:
                fig.add_trace(go.Scatter3d(
                    x=[vertices[edge[0]][0], vertices[edge[1]][0]],
                    y=[vertices[edge[0]][1], vertices[edge[1]][1]],
                    z=[vertices[edge[0]][2], vertices[edge[1]][2]],
                    mode='lines',
                    line=dict(color=box.color, width=4),
                    showlegend=False  # 不在图例中显示每条边
                ))
    
        # 在图例中显示纸箱的名称（确保显示自定义名称）
        fig.add_trace(go.Scatter3d(
            x=[None], y=[None], z=[None],
            mode='markers',
            marker=dict(
                color=box.color,
                size=25  # 增大marker大小
            ),
            name=box.name  # 在图例中显示纸箱名称
        ))

    def _add_cut_line(self, fig, x, y, z_cut, dx, dy):
        """在3D图中添加切割线"""
        # 绘制从x,y平面到z_cut高度的切割线
        fig.add_trace(go.Scatter3d(
            x=[x, x + dx], y=[y, y], z=[z_cut, z_cut],
            mode='lines',
            line=dict(color="black", width=2),
            showlegend=False
        ))
        fig.add_trace(go.Scatter3d(
            x=[x, x + dx], y=[y + dy, y + dy], z=[z_cut, z_cut],
            mode='lines',
            line=dict(color="black", width=2),
            showlegend=False
        ))

        # 添加侧面切割线
        fig.add_trace(go.Scatter3d(
            x=[x, x], y=[y, y + dy], z=[z_cut, z_cut],
            mode='lines',
            line=dict(color="black", width=2),
            showlegend=False
        ))
        fig.add_trace(go.Scatter3d(
            x=[x + dx, x + dx], y=[y, y + dy], z=[z_cut, z_cut],
            mode='lines',
            line=dict(color="black", width=2),
            showlegend=False
        ))

