from .types import ScreeningLogic
from functools import reduce
from typing import List
import pandas as pd
from opendata_finance_kr.clients import VariableClient

class Screener:
    variable_client = VariableClient()

    def __init__(self):
        self.logic_list = list()
        self.next_id = 1
        self.dataframe = pd.DataFrame()
        self.result = pd.DataFrame()

    def reset(self):
        return self.__init__()

    def create_logic(self, variable_name, yyyymm, quantile, keep):
        id = self.next_id
        self.next_id += 1
        logic = ScreeningLogic(
            id = id,
            variable_name = variable_name,
            yyyymm = yyyymm,
            quantile = quantile,
            keep = keep
        )
        self.logic_list.append(logic)
        return logic

    def get_logic(self, id):
        filtered = list(filter(lambda logic: logic.id == id, self.logic_list))
        if len(filtered) == 0:
            raise Exception(f'No logic with id {id}.')
        return filtered[0]

    def delete_logic(self, id):
        self.logic_list = list(filter(lambda logic: logic.id != id, self.logic_list))
        return None

    def order_logics(self, ordered_id: List[int]):
        self.logic_list = [self.get_logic(id) for id in ordered_id]
        return None

    def create_dataframe(self):
        if len(self.logic_list) == 0:
            return pd.DataFrame()
        ls_cs = list()
        for logic in self.logic_list:
            cs = self.variable_client.get_cross_section(
                variable_name = logic.variable_name,
                yyyymm = logic.yyyymm,
                to_dataframe = True
            )
            del cs['date']
            cs = cs.rename(columns={'value': logic.variable_name})
            cs = cs.set_index(['stock_code', 'market'])
            ls_cs.append(cs)
        df = pd.concat(ls_cs, axis=1)
        df = df.dropna().copy()
        self.dataframe = df
        return self.dataframe

    def execute(self, ordered):
        self.create_dataframe()
        if ordered:
            return self.execute_ordered()
        else:
            return self.execute_unordered()

    @property
    def METHOD_SET(self):
        return {'ordered', 'unordered'}

    def execute_ordered(self):
        screened = self.dataframe.copy()
        for logic in self.logic_list:
            s = screened[logic.variable_name]
            breakpoint = s.quantile(logic.quantile)
            if logic.keep == 'bottom':
                survivors = s <= breakpoint
            elif logic.keep == 'top':
                suvivors = s > breakpoint
            screened = screened[suvivors].copy()
        self.result = screened
        return self.result

    def execute_unordered(self):
        ls_survivors = list()
        for logic in self.logic_list:
            s = self.dataframe[logic.variable_name]
            breakpoint = s.quantile(logic.quantile)
            if logic.keep == 'bottom':
                ls_survivors.append(s <= breakpoint)
            elif logic.keep == 'top':
                ls_survivors.append(s > breakpoint)
            survivors = reduce(lambda x, y: x & y, ls_survivors)
        self.result = self.dataframe[survivors].copy()
        return self.result
