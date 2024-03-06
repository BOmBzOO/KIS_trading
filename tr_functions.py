import json
import requests
import time
import Crypto
import sys
sys.modules['Crypto'] = Crypto
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
import requests
import json
import datetime
import os
import time
from pprint import pprint

###############################################################
#### ------------------- [ TR Fucnctions ] ----------------####
###############################################################

def get_access_TOKEN(URL_BASE, APP_KEY, APP_SECRET, **arg):
    headers = {
        "content-type":"application/json"
        }
    body = {
        "grant_type":"client_credentials",
        "appkey":APP_KEY, 
        "appsecret":APP_SECRET
        }
    PATH = "oauth2/tokenP"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    ACCESS_TOKEN = res.json()["access_token"]
    return ACCESS_TOKEN

def get_approval(URL_BASE, APP_KEY, APP_SECRET, **arg):
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": APP_KEY,
            "secretkey": APP_SECRET}
    PATH = "oauth2/Approval"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    APPROVAL_KEY = res.json()["approval_key"]
    return APPROVAL_KEY

def inquire_psbl_order(URL_BASE, APP_KEY, APP_SECRET, ACCESS_TOKEN, CANO, ACNT_PRDT_CD, **arg):
    PATH = "uapi/domestic-stock/v1/trading/inquire-psbl-order"
    URL = f"{URL_BASE}/{PATH}"

    if URL_BASE in ["https://openapivts.koreainvestment.com:29443"]:
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            # "tr_id":"TTTC8908R",
            "tr_id":"VTTC8908R",
            "custtype":"P",
            }
    else:
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            "tr_id":"TTTC8908R",
            # "tr_id":"VTTC8908R",
            "custtype":"P",
            }
    
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": "005930",
        "ORD_UNPR": "65500",
        "ORD_DVSN": "01",
        "CMA_EVLU_AMT_ICLD_YN": "Y",
        "OVRS_ICLD_YN": "Y"
        }
    res = requests.get(URL, headers=headers, params=params)
    return res

def inquire_balance(URL_BASE, APP_KEY, APP_SECRET, ACCESS_TOKEN, CANO, ACNT_PRDT_CD, **arg):
    PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{URL_BASE}/{PATH}"

    if URL_BASE in ["https://openapivts.koreainvestment.com:29443"]:
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            # "tr_id":"TTTC8434R",
            "tr_id":"VTTC8434R",
            "custtype":"P",
            }        
    else:
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            "tr_id":"TTTC8434R",
            # "tr_id":"VTTC8434R",
            "custtype":"P",
            }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
        }
    res = requests.get(URL, headers=headers, params=params)
    return res

def inquire_price(URL_BASE, APP_KEY, APP_SECRET, ACCESS_TOKEN, code="005930", **arg):
    """현재가 조회"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
        "Content-Type":"application/json", 
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"FHKST01010100"
        }
    params = {
        "fid_cond_mrkt_div_code":"J",
        "fid_input_iscd":str(code),
        }
    res = requests.get(URL, headers=headers, params=params)
    return res

def inquire_daily_price(URL_BASE, APP_KEY, APP_SECRET, ACCESS_TOKEN, code="005930", start="20220501", end="20220530", D_W_M_Y="D", adj="0", **arg):
    """국내주식기간별시세(일/주/월/년)"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-price"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
        "Content-Type":"application/json", 
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"FHKST01010400"
        }
    params = {
        "fid_cond_mrkt_div_code":"J",
        "fid_input_iscd":str(code),
        "FID_INPUT_DATE_1":start,
        "FID_INPUT_DATE_2":end,
        "fid_period_div_code":D_W_M_Y,
        "fid_org_adj_prc":adj, # 0:수정주가반영, 1:수정주가미반영
        }
    res = requests.get(URL, headers=headers, params=params)
    return res

