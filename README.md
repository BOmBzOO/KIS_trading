# 한국투자증권 API 사용
한국투자증권 API사용


## Preview
##### 실행화면
![mainwindow](./sample_img/creon_datareader_v1_0.gif)
##### 분 단위 데이터 저장 형식 (DB Browser for SQLite 실행 화면)
![minute](./sample_img/sample_db.PNG)
date를 포함한 모든 값은 integer입니다.

## 폴더 생성필요

1. CONFIG_FILES 생성 후
- infomation.yaml
```
# /.... PAPER Account .../

NAME: "gildong_50953933_paper"
APP_KEY: "PSaOefdskaflsdjflkgjalerruFcN7mgHgrYuus"
APP_SECRET: "ImKZdYxKL/4b8Jhcgjdsajlfkjewslkrujlkouervflub6Tb7bnTW1bs4oArKkfjsdlakrfjeJpDQggjlkdfjslkaCLuykR7mvlul4oqLujA="
CANO: "50953933" # 계좌번호 앞 8자리
ACNT_PRDT_CD: "01" # 계좌번호 뒤 2자리
ACNT_TYPE: "paper"
URL_BASE: "https://openapivts.koreainvestment.com:29443" #모의투자
SOCKET_URL: "ws://ops.koreainvestment.com:31000" # 모의계좌
HTS_ID: "hts_id" # HTS_ID
# FILE_STOCK_INFO: "./stock_info.json" # FILE_STOCK_INFO

#디스코드 웹훅 URL
DISCORD_WEBHOOK_URL: "https://discord.com/api/webhooks/1124241629952364566/phiJ3kbfdsfksdl;fksd;lWBIU-0JUh4qkgjakljfgsdlkrjeoliwurewoijf79Z1tOK" # Paper Trading

```

```
# /.... Live Account .../
NAME: "gildong_50953933_live"
APP_KEY: "PSaOefdskaflsdjflkgjalerruFcN7mgHgrYuus"
APP_SECRET: "ImKZdYxKL/4b8Jhcgjdsajlfkjewslkrujlkouervflub6Tb7bnTW1bs4oArKkfjsdlakrfjeJpDQggjlkdfjslkaCLuykR7mvlul4oqLujA="
CANO: "50953933" # 계좌번호 앞 8자리
ACNT_PRDT_CD: "01" # 계좌번호 뒤 2자리
ACNT_TYPE: "live"
URL_BASE: "https://openapi.koreainvestment.com:9443" #실전계좌
SOCKET_URL: "ws://ops.koreainvestment.com:21000" # 실전계좌
HTS_ID: "hts_id" # HTS_ID
# FILE_STOCK_INFO: "./stock_info.json" # FILE_STOCK_INFO

#디스코드 웹훅 URL
DISCORD_WEBHOOK_URL: "https://discord.com/api/webhooks/1124241629952364566/phiJ3kbfdsfksdl;fksd;lWBIU-0JUh4qkgjakljfgsdlkrjeoliwurewoijf79Z1tOK" # Live Trading

```

2. ID_ACCOUNT 폴더 생성



1. Anaconda 32-bit 설치

만약 Anaconda 64-bit을 사용하고 있는 경우

- 32-bit 추가 설치 또는,

- `set CONDA_FORCE_32BIT`을 이용하여 32-bit 가상환경을 만들어야 합니다.
    
2. 32-bit anaconda `python=3.6` 가상환경에서
	`conda install`을 이용하여 `pyqt5`, `sqlite3`, `pandas`, `pywin32` 설치
    `conda install`이 안되는 모듈은 `pip`로 설치하시면 됩니다.

## 개발 환경
OS: `WINDOW 10`

Python: `Python3.6.4` in `Anaconda3(build version 3.4.1) 32bit`
`pandas 0.22.0` `pyqt: 5.6.0` `pywin32: 222` `sqlite: 3.22.0`

## NOTE
1. 일봉에 대해, ohlcv_only 체크 해제 시 아래 항목들을 추가로 받아옵니다.
	1. 상장주식수
	1. 외국인주문한도수량: 1999년 부터 데이터 존재. (잘못 기록된 데이터 존재함)
	1. 외국인현보유수량: 1999년 부터 데이터 존재. (잘못 기록된 데이터 존재함)
	1. 외국인현보유비율: 1999년 부터 데이터 존재.
	1. 기관순매수: 2004년 부터 데이터 존재.
	1. 기관누적순매수: 2004년 1월 2일을 시작으로 '기관순매수'를 누적한 값.


##### **데이터 제한** (18.02.23 기준)
	이 프로그램은 일봉, 분봉의 데이터만 받도록 구현되어있습니다.
	Creon Plus API에서 데이터 요청 시점으로부터
	1분봉 약 18.5만개(약 2년치 데이터) 조회 가능
	5분봉 약 9만개(약 5년치 데이터) 조회 가능

    1일봉의 경우 제한 없습니다.

### 참고 사이트
