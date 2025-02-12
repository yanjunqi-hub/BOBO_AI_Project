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
    
    # ===== 左侧控制面板 =====
    with st.sidebar:
        st.header("操作面板")
        
        # 新建纸箱输入
        with st.expander("➕ 添加新纸箱", expanded=True):
            new_size = [
                st.number_input("长度 (mm)", min_value=1, value=200, key='new_len'),
                st.number_input("宽度 (mm)", min_value=1, value=150, key='new_wid'),
                st.number_input("高度 (mm)", min_value=1, value=100, key='new_hei')
            ]
            if st.button("添加纸箱"):
                st.session_state.stack_sys.add_box(new_size)
                st.experimental_rerun()  # 添加新纸箱后刷新页面

        # 删除纸箱操作界面
        with st.expander("❌ 删除纸箱", expanded=False):
            if len(st.session_state.stack_sys.boxes) > 0:
                box_to_delete = st.selectbox("选择要删除的纸箱", range(len(st.session_state.stack_sys.boxes)), format_func=lambda x: f"Box {x+1}")
                if st.button("删除纸箱"):
                    st.session_state.stack_sys.remove_box(box_to_delete)
                    st.experimental_rerun()  # 删除纸箱后刷新页面
            else:
                st.warning("没有可删除的纸箱")
        
        # 堆叠操作界面
        with st.expander("🔗 堆叠操作", expanded=True):
            if len(st.session_state.stack_sys.boxes) >= 2:
                box1 = st.selectbox("基础纸箱", 
                                  options=range(len(st.session_state.stack_sys.boxes)),
                                  format_func=lambda x: f"Box {x+1}")
                box2 = st.selectbox("目标纸箱",
                                  options=range(len(st.session_state.stack_sys.boxes)),
                                  format_func=lambda x: f"Box {x+1}")
                axis = st.radio("堆叠方向", ['X轴', 'Y轴', 'Z轴'], index=2)
                offset = st.number_input("间距 (mm)", min_value=0, value=10)
                
                if st.button("执行堆叠"):
                    st.session_state.stack_sys.stack_boxes(
                        box1, box2,
                        axis=axis[0].lower(),
                        offset=offset
                    )
                    st.experimental_rerun()  # 堆叠后刷新页面
            else:
                st.warning("需要至少两个纸箱进行操作")
                
        # 系统控制
        with st.expander("⚙️ 系统设置", expanded=False):
            if st.button("🔄 重置系统"):
                st.session_state.stack_sys = StackSystem()
                st.experimental_rerun()
    
    # ===== 主显示区域 =====
    st.subheader("三维堆叠视图")
    if len(st.session_state.stack_sys.boxes) > 0:
        # 重新渲染图表以反映删除后的变化
        fig = st.session_state.stack_sys.visualize()
        st.plotly_chart(fig)
        
        # 显示纸箱信息表
        st.subheader("纸箱清单")
        box_table = []
        for i, box in enumerate(st.session_state.stack_sys.boxes):
            box_table.append({
                "编号": f"Box {i+1}",
                "位置 (mm)": f"{box.position[0]:.1f}, {box.position[1]:.1f}, {box.position[2]:.1f}",
                "尺寸 (L×W×H)": f"{box.size[0]}×{box.size[1]}×{box.size[2]}",
                "颜色标识": f"<div style='background-color: rgba{box.color}; width: 20px; height: 20px;'></div>"
            })
        st.markdown(
            pd.DataFrame(box_table).to_html(escape=False, index=False), 
            unsafe_allow_html=True
        )
    else:
        st.info("请先添加纸箱开始设计")





