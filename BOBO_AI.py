import streamlit as st
import app_pages

def main():
    st.sidebar.title("啵啵的AI小屋")
    
    st.sidebar.markdown("<strong>此页面用于设计工作，欢迎使用！</strong>", unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    def login():
        st.session_state.logged_in = True
        st.experimental_rerun()

    def logout():
        st.session_state.logged_in = False
        st.experimental_rerun()

    if st.session_state.logged_in:
        st.sidebar.write("注销")
        if st.sidebar.button("注销"):
            logout()
        st.sidebar.markdown("---")
        # 选择功能
        page = st.sidebar.selectbox("选择一个功能", ["计算并生成3D堆码图"], key="page_selector")
        
        if page == "计算并生成3D堆码图":
            # 调用纸箱堆码计算功能
            app_pages.render_carton_stacking()
    else:
        st.sidebar.write("请先登录")
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        if st.button("登录"):
            if username == "BOBO" and password == "19980323":
                login()
            else:
                st.error("用户名或密码错误")

    if not st.session_state.logged_in:
        st.write("请登录以查看更多功能。")

if __name__ == "__main__":
    main()
