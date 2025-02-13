# 完整import列表应类似：
import streamlit as st
from carton_calculation import calculate_and_generate_3d_stack, generate_3d_plot
import pandas as pd
from stacking_assistant import StackSystem

def render_carton_stacking():
    st.markdown("<h1 class='big-header'>纸箱堆码计算与3D可视化</h1>", unsafe_allow_html=True)
    
    # Inputs for carton and pallet sizes
    carton_length = st.number_input("请输入纸箱长度 (毫米)", min_value=1, value=400)
    carton_width = st.number_input("请输入纸箱宽度 (毫米)", min_value=1, value=300)
    carton_height = st.number_input("请输入纸箱高度 (毫米)", min_value=1, value=200)

    pallet_length = st.number_input("请输入托盘长度 (毫米)", min_value=1, value=1100)
    pallet_width = st.number_input("请输入托盘宽度 (毫米)", min_value=1, value=1100)
    max_length_with_margin = st.number_input("允许的最大长度 (毫米)", min_value=1, value=1150)
    max_width_with_margin = st.number_input("允许的最大宽度 (毫米)", min_value=1, value=1150)
    max_height = st.number_input("托盘的最大高度 (毫米)", min_value=1, value=2000)

    if st.button("计算并生成3D堆码图"):
        # Call the calculation function from carton_calculation.py
        max_cartons_length, max_cartons_width, cartons_per_layer, max_layers, total_cartons_per_pallet = calculate_and_generate_3d_stack(
            carton_length, carton_width, carton_height, pallet_length, pallet_width, max_length_with_margin, max_width_with_margin, max_height
        )

        # Display results
        st.write(f"**每层纸箱数量:** {cartons_per_layer}")
        st.write(f"**最大层数:** {max_layers}")
        st.write(f"**总纸箱数量:** {total_cartons_per_pallet}")
        st.write(f"**每层的纸箱摆放 (行数x列数):** {max_cartons_length} x {max_cartons_width}")

        # Generate and display 3D plot
        fig = generate_3d_plot(max_cartons_length, max_cartons_width, max_layers, carton_length, carton_width, carton_height)
        st.pyplot(fig)

