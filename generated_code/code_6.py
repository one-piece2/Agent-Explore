# 建议：自定义异常类
class BitcoinDataError(Exception):
    """比特币数据获取异常基类"""
    pass

class APITimeoutError(BitcoinDataError):
    """API请求超时异常"""
    pass

class DataParseError(BitcoinDataError):
    """数据解析异常"""
    pass

# 建议：改进get_bitcoin_data函数
def get_bitcoin_data() -> Optional[BitcoinData]:
    """
    从CoinGecko API获取比特币价格数据
    
    Returns:
        BitcoinData: 比特币数据对象
        None: 获取失败时返回None
    
    Raises:
        BitcoinDataError: 数据获取过程中的特定异常
    """
    try:
        response = requests.get(
            APIConfig.BASE_URL, 
            params=APIConfig.PARAMS, 
            timeout=Constants.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        
        if 'bitcoin' not in data:
            raise DataParseError("API返回的数据格式异常：缺少bitcoin字段")
            
        return BitcoinData(
            price=data['bitcoin']['usd'],
            change_24h=data['bitcoin']['usd_24h_change'],
            last_updated=data['bitcoin'].get('last_updated_at')
        )
        
    except requests.exceptions.Timeout:
        raise APITimeoutError("API请求超时")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            st.warning("API请求频率过高，请稍后重试")
        raise BitcoinDataError(f"HTTP错误: {e}")
    # ... 其他异常处理