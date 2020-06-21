#-*-coding:utf-8 -*-

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import time
from pyfcm import FCMNotification

cred = credentials.Certificate('drxxx.json')
# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('xxxxxx0.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# 파이어베이스 콘솔에서 얻어 온 API키를 넣어 줌
push_service = FCMNotification(api_key="AAAAXxxxxxxxx")
#Settings 일반 웹API키 
'''
여기서는 지정된 토큰 1개만 넣어서 사용함. 
좀 더 확장할려면 토큰을 앱으로 부터 받거나 앱서버 DB에서 가져와서 다수의 토큰에 알림을 발송 할 수도 있음.
'''
#클라우드 메세징 서버키 토큰 
mToken = "dBrcpo2xxxxxx" #안드로이드스튜디오에서 토큰얻어서 넣기 
nth = 0
def sendMessage():

    global nth
    nth += 1
    registration_id = mToken

    data_message = {
        "body" : " Drone WARNING 알수 없는 드론이 " + str(nth)+"번 나타났습니다."
    }
    
    #data payload만 보내야 안드로이드 앱에서 백그라운드/포그라운드 두가지 상황에서 onMessageReceived()가 실행됨
    result = push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)
    print(result)

def _main():
    dnum=0
    while True:
        doc_ref_drone = db.collection(u'robot').document(u'sky')
        dic = doc_ref_drone.get().to_dict()
        current = int(dic['Num_of_drone'])
        if dnum != current:
            dnum = current
            if dnum != 0:
                print(current)
                print('sending')
                sendMessage()

if __name__ == "__main__":
	_main()