import logging
import json
import os
import time
import asyncio
from queue import Queue
from tr_functions import *
from utility_asycio import *
from ALGORITHM import STRATEGY

logger = logging.getLogger()
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

class ID_ACCOUNT:
    def __init__(self, info):
        self._info = info
        self._name = self._info["NAME"]
        self._PATH = os.getcwd()
        self._l = logger.getChild(self._info['CANO'])
        self._DIR = os.path.join(self._PATH, "ID_ACCOUNT" , self._info['NAME'])
        self._info['directory'] = self._DIR
        self._info['ACCESS_TOKEN'] = get_access_TOKEN(**self._info) # API 토큰 발급
        self._info['APPROVAL_KEY'] = get_approval(**self._info) # 웹소켓 키 발급
        write_JSON(self._info, f'{self._DIR}/info.json')
        # info = self._read_JSON(f'{self._directory}/info.json')

        asyncio.run(self._RUN())

        # asyncio.run(self._connect())

    # async def _run():
    #     await asyncio.wait([
    #         asyncio.create_task(self._connect())
    #     ])

    async def _RUN(self):

        while True:
            print("No. 1")
            await asyncio.sleep(5)

        # Get_Balance(**self._info)
        # self._get_balance()
        # self._get_stock_balance()

        # self._stocksinfo = read_JSON(f'{self._DIR}/stocksinfo_TOTAL.json')
        # StockAlgo = self._assign_trading_algorithm_to_stock() # 각각의 주식 종목당 정해진 트레이딩 알고리즘 배정
        # ws = await self._connect_ws() # 웹소켓 연결
        # send_message(**self._info, msg="[ START ALGOTRADING ]")
        
        # while True:
        #     try:
        #         t_now = datetime.datetime.now()
        #         t_market_open = t_now.replace(hour=9, minute=00, second=00)
        #         t_liquidation = t_now.replace(hour=15, minute=21, second=00)
        #         t_15_20 = t_now.replace(hour=15, minute=20, second=00)
        #         t_market_closed = t_now.replace(hour=15, minute=40, second=00)
        #         t_exit = t_now.replace(hour=15, minute=40, second=00)

        #         # if not Market_Open():
        #         #     time.sleep(10)
        #         #     continue
        #         # # print(t_now, t_liquidation)
        #         # # print((t_now == t_liquidation), (t_now.second <= 2))

        #         # if (t_now == t_liquidation) and (t_now.second <= 1):
        #         #     Liquidation()
        #         # else: pass

        #         if t_market_open < t_now < t_market_closed:
        #             if (t_now.minute % 2) == 0 and t_now.second <= 1: 
        #                 print()
        #                 Get_Balance() # 보유 현금 조회
        #                 Get_Stock_Balance()
        #         else: pass

        #         data = Queue()
        #         data = ws.recv()
        #         time.sleep(0.1)
        #         if data[0] == '0' or data[0] == '1':  # 실시간 데이터일 경우
        #             if data[0] == '0': # 주식 호가
        #                 recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
        #                 trid0 = recvstr[1]
        #                 body_data = recvstr[3].split('^')
        #                 code = body_data[0]
        #                 StockAlgo[code]._On_Realtime_Stock_Monitor(recvstr)
        #             elif data[0] == '1': # 주식체결 통보
        #                 recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
        #                 trid0 = recvstr[1]
        #                 if trid0 == "K0STCNI0" or trid0 == "K0STCNI9" or trid0 == "H0STCNI0" or trid0 == "H0STCNI9":  # 주실체결 통보 처리
        #                     aes_dec_str = aes_cbc_base64_dec(aes_key, aes_iv, recvstr[3]).split('^')
        #                     code = aes_dec_str[8]
        #                     StockAlgo[code]._Stock_Signal_Notice(aes_dec_str)
        #         else:
        #             jsonObject = json.loads(data)
        #             trid = jsonObject["header"]["tr_id"]
        #             if trid != "PINGPONG":
        #                 rt_cd = jsonObject["body"]["rt_cd"]
        #                 if rt_cd == '1':    # 에러일 경우 처리
        #                     print("### ERROR RETURN CODE [ %s ] MSG [ %s ]" % (rt_cd, jsonObject["body"]["msg1"]))
        #                     pass
        #                 elif rt_cd == '0':  # 정상일 경우 처리
        #                     print("### RETURN CODE [ %s ] MSG [ %s ]" % (rt_cd, jsonObject["body"]["msg1"]))
        #                     # 체결통보 처리를 위한 AES256 KEY, IV 처리 단계
        #                     if trid == "K0STCNI0" or trid == "K0STCNI9" or trid == "H0STCNI0" or trid == "H0STCNI9":
        #                         aes_key = jsonObject["body"]["output"]["key"]
        #                         aes_iv = jsonObject["body"]["output"]["iv"]
        #                         print("### TRID [%s] KEY[%s] IV[%s]" % (trid, aes_key, aes_iv))
        #             elif trid == "PINGPONG":
        #                 print("### RECV [PINGPONG] [%s]" % (data))
        #                 print("### SEND [PINGPONG] [%s]" % (data))
        #     except Exception as e:
        #         print(e)

    def _connect_ws(self):
        code_list_websocket = []
        for sym in self._stocksinfo.keys():
            code_list_websocket.append(['1','H0STASP0',sym])
            code_list_websocket.append(['1','H0STCNT0',sym])
        code_list_websocket.append(['1','H0STCNI9', self._info['HTS_ID']])

        senddata_list=[]
        for tr_type, tr_id, tr_key in code_list_websocket:
            list_temp = {
                "header": {"approval_key": self._info['APPROVAL_KEY'], "custtype": "P", "tr_type": tr_type, "content-type": "utf-8"},
                "body": { "input": {"tr_id": tr_id,  # API명
                                    "tr_key": tr_key  # 종목번호
                                }
                        }
            }
            temp = json.dumps(list_temp)
            # temp = '{"header":{"approval_key": "%s","custtype":"P","tr_type":"%s","content-type":"utf-8"},"body":{"input":{"tr_id":"%s","tr_key":"%s"}}}'%(info['APPROVAL_KEY'], tr_type, tr_id, tr_key)
            senddata_list.append(temp)
        try: 
            websocket.close()
        except: 
            pass
        ws = websocket.WebSocket()
        ws.connect(self._info['SOCKET_URL'], ping_interval=60)
        for senddata in senddata_list:
            ws.send(senddata)
        return ws

    def _get_balance(self):
        res = inquire_psbl_order(**self._info)
        cash = res.json()['output']['ord_psbl_cash']
        send_message(**self._info, msg=f"{self._info['NAME']}", timestamp='False')
        send_message(**self._info, msg="CURRENT BALANCE DETAILS")
        send_message(**self._info, msg="=" * (40), timestamp='False')
        send_message(**self._info, msg='{0:<18} {1:>20,}'.format('Available Balance:', int(cash)), timestamp='False')
        time.sleep(0.02)
        return cash
    
    def _get_stock_balance(self):
        res = inquire_balance(**self._info)
        stock_list = res.json()['output1']
        evaluation = res.json()['output2']  
        stock_dict = {}
        for stock in stock_list:
            if int(stock['hldg_qty']) > 0:
                stock_dict[stock['pdno']] = stock['hldg_qty']
                send_message(**self._info, msg='{0:<2}{1:<8}({2:<6}):{3:>4}주{4:>7}%'.format('+ ',stock['prdt_name'], stock['pdno'], stock['hldg_qty'], stock['evlu_pfls_rt']), timestamp='False')
                time.sleep(0.01)
        send_message(**self._info, msg="-" * (40), timestamp='False')
        send_message(**self._info, msg='{0:<18} {1:>20,}'.format('Evaluation Amount:', int(evaluation[0]['scts_evlu_amt'])), timestamp='False')
        time.sleep(0.01)
        send_message(**self._info, msg='{0:<18} {1:>20,}'.format('Profits:', int(evaluation[0]['evlu_pfls_smtl_amt'])), timestamp='False')
        time.sleep(0.01)
        send_message(**self._info, msg='{0:<18} {1:>20,}'.format('Total Balance: ', int(evaluation[0]['tot_evlu_amt'])), timestamp='False')
        time.sleep(0.01)
        send_message(**self._info, msg="=" * (40), timestamp='False')
        # send_message("\n", timestamp='False')
        return stock_dict
    
    def _assign_trading_algorithm_to_stock(self):
        # info = Read_JSON('./info.json')
        # stock_infos = Read_JSON('./stock_info.json')
        Trading_Algo = {}
        create_Folder(f'{self._DIR}/stock')
        for code in self._stocksinfo.keys():
            write_JSON (self._stocksinfo[code], f'{self._DIR}/stock/{code}.json')
            algo = STRATEGY(self._info, code=code)
            Trading_Algo[code] = algo
        return Trading_Algo
    
