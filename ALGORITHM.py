import pandas as pd
import pytz
import sys
import logging
import math
import websocket
import json
from collections import OrderedDict
import datetime
import os
import time
import Crypto
import sys
from pprint import pprint
sys.modules['Crypto'] = Crypto
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from tr_functions import *
from utility_multiprocessing import Account_detail, delete_JSON

logger = logging.getLogger()

class STRATEGY:
    def __init__(self, info, code):
        self._info = info
        self._code = code
        self._l = logger.getChild(self._code)
        self._STOCKS_DIR_PATH = self._info['STOCKS_DIR_PATH']
        self._stock_info = self._Read_Stock_Info()
        self._current_price = None
        self._positions = "00000"
        self._sell_order_hoga = float(self._stock_info['sell_price_ori'])
        self._buy_order_hoga = None
        self._buy_start_time = datetime.datetime.strptime(self._stock_info['timepoint_trading_start'], "%Y-%m-%d %H:%M:%S")

        
        self._Set_Initial_State()
        # print(self._stock_info['name'], self._stock_info['state'], self._stock_info['positions'], self._positions)

# /... [ Realtime Functions ] .../
    def _Set_Initial_State(self):
        self._Stock_Info_Update_With_Account()
        if self._stock_info['positions'] in ["None","0"]:
            self._stock_info['state'] = 'TO_BUY'
        elif int(self._stock_info['positions']) > 0:
            self._stock_info['state'] = 'TO_SELL'
        else: pass
        self._Write_Stock_Info()

    def _Stock_Info_Update_With_Account(self):
        res = self._Inquire_Balance()
        if res is not None and int(res['hldg_qty'])>0:
            for item in res.keys():
                self._stock_info[item] = res[item]
            self._stock_info['sell_price_modi'] = math.trunc(float(res['pchs_avg_pric'])*(1 + float(self._stock_info['sell_target_percent']))) # 매도가격
            self._stock_info['positions'] = int(res['hldg_qty']) # 보유수량
            self._current_price = int(res['prpr']) # 현재가격
            self._postions = int(self._stock_info['positions'])
            self._sell_order_hoga = int(self._stock_info['sell_price_modi']) # 변화된 매도가격
            self._buy_order_hoga = self._current_price
            self._Write_Stock_Info()
        else:
            self._stock_info['sell_price_modi'] = self._stock_info['sell_price_ori'] # 매도가격
            self._stock_info['positions'] = "0" # 보유수량
            self._positions = "000"
            self._current_price = int(inquire_price(**self._info, code=self._code).json()['output']['stck_prpr']) # 현재가격
            self._stock_info['buy_price_modi'] = self._stock_info['buy_price_ori']
            self._stock_info['buy_qty_modi'] = self._stock_info['buy_qty_ori']
            self._sell_order_hoga = int(self._stock_info['sell_price_modi']) # 변화된 매도가격
            self._buy_order_hoga = self._current_price
            self._Write_Stock_Info()
        
    def _Checkup_Buy_Signal(self):
        t_now = datetime.datetime.now()
        buy_start_time = datetime.datetime.strptime(self._stock_info['timepoint_trading_start'], "%Y-%m-%d %H:%M:%S")
        if ((self._stock_info['state'] == 'TO_BUY') and 
            (self._current_price <= int(self._stock_info['buy_price_ori'])) and
            (t_now >= buy_start_time)
            ):
            self._stock_info['buy_price_modi'] = self._buy_order_hoga
            # self._stock_info['buy_qty_modi'] = int(self._stock_info['buy_amount'])//self._buy_price_hoga
            return True
        else:
            return False

    def _Checkup_Sell_Signal(self):
        # self._stock_info["sell_price_modi"]='-1' # 무조건 매도

        if ((self._stock_info['state'] == 'TO_SELL') and 
            (self._current_price >= int(self._stock_info['sell_price_modi'])) and 
            (self._stock_info['positions']) >= 1
            ):
            return True
        else: 
            return False
    
    def _On_Realtime_Stock_Monitor(self, data):
        tr_id0 = data[1]
        body_data = data[3].split('^')
        if tr_id0 == "H0STASP0":  # [실전/모의투자] 실시간 주식호가
            self._buy_order_hoga = int(body_data[13]) # 매수호가
            self._sell_order_hoga = int(body_data[3]) # 매도호가                
            # time.sleep(1)
            pass
        elif tr_id0 == "H0STCNT0":  # [실전/모의투자] 실시간 주식체결가
            self._current_price = int(body_data[2])
            # print("%-8s%-8s%-8s%-8s%-8s%-8s%-8s" %(self._stock_info['name'], 
            #            self._stock_info['state'],
            #            self._stock_info['buy_price_ori'],
            #             self._current_price, 
            #             self._stock_info['sell_price_ori'],
            #             self._Checkup_Buy_Signal(), 
            #             self._Checkup_Sell_Signal()))
            # 매수 조건
            if self._Checkup_Buy_Signal():
                self._stock_info['buy_qty_submitted'] = math.trunc(int(self._stock_info['buy_amount'])//self._current_price)
                MESSAGE = f"[매수] {self._stock_info['name']}({self._current_price}<={self._stock_info['buy_price_ori']}) {self._stock_info['buy_qty_submitted']}주 주문"
                self._Send_Message(msg=MESSAGE)
                self._Submit_Buy()
                # self._Transition_State("BUY_SUBMITTED")
            else: pass
            # 매도 조건
            if self._Checkup_Sell_Signal():
                MESSAGE = f"[매도] {self._stock_info['name']}({self._current_price}>={self._stock_info['sell_price_modi']}) {self._stock_info['positions']}주 주문"
                self._Send_Message(msg=MESSAGE)
                self._Submit_Sell()
                # self._Transition_State("SELL_SUBMITTED")
            else: pass
            # print(self._stock_info['name'], self._stock_info['state'], self._stock_info['positions'], self._positions)
        
    def _Stock_Signal_Notice(self, pValue):
        매도매수구분 = pValue[4] # 매도매수구분
        종목코드 = pValue[8] # 주식단축종목코드
        체결수량 = pValue[9] # 체결수량
        체결단가 = pValue[10] # 체결단가
        체결시간 = pValue[11] #주식체결시간
        접수여부 = pValue[14] # 접수여부
        주문수량 = pValue[16] #주문수량
        종목명 = pValue[18] # 체결종목명
        
        # 매수
        if 매도매수구분 == '02': # 매수
            if 접수여부 == '1': # 주문 접수
                MESSAGE = f"[매수접수] %s(%s) %s원: %s주" % (종목명, 종목코드, int(체결단가), int(체결수량))
                # self._l.info(MESSAGE)
                # self._Send_Message(MESSAGE)
                self._stock_info['buy_qty_submitted'] = 주문수량
                self._Transition_State("BUY_SUBMITTED")
                # self._Write_Stock_Info()
            elif 접수여부== '2': # 주문 확인
                self._stock_info['positions'] = int(self._stock_info['positions']) + int(체결수량)
                MESSAGE = f"[매수확인] %s(%s) %s원: %s주 %s주보유" % (종목명, 종목코드, int(체결단가), int(체결수량), self._stock_info['positions'])
                # self._l.info(MESSAGE)
                # self._Send_Message(MESSAGE)
                if  int(self._stock_info['positions']) < int(self._stock_info['buy_qty_submitted']):
                    self._Transition_State('BOUGHT_PARTIAL_FILLED')
                if int(self._stock_info['positions']) >= int(주문수량):
                    self._Transition_State('TO_SELL')
                    MESSAGE = f"[매수완료] %s(%s)" % (종목명, 종목코드)
                    self._Send_Message(msg=MESSAGE)
                    self._Stock_Info_Update_With_Account()
                    # Account_detail(**self._info)
            else: pass

        # 매도
        if 매도매수구분 == '01': # 매도
            if 접수여부 == '1': # 주문 접수
                MESSAGE = f"[매도접수] %s(%s) %s원: %s주" % (종목명, 종목코드, int(체결단가), int(체결수량))
                # self._l.info(MESSAGE)
                # self._Send_Message(MESSAGE)
                self._stock_info['sell_qty_submitted'] = 주문수량
                self._stock_info['positions'] = int(주문수량)
                self._Transition_State("SELL_SUBMITTED")
            elif 접수여부 == '2': # 주문 확인
                temp = int(self._stock_info['positions'])
                self._stock_info['positions'] = temp - int(체결수량)
                MESSAGE = f"[매도확인] %s(%s) %s원: %s주 %s주보유" % (종목명, 종목코드, int(체결단가), int(체결수량), self._stock_info['positions'])
                # self._l.info(MESSAGE)
                # self._Send_Message(MESSAGE)
                if  (int(self._stock_info['positions']) > 0) and (int(self._stock_info['positions']) < int(self._stock_info['sell_qty_submitted'])):
                    self._Transition_State('SOLD_PARTIAL_FILLED')
                if  int(self._stock_info['positions']) <= 0:
                    self._Transition_State('SOLD_COMPLETED')
                    MESSAGE = f"[매도완료] %s(%s)" % (종목명, 종목코드)
                    self._Send_Message(msg=MESSAGE)
                    # Account_detail(**self._info)
                    # self._Transition_State('TO_BUY')
                    # self._Delete_Stock_Info_JSON()
                    # self._Set_Initial_State()
        return self._Write_Stock_Info()
    
    def _Transition_State(self, NEW_STATE):
        self._stock_info['state'] = NEW_STATE
        self._Write_Stock_Info()

# [ TR Functions ]           
    def _Inquire_Balance(self):
        res = inquire_balance(**self._info)
        stock_list = res.json()['output1']
        # evaluation = res.json()['output2']
        stock_dict = {}
        for stock in stock_list:
            stock_dict[stock['pdno']] = stock
        if self._code in stock_dict:
            return (stock_dict[self._code])
        else: 
            return None
        
    def _Inquire_Asking_Price_Exp_CCN(self):
        res = inquire_asking_price_exp_ccn(self._code)
        return res
    
    def _Submit_Buy(self):
        res = order_cash_Buy(**self._info, code=self._code, qty=str(self._stock_info['buy_qty_submitted']), price=str(self._current_price), side='market')
        if res['rt_cd'] == '0':
            MESSAGE = f"[매수주문성공] %s(%s) %s" % (self._stock_info['name'], self._code, str(res['msg1']))
            # self._l.info(MESSAGE)
            # self._Send_Message(MESSAGE)
            self._Transition_State('BUY_SUBMITTED')
            return True
        else:
            MESSAGE = f"[매수주문실패] %s(%s) %s" % (self._stock_info['name'], self._code, str(res['msg1']))
            # self._l.info(MESSAGE)
            # self._Send_Message(MESSAGE)           
            self._Transition_State('TO_BUY')
            return False

    def _Submit_Sell(self):
        res = order_cash_Sell(**self._info, code=self._code, qty=str(self._stock_info['positions']), price=str(self._current_price),  side='market')
        if res['rt_cd'] == '0':
            MESSAGE = f"[매도주문성공] %s(%s) %s" % (self._stock_info['name'], self._code, str(res['msg1']))
            # self._l.info(MESSAGE)
            # self._Send_Message(MESSAGE)
            self._Transition_State('SELL_SUBMITTED')
            return True
        else:
            MESSAGE = f"[매도주문실패] %s(%s) %s" % (self._stock_info['name'], self._code, str(res['msg1']))
            # self._l.info(MESSAGE)
            # self._Send_Message(MESSAGE)  
            self._Transition_State('TO_SELL')
            return False

# [ Basic Functions ]   
    def _Out_Of_Market(self):
        today = datetime.datetime.today().weekday()
        market_time_over = self._NOW().time() >= pd.Timestamp('15:30').time()
        return (today==5 or today==6 or market_time_over)
    
    def _Send_Message(self, msg, timestamp='True'):
        now = datetime.datetime.now()
        # message = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"
        # message_discode = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
        if timestamp == 'True':
            message = f"[{now.strftime('%H:%M:%S')}]{str(msg)}"
            message_discode = {"content": message}
        elif timestamp == 'False':
            message = f"{str(msg)}"
            message_discode = {"content": message}
        else: pass
        requests.post(self._info['DISCORD_WEBHOOK_URL'], data=message_discode)
        print(self._info['NAME'], message)

    def _Write_Stock_Info(self):
        file = os.path.join(self._STOCKS_DIR_PATH, f'{self._code}.json')
        with open(file, 'w', encoding='utf-8') as f:
            return json.dump(self._stock_info, f, ensure_ascii=False, indent="\t", sort_keys=True)

    def _Read_Stock_Info(self):
        file = os.path.join(self._STOCKS_DIR_PATH, f'{self._code}.json')
        with open(file, 'r', encoding='utf-8') as f:
            self._stock_info = json.load(f)
        return self._stock_info
    
    def _Delete_Stock_Info_JSON(self):
        filename = os.path.join(self._STOCKS_DIR_PATH, f'{self._code}.json')
        delete_JSON(filename)
               
    def _NOW(self):
        return pd.Timestamp.now(tz='Asia/Seoul')

    

    