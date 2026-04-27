import streamlit as st
import requests
import time
from datetime import datetime
import pytz

# 页面配置
st.set_page_config(
    page_title="Bitcoin Price Tracker",
    page_icon="₿",
    layout="centered"
)

# 应用标题和描述
st.title("₿ Bitcoin Price Tracker")
st.markdown("""
实时监控比特币价格，追踪24小时市场变化。
数据来源：CoinGecko API
""")

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #F7931A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .price-container {
        background-color: #f5f5f5;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    .positive-change {
        color: #00cc66;
        font-weight: bold;
    }
    .negative-change {
        color: #ff3333;
        font-weight: bold;
    }
    .last-updated {
        font-size: 0.9rem;
        color: #666;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 缓存数据获取函数，设置TTL为30秒
@st.cache_data(ttl=30)
def get_bitcoin_data():
    """
    从CoinGecko API获取比特币价格数据
    
    Returns:
        dict: 包含价格和变化数据，出错时返回None
    """
    try:
        # CoinGecko API端点
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        # 请求参数
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true'
        }
        
        # 发送请求，设置超时时间
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        
        data = response.json()
        
        if 'bitcoin' not in data:
            st.error("API返回的数据格式异常")
            return None
            
        return {
            'price': data['bitcoin']['usd'],
            'change_24h': data['bitcoin']['usd_24h_change'],
            'last_updated': data['bitcoin']['last_updated_at']
        }
        
    except requests.exceptions.Timeout:
        st.error("请求超时，请检查网络连接")
        return None
    except requests.exceptions.ConnectionError:
        st.error("网络连接错误，请检查网络设置")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP错误: {e}")
        return None
    except requests.RequestException as e:
        st.error(f"请求异常: {e}")
        return None
    except (KeyError, ValueError) as e:
        st.error(f"数据解析错误: {e}")
        return None

def format_price(price):
    """格式化价格显示"""
    if price >= 1000:
        return f"${price:,.2f}"
    else:
        return f"${price:.2f}"

def format_change(change):
    """格式化变化率显示"""
    return f"{change:+.2f}%"

def format_timestamp(timestamp):
    """格式化时间戳"""
    if timestamp:
        # 将Unix时间戳转换为可读格式
        dt = datetime.fromtimestamp(timestamp, pytz.UTC)
        local_dt = dt.astimezone(pytz.timezone('Asia/Shanghai'))
        return local_dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    return "未知时间"

def display_price_metrics(price_data):
    """显示价格指标"""
    if not price_data:
        return
    
    # 价格显示容器
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # 当前价格
            st.markdown(f"""
            <div class="price-container">
                <h2 style="font-size: 3rem; margin-bottom: 0.5rem;">
                    {format_price(price_data['price'])}
                </h2>
                <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                    比特币/USD
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # 变化指标
    col1, col2 = st.columns(2)
    
    with col1:
        # 24小时变化率
        change = price_data['change_24h']
        change_class = "positive-change" if change >= 0 else "negative-change"
        change_emoji = "📈" if change >= 0 else "📉"
        
        st.metric(
            label="24小时变化率",
            value=format_change(change),
            delta=format_change(change),
            delta_color="normal"
        )
    
    with col2:
        # 24小时变化金额
        change_amount = price_data['price'] * (change / 100)
        st.metric(
            label="24小时变化金额",
            value=format_price(change_amount),
            delta=format_price(change_amount),
            delta_color="normal"
        )
    
    # 最后更新时间
    last_updated = format_timestamp(price_data['last_updated'])
    st.markdown(f"""
    <div class="last-updated">
        最后更新: {last_updated}
    </div>
    """, unsafe_allow_html=True)

def main():
    """主应用函数"""
    
    # 侧边栏配置
    with st.sidebar:
        st.header("设置")
        
        # 自动刷新选项
        auto_refresh = st.checkbox("启用自动刷新", value=True)
        refresh_interval = st.slider(
            "刷新间隔(秒)",
            min_value=10,
            max_value=120,
            value=30,
            step=10
        )
        
        st.markdown("---")
        st.markdown("### 关于")
        st.markdown("""
        这是一个比特币价格追踪应用，使用CoinGecko API获取实时数据。
        
        功能包括：
        - 实时比特币价格
        - 24小时价格变化
        - 手动/自动刷新
        - 错误处理和加载状态
        """)
    
    # 主界面
    # 手动刷新按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        refresh_button = st.button("🔄 刷新数据", use_container_width=True)
    
    # 获取数据（带加载状态）
    with st.spinner("正在获取比特币价格数据..."):
        # 如果点击了刷新按钮，清除缓存强制重新获取
        if refresh_button:
            st.cache_data.clear()
        
        price_data = get_bitcoin_data()
    
    # 显示数据或错误信息
    if price_data:
        display_price_metrics(price_data)
        
        # 显示数据状态
        st.success("数据获取成功！")
    else:
        st.error("无法获取比特币价格数据，请稍后重试")
        
        # 显示占位数据（演示用）
        st.info("显示示例数据（演示模式）")
        display_price_metrics({
            'price': 45000.00,
            'change_24h': 2.5,
            'last_updated': time.time()
        })
    
    # 自动刷新逻辑
    if auto_refresh and price_data:
        time.sleep(refresh_interval)
        st.rerun()
    
    # 页脚
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            <p>数据更新频率受API限制，价格仅供参考</p>
            <p>© 2024 Bitcoin Price Tracker</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()