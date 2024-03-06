import os
import json
import asyncio
import datetime
from utility_asycio import read_JSON, write_JSON, Account_detail, Web_socket_connect, Market_open, Send_message, Liquidation, create_Folder, delete_Folder
from tr_functions import get_access_TOKEN, get_approval, aes_cbc_base64_dec
from ALGORITHM import STRATEGY
from stockinfo_generation_on_trading import stockinfo_generation_on_trading

class OuterWorker:
    def __init__(self, info):
        self._info = info
        self._info_path = self._info['INFO_PATH'] = os.path.join(os.getcwd(), "ID_ACCOUNT", self._info['NAME'])
        self._stock_dir_path = self._info['STOCKS_DIR_PATH'] = os.path.join(self._info['INFO_PATH'], "stocks")
        self._stock_list = read_JSON(f'{self._info_path}/stocksinfo_TOTAL.json')

        idAccout_path = os.path.join(os.getcwd(), "ID_ACCOUNT")
        self._IdAccounts = os.listdir(idAccout_path)

        delete_Folder(self._info['STOCKS_DIR_PATH'])
        create_Folder(self._info['STOCKS_DIR_PATH'])
        for stock in self._stock_list.keys():
            write_JSON(self._stock_list[stock], f'{self._stock_dir_path}/{stock}.json')

        self._info['ACCESS_TOKEN'] = get_access_TOKEN(**self._info) # API 토큰 발급
        self._info['APPROVAL_KEY'] = get_approval(**info) # 웹소켓 키 발급

        self._Stock_Algo = Assign_Trading_Algorithm_To_Stock(self._info, self._stock_list) # 각각의 주식 종목당 정해진 트레이딩 알고리즘 배정

    async def do_work(self):
        await Account_detail(**self._info)
        self._ws, self._aes_key, self._aes_iv = await Web_socket_connect(self._info, self._stock_list)
    
        while True:
            try:
                t_now = datetime.datetime.now()
                t_market_open = t_now.replace(hour=9, minute=00, second=00, microsecond=00)
                t_liquidation = t_now.replace(hour=15, minute=22, second=00, microsecond=00)
                t_15_20 = t_now.replace(hour=15, minute=20, second=00, microsecond=00)
                t_15_30 = t_now.replace(hour=15, minute=30, second=00, microsecond=00)
                t_market_closed = t_now.replace(hour=15, minute=40, second=00, microsecond=00)
                t_exit = t_now.replace(hour=15, minute=40, second=00, microsecond=00)

                # if not Market_open(**self._info):
                #     time.sleep(10)
                #     continue
     
                if (t_now == t_liquidation) and (t_now.second <= 3):
                    await Liquidation(**self._info)
                    # await asyncio.sleep(0.01)
                else: pass

                if t_market_open < t_now < t_market_closed:
                    if (t_now.minute % 2) == 0 and (t_now.second <= 3): 
                        await Account_detail(**self._info)
                else: pass

                data = self._ws.recv()
                await asyncio.sleep(0.01)
                if data[0] in ['0', '1']:  # 실시간 데이터일 경우
                    if data[0] == '0': # 주식 호가/주식 체결
                        recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                        trid0 = recvstr[1]
                        body_data = recvstr[3].split('^')
                        code = body_data[0]
                        # STRATEGY(self._info, code=code)._On_Realtime_Stock_Monitor(recvstr)
                        self._Stock_Algo[code]._On_Realtime_Stock_Monitor(recvstr)
                    elif data[0] == '1': # 주식체결 통보
                        recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                        trid0 = recvstr[1]
                        if trid0 == "K0STCNI0" or trid0 == "K0STCNI9" or trid0 == "H0STCNI0" or trid0 == "H0STCNI9":  # 주실체결 통보 처리
                            aes_dec_str = aes_cbc_base64_dec(self._aes_key, self._aes_iv, recvstr[3]).split('^')
                            code = aes_dec_str[8]
                            # STRATEGY(self._info, code=code)._Stock_Signal_Notice(aes_dec_str)
                            self._Stock_Algo[code]._Stock_Signal_Notice(aes_dec_str)
                else:
                    jsonObject = json.loads(data)
                    
                    trid = jsonObject["header"]["tr_id"]
                    if trid != "PINGPONG":
                        rt_cd = jsonObject["body"]["rt_cd"]
                        if rt_cd == '1':    # 에러일 경우 처리
                            print("[%s] ERROR RETURN CODE [%s] MSG [%s]" % (self._info['NAME'], rt_cd, jsonObject["body"]["msg1"]))
                        elif rt_cd == '0':  # 정상일 경우 처리
                            print("[%s] RETURN CODE [%s] MSG [%s]" % (self._info['NAME'], rt_cd, jsonObject["body"]["msg1"]))
                            if trid == "K0STCNI0" or trid == "K0STCNI9" or trid == "H0STCNI0" or trid == "H0STCNI9":
                                self._aes_key = jsonObject["body"]["output"]["key"]
                                self._aes_iv = jsonObject["body"]["output"]["iv"]
                                print("[%s] TRID [%s] KEY[%s] IV[%s]" % (self._info['NAME'], trid, self._aes_key, self._aes_iv))
                    elif trid == "PINGPONG":
                        print("[%s] RECV [%s]" % (self._info['NAME'], trid))
                        print("[%s] SEND [%s]" % (self._info['NAME'], trid))
            except Exception as e:
                print(e)

def Assign_Trading_Algorithm_To_Stock(info, stock_infos):
    Trading_Algo = {}
    for code in stock_infos.keys():
        algo = STRATEGY(info, code=code)
        Trading_Algo[code] = algo
    return Trading_Algo

async def main():
    idAccount_path = os.path.join(os.getcwd(), "ID_ACCOUNT")
    idAccounts = os.listdir(idAccount_path)

    id_Accounts = {}
    for IdAccount in idAccounts:
        id_Account = read_JSON(f'{idAccount_path}/{IdAccount}/info.json')
        id_Accounts[id_Account['NAME']] = id_Account

    outer_workers = [OuterWorker(info=id_Accounts[id_Account]) for id_Account in id_Accounts.keys()]
    tasks = [outer_worker.do_work() for outer_worker in outer_workers]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    stockinfo_generation_on_trading()
    asyncio.run(main())



