# 建议：使用Session State管理状态
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 30

# 在侧边栏中使用session_state
auto_refresh = st.sidebar.checkbox(
    "启用自动刷新", 
    value=st.session_state.auto_refresh,
    key='auto_refresh_checkbox'
)
st.session_state.auto_refresh = auto_refresh