def render_stacking_assistant():
    st.markdown("<h1 class='big-header'>📦 智能纸箱堆叠助手</h1>", unsafe_allow_html=True)
    
    # 初始化堆叠系统
    if 'stack_sys' not in st.session_state:
        st.session_state.stack_sys = StackSystem()

    # 初始化纸箱规格字典
    if 'box_specs' not in st.session_state:
        st.session_state.box_specs = {}  # 存储纸箱规格

    # 确保 display_mode 被初始化
    if 'display_mode' not in st.session_state:
        st.session_state.display_mode = '实心'  # 默认值为实心

    # ===== 左侧控制面板 =====
    with st.sidebar:
        st.header("操作面板")
        
        # 设置纸箱规格
        with st.expander("📌 纸箱规格设置", expanded=True):
            spec_name = st.text_input("纸箱规格名称", value="A")  # 纸箱规格名称
            spec_size = [
                st.number_input("长度 (mm)", min_value=1, value=200, key='spec_len'),
                st.number_input("宽度 (mm)", min_value=1, value=150, key='spec_wid'),
                st.number_input("高度 (mm)", min_value=1, value=100, key='spec_hei')
            ]
            z_cut_count = st.number_input("切割块数", min_value=1, value=1, step=1)  # 新增切割块数
            if st.button("添加规格"):
                st.session_state.box_specs[spec_name] = {"size": spec_size, "z_cut_count": z_cut_count}  # 存储规格和切割块数
                st.success(f"已添加纸箱规格：{spec_name} ({spec_size[0]}×{spec_size[1]}×{spec_size[2]}) 切割块数：{z_cut_count}")

        # 添加新纸箱
        with st.expander("➕ 添加新纸箱", expanded=True):
            if len(st.session_state.box_specs) > 0:
                selected_spec = st.selectbox("选择纸箱规格", list(st.session_state.box_specs.keys()))
                box_size = st.session_state.box_specs[selected_spec]["size"]  # 获取规格的尺寸
                z_cut_count = st.session_state.box_specs[selected_spec]["z_cut_count"]  # 获取切割块数
                box_index = st.number_input("纸箱序号", min_value=1, value=1, step=1)
                new_name = f"{selected_spec}_{box_index}"  # 自动生成纸箱名称
                if st.button("添加纸箱"):
                    st.session_state.stack_sys.add_box(box_size, new_name, z_cut_count)  # 添加纸箱，并考虑切割块数
                    st.experimental_rerun()  # 刷新页面

            else:
                st.warning("请先添加纸箱规格")
                
        # 删除纸箱
        with st.expander("❌ 删除纸箱", expanded=False):
            if len(st.session_state.stack_sys.boxes) > 0:
                box_names = [box.name for box in st.session_state.stack_sys.boxes]
                box_to_delete = st.selectbox("选择要删除的纸箱", box_names, key="delete_box_select")
                
                if st.button("删除纸箱"):
                    # 找到并删除匹配名称的纸箱
                    st.session_state.stack_sys.remove_box(box_to_delete)
                    st.experimental_rerun()  # 刷新页面
            else:
                st.warning("没有可删除的纸箱")

        # 堆叠操作界面
        with st.expander("🔗 堆叠操作", expanded=True):
            if len(st.session_state.stack_sys.boxes) >= 1:
                box_names = [box.name for box in st.session_state.stack_sys.boxes]
                box = st.selectbox("选择目标纸箱", box_names, key="box_select")
                
                # 输入目标坐标
                target_position = (
                    st.number_input("目标 X 坐标 (mm)", value=0, key="target_x"),
                    st.number_input("目标 Y 坐标 (mm)", value=0, key="target_y"),
                    st.number_input("目标 Z 坐标 (mm)", value=0, key="target_z")
                )
                
                if st.button("执行堆叠"):
                    # 找到对应的纸箱
                    box_idx = next(i for i, b in enumerate(st.session_state.stack_sys.boxes) if b.name == box)
                    
                    # 执行堆叠操作，将纸箱放置到目标坐标
                    st.session_state.stack_sys.stack_box_to_position(
                        box_idx, target_position
                    )
                    st.experimental_rerun()  # 刷新页面
            else:
                st.warning("需要至少一个纸箱进行操作")

        # 设置显示模式
        with st.expander("🎨 显示方式", expanded=False):
            display_mode = st.radio("选择纸箱显示方式", ['实心', '空心'], index=0, key="display_mode")
            if st.session_state.display_mode != display_mode:
                st.session_state.display_mode = display_mode

        # 重置系统
        with st.expander("⚙️ 系统设置", expanded=False):
            if st.button("🔄 重置系统"):
                st.session_state.stack_sys = StackSystem()
                st.session_state.box_specs = {}
                st.experimental_rerun()  # 刷新页面

    # ===== 主显示区域 =====
    st.subheader("三维堆叠视图")
    if len(st.session_state.stack_sys.boxes) > 0:
        fig = st.session_state.stack_sys.visualize(is_solid=(st.session_state.display_mode == '实心'))
        st.plotly_chart(fig)
        
        # 显示纸箱信息表
        st.subheader("纸箱清单")
        box_table = []
        for i, box in enumerate(st.session_state.stack_sys.boxes):
            box_table.append({
                "编号": box.name,
                "位置 (mm)": f"{box.position[0]:.1f}, {box.position[1]:.1f}, {box.position[2]:.1f}",
                "尺寸 (L×W×H)": f"{box.size[0]}×{box.size[1]}×{box.size[2]}",
                "颜色标识": f"<div style='background-color: rgba{box.color}; width: 20px; height: 20px;'></div>"
            })
        st.markdown(
            pd.DataFrame(box_table).to_html(escape=False, index=False), 
            unsafe_allow_html=True
        )
    else:
        st.info("请先添加纸箱")
