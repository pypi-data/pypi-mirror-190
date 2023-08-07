from .types import Portfolio
from dateutil.relativedelta import relativedelta
from opendata_finance_kr.clients import StockPriceClient
from warnings import warn
import datetime
import pandas as pd


class Backtester:
    stock_price_client = StockPriceClient()

    def __init__(self):
        self.date_range = self.range_date()
        self.portfolio_list: List[Portfolio] = list()
        self.dataframe = pd.DataFrame()
        self.next_id = 1
        self.portfolio_list_changed = False
        self.query = dict()
        self.query_changed = False
        self.result = pd.DataFrame()

    def reset(self):
        return self.__init__()

    def range_date(self):
        return [
            self.stock_price_client.data_list[0]['date'],
            self.stock_price_client.data_list[-1]['date']
        ]

    def create_portfolio(self, date, stock_codes, weights=None, holding_period_in_month=None, label=None):
        pf = Portfolio(
            id = self.next_id,
            date = date,
            stock_codes = stock_codes,
            weights = weights,
            holding_period_in_month = holding_period_in_month,
            label = label
        )
        validated = self.validate_portfolio(pf)
        self.portfolio_list.append(validated)
        self.next_id += 1
        self.portfolio_list_changed = True
        return validated

    def validate_portfolio(self, portfolio: Portfolio):
        labels = [pf.label for pf in self.portfolio_list]
        if portfolio.label in labels:
            raise Exception(f"Portfolio labelled by '{portfolio.label}' has already exists.")
        if portfolio.date < self.date_range[0]:
            portfolio.date = self.date_range[0]
            warn(f"Input date is replaced to {self.date_range[0]} because it is lesser than the min date of service.")
        df = self.stock_price_client.get_dataframe(portfolio.date)
        omitted = [
            sc for sc in portfolio.stock_codes
            if df.stock_code.isin([sc]).empty
        ]
        if len(omitted) > 0:
            portfolio.omitted += omitted
            warn(f"{len(omitted)} number of stock codes were omitted because price data missing.")

        # some validation process for weights and holding_period_in_month

        # append date range to arrange query
        format_date = lambda dt: datetime.datetime.strptime(dt, '%Y%m%d').date()
        if not portfolio.holding_period_in_month:
            to_date = self.date_range[-1]
        else:
            to_date = format_date(portfolio.date) + relativedelta(months=portfolio.holding_period_in_month)
            to_date = to_date.strftime('%Y%m%d')
        portfolio.date_range = [portfolio.date, to_date]
        return portfolio

    def get_portfolio(self, id_or_label):
        k = self.identify_id_or_label(id_or_label)
        filtered = list(filter(
            lambda pf: getattr(pf, k) == id_or_label,
            self.portfolio_list
        ))
        if len(filtered) == 0:
            raise Exception(f"No matched portfolio with {k} {id_or_label}.")
        return filtered[0]

    def delete_portfolio(self, id_or_label):
        k = self.identify_id_or_label(id_or_label)
        self.portfolio_list = list(filter(
            lambda pf: getattr(pf, k) != id_or_label,
            self.portfolio_list
        ))
        self.portfolio_list_changed = True
        return None

    def identify_id_or_label(self, id_or_label):
        if type(id_or_label) == int:
            return 'id'
        elif type(id_or_label) == str:
            return 'label'
        else:
            raise Exception('Invalid id or label.')

    def create_dataframe(self, return_dataframe=False):
        if len(self.portfolio_list) == 0:
            raise Exception('No portfolio to create dataframe. Please create portfolio.')
        if not self.query_changed:
            return self.dataframe
        for date, stock_code_set in self.query.items():
            df = self.stock_price_client.get_dataframe(date)
            self.dataframe = pd.concat(
                [self.dataframe, df.loc[df.stock_code.isin(stock_code_set)]],
                axis = 0,
                ignore_index = True
            )
        self.portfolio_list_changed = False
        if return_dataframe:
            return self.dataframe
        return None

    def create_query(self, return_query=False):
        if not self.portfolio_list_changed:
            return self.query

        # set date range to query
        min_date = min([pf.date_range[0] for pf in self.portfolio_list])
        max_date = max([pf.date_range[1] for pf in self.portfolio_list])
        query = {
            data['date']: list()
            for data in self.stock_price_client.data_list
            if (data['date'] >= min_date) and (data['date'] <= max_date)
        }

        # set stock codes to query
        for date in query.keys():
            for pf in self.portfolio_list:
                from_date, to_date = pf.date_range
                matched = (date >= from_date) and (date <= to_date)
                if not matched:
                    continue
                query[date] += pf.stock_codes

        # drop duplicates
        for date in query.keys():
            stock_code_set = sorted(list(set(query[date])))
            query[date] = stock_code_set

        # update query
        self.query_changed = self.query != query
        if self.query_changed:
            self.query = query

        if return_query:
            return self.query
        return None

    def execute(self):
        result = pd.DataFrame()
        if self.portfolio_list_changed:
            self.create_query()
            if self.query_changed:
                # return self.dataframe
                print('Creating dataframe for backtest... It takes a couple of minutes.')
                self.create_dataframe()
        for pf in self.portfolio_list:
            result_pf = self.execute_by_portfolio(pf)
            result = pd.concat([result, result_pf], axis=0, ignore_index=True)
        self.result = result.set_index(['date', 'portfolio']).unstack('portfolio')
        return self.result

    def execute_by_portfolio(self, portfolio):
        # subset
        df = self.dataframe[
            (self.dataframe.stock_code.isin(portfolio.stock_codes))
            & (self.dataframe.date >= portfolio.date_range[0])
            & (self.dataframe.date <= portfolio.date_range[1])
        ]
        if portfolio.weights:
            d = dict(zip(portfolio.stock_codes, portfolio.weights))
            w_records = [{
                'stock_code': stock_code,
                'weight': weight
            } for stock_code, weight in d.items()]
            dfw = pd.DataFrame.from_records(w_records)
        else:
            dfw = df[df.date == portfolio.date]
            dfw = dfw[['stock_code', 'date', 'mktcap']]
            sum_mktcap = dfw.mktcap.sum()
            dfw['weight'] = dfw.mktcap / sum_mktcap
            dfw = dfw[['stock_code', 'weight']]
        df = df.merge(dfw, on=['stock_code'])
        df = df.sort_values(['stock_code', 'date'])
        Ri = df.ri / 100 + 1
        is_first = df.stock_code != df.stock_code.shift(1)
        Ri.loc[is_first] = 1
        cum_Ri = Ri.groupby(df.stock_code).cumprod()
        w_cum_Ri = df.weight * cum_Ri

        result_pf = w_cum_Ri.groupby(df.date).sum().rename('cumrp').reset_index()
        result_pf['rp'] = result_pf['cumrp'] / result_pf['cumrp'].shift(1)

        R2pct = lambda s: ((s - 1)*100).round(2)
        result_pf.cumrp = R2pct(result_pf.cumrp)
        result_pf.rp = R2pct(result_pf.rp)
        result_pf['portfolio'] = portfolio.id if not portfolio.label else portfolio.label
        return result_pf[['date', 'portfolio', 'rp', 'cumrp']]
