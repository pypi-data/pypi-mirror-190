from .clients import *
from .tools.screener import Screener
from .tools.backtester import Backtester

def client(service_name: str):
    if service_name == 'variable':
        return VariableClient()
    elif service_name == 'stock_price':
        return StockPriceClient()

def tool(tool_name: str):
    if tool_name == 'screener':
        return Screener()
    elif tool_name == 'backtester':
        return Backtester()
