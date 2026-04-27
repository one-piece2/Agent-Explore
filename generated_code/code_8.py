# 建议：添加数据新鲜度检查
def is_data_fresh(last_updated: Optional[int], max_age_seconds: int = 60) -> bool:
    """检查数据是否新鲜"""
    if not last_updated:
        return False
    current_time = int(time.time())
    return (current_time - last_updated) <= max_age_seconds

# 在显示数据时添加新鲜度提示
if price_data and not is_data_fresh(price_data.last_updated, max_age_seconds=60):
    st.warning("数据可能不是最新的，正在尝试刷新...")