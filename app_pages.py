import streamlit as st
from carton_calculation import calculate_and_generate_3d_stack, generate_3d_plot

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
