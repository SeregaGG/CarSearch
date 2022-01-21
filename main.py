from imageai.Detection import ObjectDetection
import os
import requests
from Camera import Cam

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "yolo.h5"))
detector.loadModel()
custom_objects = detector.CustomObjects(car=True, motorcycle=True)

image_name = 'park'
frame_name = 'lastframe'

current_cam = Cam('http://ekb.holme.ru/webcam/5a592fcbc7d6045057b2ede4/')

temp_percentage = 10
while (True):

    current_cam.WriteImage(image_name, frame_name)
    detections = detector.detectObjectsFromImage(custom_objects=custom_objects,
                                                 input_image=os.path.join(execution_path, image_name + ".jpg"),
                                                 output_image_path=os.path.join(execution_path, "image2new.jpg"),
                                                 minimum_percentage_probability=temp_percentage)
    print(len(detections))
