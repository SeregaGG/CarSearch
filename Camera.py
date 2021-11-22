import requests
import m3u8
import cv2

#http://ekb.holme.ru/webcam/5a592fcbc7d6045057b2ecfc/
m3u8_url = 'https://msk3007.extcam.com/hls/playlist.m3u8?hlsId=226c31ee482b4398989b033fba779514_100000884167_0&expires_at=1637579395&token=09fb8c5c4c5e86f5fc58c03ccd2fa75e'
ts_url = 'https://msk3007.extcam.com/hls/'
r = requests.get(m3u8_url)
m3u8_master = m3u8.loads(r.text)

with open("test.ts", 'wb') as file:
    url = ts_url + m3u8_master.data['segments'][len(m3u8_master.data['segments'])-1]['uri']
    rr = requests.get(url)
    file.write(rr.content)

cam = cv2.VideoCapture("test.ts")
ret, frame = cam.read()
if ret:
    cv2.imwrite('park.jpg', frame)

