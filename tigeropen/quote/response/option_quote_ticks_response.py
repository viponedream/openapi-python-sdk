# -*- coding: utf-8 -*-
"""
Created on 2018/10/31

@author: gaoan
"""
import six
import pandas as pd

from tigeropen.common.util.string_utils import get_string
from tigeropen.common.util.common_utils import eastern
from tigeropen.common.response import TigerResponse

COLUMNS = ['symbol', 'expiry', 'put_call', 'strike', 'time', 'price', 'volume']


class OptionTradeTickResponse(TigerResponse):
    def __init__(self):
        super(OptionTradeTickResponse, self).__init__()
        self.trade_ticks = []
        self._is_success = None

    def parse_response_content(self, response_content):
        response = super(OptionTradeTickResponse, self).parse_response_content(response_content)
        if 'is_success' in response:
            self._is_success = response['is_success']

        if self.data and isinstance(self.data, list):
            tick_items = []
            for symbol_item in self.data:
                if 'items' in symbol_item and len(symbol_item['items']) > 0:
                    symbol = symbol_item.get('symbol')
                    put_call = symbol_item.get('right').upper()
                    expiry = pd.Timestamp(symbol_item.get('expiry'), unit='ms', tzinfo=eastern).date()
                    strike = float(symbol_item.get('strike'))

                    for item in symbol_item['items']:
                        item_values = {'symbol': symbol, 'expiry': expiry, 'put_call': put_call, 'strike': strike}
                        for key, value in item.items():
                            if value is None:
                                continue
                            if isinstance(value, six.string_types):
                                value = get_string(value)
                            # if 'time' == key:
                            #     value = pd.Timestamp(value, unit='ms', tzinfo=eastern)
                            item_values[key] = value
                        tick_items.append([item_values.get(tag) for tag in COLUMNS])

            self.trade_ticks = pd.DataFrame(tick_items, columns=COLUMNS)
