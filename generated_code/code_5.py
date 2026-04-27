# 建议：提取常量定义
class Constants:
    DEFAULT_REFRESH_INTERVAL = 30
    MIN_REFRESH_INTERVAL = 10
    MAX_REFRESH_INTERVAL = 120
    CACHE_TTL = 30
    DEFAULT_TIMEOUT = 10
    
class APIConfig:
    BASE_URL = "https://api.coingecko.com/api/v3/simple/price"
    PARAMS = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd',
        'include_24hr_change': 'true',
        'include_last_updated_at': 'true'
    }

# 建议：创建数据模型类
from dataclasses import dataclass
from typing import Optional

@dataclass
class BitcoinData:
    price: float
    change_24h: float
    last_updated: Optional[int] = None
    
    @property
    def formatted_price(self) -> str:
        return f"${self.price:,.2f}" if self.price >= 1000 else f"${self.price:.2f}"
    
    @property
    def formatted_change(self) -> str:
        return f"{self.change_24h:+.2f}%"