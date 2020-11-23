
# Blueprint for StartupDay
> 스타트업 밋업데이 2020 사이트를 위한 설계도
> Written By Happycastle ( Soungmin Son )
## WEB
> 기본적으로 Bottom Navigation Style로 구성
### /
메인 화면 
로그인 되어 있지 않다면 login 화면으로 redirect
### /login
구글 로그인
### /map
부스 맵
### /bingo
개인 별 빙고판
### /profile
개인 별 QR 코드 및 부스 참여내역 알림
### /booth
부스 소개
### 미사용
### /plan
행사 일정 소개 및 현재 일정 소개
### /booth/<string>
부스 명에 해당하는 부스 세부설명
## DB (MongoDB Collection)
### USER
- _id : 고유 키값으로 활용
- award : 기본 False 보상 수령 여부 확인
- bingo
```
bingo : [
   '_id'
]
```
- booth : 부스 이용 내역
```
{
   'name': '부스이름',
   'code': '부스 코드',
   'date': '이용시간'
}
```
### Booth
부스 내용 저장
```
{
   'name': '부스이름시발',
   'club': '운영동아리시발',
   '_id': '고유아이디시발',
   'message': '메세지',
   'busy': 0|1|2,,
   'code': '3B'
}
```