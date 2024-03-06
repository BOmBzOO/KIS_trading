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

### /.... PAPER Account .../
```
NAME: "gildong_50953933_paper"
APP_KEY: "PSaOefdskaflsdjflkgjalerruFcN7mgHgrYuus"
APP_SECRET: "ImKZdYxKL/4b8Jhcgjdsajlfkjewslkrujlkouervflub6Tb7bnTW1bs4oArKkfjsdlakrfjeJpDQggjlkdfjslkaCLuykR7mvlul4oqLujA="
CANO: "50953933" # 계좌번호 앞 8자리
ACNT_PRDT_CD: "01" # 계좌번호 뒤 2자리
ACNT_TYPE: "paper"
URL_BASE: "https://openapivts.koreainvestment.com:29443" #모의투자
SOCKET_URL: "ws://ops.koreainvestment.com:31000" # 모의계좌
HTS_ID: "hts_id" # HTS_ID

#디스코드 웹훅 URL
DISCORD_WEBHOOK_URL: "https://discord.com/api/webhooks/1124241629952364566/phiJ3kbfdsfksdl;fksd;lWBIU-0JUh4qkgjakljfgsdlkrjeoliwurewoijf79Z1tOK" # Paper Trading
```
### /.... Live Account .../
```
NAME: "gildong_50953933_live"
APP_KEY: "PSaOefdskaflsdjflkgjalerruFcN7mgHgrYuus"
APP_SECRET: "ImKZdYxKL/4b8Jhcgjdsajlfkjewslkrujlkouervflub6Tb7bnTW1bs4oArKkfjsdlakrfjeJpDQggjlkdfjslkaCLuykR7mvlul4oqLujA="
CANO: "50953933" # 계좌번호 앞 8자리
ACNT_PRDT_CD: "01" # 계좌번호 뒤 2자리
ACNT_TYPE: "live"
URL_BASE: "https://openapi.koreainvestment.com:9443" #실전계좌
SOCKET_URL: "ws://ops.koreainvestment.com:21000" # 실전계좌
HTS_ID: "hts_id" # HTS_ID

#디스코드 웹훅 URL
DISCORD_WEBHOOK_URL: "https://discord.com/api/webhooks/1124241629952364566/phiJ3kbfdsfksdl;fksd;lWBIU-0JUh4qkgjakljfgsdlkrjeoliwurewoijf79Z1tOK" # Live Trading
```

2. ID_ACCOUNT 폴더 생성

