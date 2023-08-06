from typing import Union, List

class ScreeningLogic:
    def __init__(
        self,
        id: int,
        variable_name: str,
        yyyymm: str,
        quantile: float,
        keep: str
    ):
        self.id = id
        self.variable_name = variable_name
        self.yyyymm = yyyymm
        if (quantile <= 0) or (quantile >= 1):
            raise Exception('Invalid quantile. Try to input a float in range (0,1).')
        self.quantile = quantile
        keep_set = {'bottom', 'top'}
        if keep not in keep_set:
            raise Exception(f'Invalid keep. Try to input one of {keep_set}.')
        self.keep = keep

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.id}): {self.variable_name}>"


class Portfolio:
    def __init__(
        self,
        id: int,
        date: str,
        stock_codes: List[str],
        weights: Union[List[float], None] = None,
        holding_period_in_month: Union[int, None] = None,
        label: Union[str, None] = None,
    ):
        self.id = id
        self.date = date
        self.stock_codes = stock_codes
        self.weights = weights
        if weights:
            if len(stock_codes) != len(weights):
                raise Exception('weights should have same length as stock_codes.')
        self.holding_period_in_month = holding_period_in_month
        self.omitted = list()
        self.label = label

    def __repr__(self):
        if self.label:
            return f"<{self.__class__.__name__} ({self.label})>"
        return f"<{self.__class__.__name__} ({self.id})>"