def inquire_daily_itemchartprice(URL_BASE, APP_KEY, APP_SECRET, ACCESS_TOKEN, code="005930", D_W_M="D", adj="0", **arg):
    """현재가 조회"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
        "Content-Type":"application/json", 
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"FHKST01010400"
        }
    params = {
        "fid_cond_mrkt_div_code":"J",
        "fid_input_iscd":str(code),
        "fid_period_div_code":D_W_M,
        "fid_org_adj_prc":adj, # 0:수정주가반영, 1:수정주가미반영
        }
    res = requests.get(URL, headers=headers, params=params)
    return res

def order_cash_Buy(URL_BASE, APP_KEY, APP_SECRET, ACCESS_TOKEN, CANO, ACNT_PRDT_CD, code, qty, price, side='market', **arg):
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"

    if side in ["market", "MARKET"]:
        data = {
            "CANO": CANO,
            "ACNT_PRDT_CD": ACNT_PRDT_CD,
            "PDNO": str(code),
            "ORD_DVSN": "01", # 주문구분 (00:지정가, 01:시장가)
            "ORD_QTY": str(qty),
            "ORD_UNPR": "0", # 주문가격 (0: 시장가일 경우)
        }
    else:
        data = {
            "CANO": CANO,
            "ACNT_PRDT_CD": ACNT_PRDT_CD,
            "PDNO": str(code),
            "ORD_DVSN": "00", # 주문구분 (00:지정가, 01:시장가)
            "ORD_QTY": str(qty),
            "ORD_UNPR": str(price), # 주문가격 (0: 시장가일 경우)
        }

    if URL_BASE in ["https://openapivts.koreainvestment.com:29443"]:
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            # "tr_id":"TTTC0802U",
            "tr_id":"VTTC0802U", # 모의 매수 주문
            "custtype":"P",
            "hashkey" : str(hashkey(URL_BASE, APP_KEY, APP_SECRET, data))
            }
    else:
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            "tr_id":"TTTC0802U",
            # "tr_id":"VTTC0802U", # 모의 매수 주문
            "custtype":"P",
            "hashkey" : str(hashkey(URL_BASE, APP_KEY, APP_SECRET, data))
            }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    return res.json()

def order_cash_Sell(URL_BASE, APP_KEY, APP_SECRET, ACCESS_TOKEN, CANO, ACNT_PRDT_CD, code, qty, price, side='market', **arg):
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"
    if side in ["market", "MARKET"]:
        data = {
            "CANO": CANO,
            "ACNT_PRDT_CD": ACNT_PRDT_CD,
            "PDNO": str(code),
            "ORD_DVSN": "01", # 주문구분 (00:지정가, 01:시장가)
            "ORD_QTY": str(qty),
            "ORD_UNPR": "0", # 주문가격 (0: 시장가일 경우)
        }
    else:
        data = {
            "CANO": CANO,
            "ACNT_PRDT_CD": ACNT_PRDT_CD,
            "PDNO": str(code),
            "ORD_DVSN": "00", # 주문구분 (00:지정가, 01:시장가)
            "ORD_QTY": str(qty),
            "ORD_UNPR": str(price), # 주문가격 (0: 시장가일 경우)
        }
    
    if URL_BASE in ["https://openapivts.koreainvestment.com:29443"]:
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            # "tr_id":"TTTC0801U",
            "tr_id":"VTTC0801U", # 모의 매도 주문
            "custtype":"P",
            "hashkey" : str(hashkey(URL_BASE, APP_KEY, APP_SECRET, data))
            }
    else:
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            "tr_id":"TTTC0801U",
            # "tr_id":"VTTC0801U", # 모의 매도 주문
            "custtype":"P",
            "hashkey" : str(hashkey(URL_BASE, APP_KEY, APP_SECRET, data))
            }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    return res.json()

def hashkey(URL_BASE, APP_KEY, APP_SECRET, data, **arg):
    PATH = "uapi/hashkey"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
        'content-Type' : 'application/json',
        'appKey' : APP_KEY,
        'appSecret' : APP_SECRET,
        }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    hashkey = res.json()["HASH"]
    return hashkey

def inquire_asking_price_exp_ccn(URL_BASE, APP_KEY, APP_SECRET, ACCESS_TOKEN, code, **arg):
    PATH = "uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
        "Content-Type":"application/json",
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"FHKST01010200",
        "custtype":"P",
        }
    params = {
        "FID_COND_MRKT_DIV_CODE":"J",
        "FID_INPUT_ISCD":str(code),
        }
    res = requests.get(URL, headers=headers, params=params)
    return res.json()

def check_holiday(URL_BASE, APP_KEY, APP_SECRET, ACCESS_TOKEN, **arg):

    PATH = "uapi/domestic-stock/v1/quotations/chk-holiday"
    URL = f"{URL_BASE}/{PATH}"

    if URL_BASE in ["https://openapivts.koreainvestment.com:29443"]:
        print("Unable to check holiday with Paper Account")
        return False

    headers = {
        "Content-Type":"application/json",
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"CTCA0903R",
        "custtype":"P",
        }
    params = {
        "BASS_DT":"20230625",
        "CTX_AREA_NK":"",
        "CTX_AREA_FK":"",
        }
    res = requests.get(URL, headers=headers, params=params)
    return res.json()

def aes_cbc_base64_dec(key, iv, cipher_text):
    """
    :param key:  str type AES256 secret key value
    :param iv: str type AES256 Initialize Vector
    :param cipher_text: Base64 encoded AES256 str
    :return: Base64-AES256 decodec str
    """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    decoded_text = bytes.decode(unpad(cipher.decrypt(b64decode(cipher_text)), AES.block_size))
    return decoded_text
