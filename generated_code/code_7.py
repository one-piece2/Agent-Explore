# 建议：添加重试机制
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError)),
    reraise=True
)
@st.cache_data(ttl=Constants.CACHE_TTL)
def get_bitcoin_data_with_retry() -> Optional[BitcoinData]:
    """带重试机制的数据获取函数"""
    return get_bitcoin_data()