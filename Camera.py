import requests
import m3u8
import cv2
import time
import re
from seleniumwire import webdriver  # Import from seleniumwire http://ekb.holme.ru/webcam/5a592fcbc7d6045057b2ede4/


class Cam:

    def __init__(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        time.sleep(10)  # ????

    def WriteImage(self, image_name, frame_name):

        lastFrame = ""
        for r in self.driver.requests:
            if re.search('\.ts', r.__str__()):
                #print(r)
                lastFrame = r.__str__()

        with open(frame_name + ".ts", 'wb') as file:
            url = lastFrame
            rr = requests.get(url)
            file.write(rr.content)

        cam = cv2.VideoCapture(frame_name + ".ts")
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(image_name + '.jpg', frame)

    def __del__(self):
        self.driver.quit()
    # http://ekb.holme.ru/webcam/5a592fcbc7d6045057b2ecfc/
    # m3u8_url = 'http://ekb.holme.ru/webcam/5a592fcbc7d6045057b2ede4/'
    # r = requests.Session().get(m3u8_url)
    # print(r.headers)
