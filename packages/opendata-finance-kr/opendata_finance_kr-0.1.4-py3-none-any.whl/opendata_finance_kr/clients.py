from io import StringIO, BytesIO

import requests
import pandas as pd
import zipfile

class VariableClient:
    # opendata-finance-kr open api 서비스의 base url
    BASE_URL = 'http://apis.opendata-finance-kr.com'

    def __init__(self):
        self.variable_list = self.list_variables()

    def list_variables(self, to_dataframe=False):
        if to_dataframe:  # 데이터프레임으로 변환
            records = list()
            for var in self.variable_list:
                address = var.get('address')
                model_name, id = var.get('address').values()
                r = {
                    **var,
                    'model_name': address.get('model_name'),
                    'id': address.get('id')
                }
                address = r.pop('address')
                records.append(r)
            return pd.DataFrame.from_records(records)
        url = f"{self.BASE_URL}/variable/list"  # 요청 url 구성
        return self.request_data(url)           # 요청

    def request_data(self, url):
        res = requests.get(url)       # 요청 및 응답
        d = res.json()                # dictionary로 변환
        status = d.get('status')  # 응답 상태 확인
        if status['code'] == 204:
            return None
        return d.get('data')

    def get_cross_section(self, variable_name, yyyymm, to_dataframe=False):
        var = self.find_variable_by_name(variable_name)   # 지표 선택
        var_url = self.get_variable_request_url(var)     # 지표 요청 url 구성
        url = f"{var_url}/cross-section/{yyyymm}"         # 횡단면 데이터 요청 url 구성
        data = self.request_data(url)                     # 요청
        if not to_dataframe:
            return data
        return pd.DataFrame.from_records(data.get('records')) # 데이터프레임으로 변환

    def get_time_series(self, variable_name, stock_code, to_dataframe=False):
        var = self.find_variable_by_name(variable_name)  # 지표 선택
        var_url = self.get_variable_request_url(var)     # 지표 요청 url 구성
        url = f"{var_url}/time-series/{stock_code}"       # 시계열 데이터 요청 url 구성
        data = self.request_data(url)                     # 요청
        if not to_dataframe:
            return data
        return pd.DataFrame.from_records(data.get('records')) # 데이터프레임으로 변환

    def download_variable_panel(self, variable_name):
        var = self.find_variable_by_name(variable_name)  # 지표 선택
        return requests.get(var['download_url'])                 # 다운로드


    def find_variable_by_name(self, name):
        filtered = list(filter(lambda var: var['name'] == name, self.variable_list))
        if len(filtered) == 0:
            return Exception(f"no matched variable named with {name}.")
        return filtered[0]

    def get_variable_request_url(self, variable):
        address = variable.get('address')
        return f"{self.BASE_URL}/variable/{address['model_name']}/{address['id']}"


class StockPriceClient:
    BASE_URL = 'http://apis.opendata-finance-kr.com'

    def __init__(self):
        self.data_list = self.list_data()

    def list_data(self, to_dataframe=False):
        if to_dataframe:
            return pd.DataFrame.from_records(self.data_list)
        url = f"{self.BASE_URL}/stock-price/list"
        return self.request_data(url)

    def request_data(self, url):
        res = requests.get(url)
        d = res.json()
        return d.get('data')

    def get_dataframe(self, date, column_name='en'):
        download_url = self.get_download_url(date)
        res = requests.get(download_url)
        zf = zipfile.ZipFile(BytesIO(res.content))
        fnm = zf.namelist()[0]
        with zf.open(fnm) as f:
            encoded = f.read()
            decoded = encoded.decode('utf-8')
        df = pd.read_csv(StringIO(decoded))
        df['basDt'] = df.basDt.astype(str)
        df = df[self.COLUMN_NAME_MAP.keys()] # ordering columns
        if column_name == 'raw':
            return df
        rnm_map = {
            k: v.get(column_name)
            for k, v in self.COLUMN_NAME_MAP.items()
        }
        return df.rename(columns=rnm_map)

    def get_download_url(self, date):
        ls = list(filter(
            lambda data: data['date'] == date,
            self.data_list
        ))
        if len(ls) == 0:
            raise Exception(f"No matched data with date {date}.")
        return ls[0].get('download_url')


    @property
    def COLUMN_NAME_MAP(self):
        return {
            'basDt': {'en': 'date', 'kr': '날짜'},
            'isinCd': {'en': 'isin_code', 'kr': 'ISIN코드'},
            'srtnCd': {'en': 'stock_code', 'kr': '종목코드'},
            'itmsNm': {'en': 'name', 'kr': '종목명'},
            'mrktCtg': {'en': 'market', 'kr': '시장구분'},
            'mkp': {'en': 'open', 'kr': '시가'},
            'hipr': {'en': 'high', 'kr': '고가'},
            'lopr': {'en': 'low', 'kr': '저가'},
            'clpr': {'en': 'close', 'kr': '종가'},
            'vs': {'en': 'delta_close', 'kr': '전일대비'},
            'fltRt': {'en': 'ri', 'kr': '수익률'},
            'lstgStCnt': {'en': 'n_listed', 'kr': '상장주식수'},
            'trqu': {'en': 'vol_n', 'kr': '거래량(주)'},
            'trPrc': {'en': 'vol_m', 'kr': '거래량(원)'},
            'mrktTotAmt': {'en': 'mktcap', 'kr': '시가총액'}
        }
