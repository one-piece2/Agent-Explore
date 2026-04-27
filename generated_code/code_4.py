# 建议：使用环境变量或配置文件管理敏感配置
import os
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

API_CONFIG = {
    'url': os.getenv('COINGECKO_API_URL', 'https://api.coingecko.com/api/v3/simple/price'),
    'timeout': int(os.getenv('API_TIMEOUT', '10')),
    'max_retries': int(os.getenv('API_MAX_RETRIES', '3')),
}