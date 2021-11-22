from imageai.Detection import ObjectDetection
import os
import requests


execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "yolo.h5"))
detector.loadModel()
custom_objects = detector.CustomObjects(car=True, motorcycle=True)

IP = '89.108.88.254'
totalParks = len(requests.get(f'http://{IP}/api/v1/parkings').json())
print(totalParks)
park_id = 1

while(True):

    response = requests.get(f'http://{IP}/api/v1/parkings/{park_id}')
    json_response = response.json()
    pictureUrl = json_response['camera']
    p = requests.get(f'http://{IP}/api/v1/parkings/{park_id}/camera')
    out = open("park.jpg", "wb")
    out.write(p.content)
    out.close()
    temp_percentage = 10


    detections = detector.detectObjectsFromImage(custom_objects=custom_objects, input_image=os.path.join(execution_path, "park.jpg"),
                                                 output_image_path=os.path.join(execution_path, "image2new.jpg"),
                                                 minimum_percentage_probability=temp_percentage)
    freeSpaces = json_response['totalParkingSpaces'] - len(detections)
    print(freeSpaces)
    if freeSpaces != json_response['freeParkingSpaces']:
        if freeSpaces < 0:
            freeSpaces = 0
        requests.post(f'http://{IP}/api/v1/parkings/{park_id}/update', json={"Value": freeSpaces})
        #requests.post(f'http://{IP}/api/v1/parkings/{park_id}/update', json={"freeParkingSpaces": freeSpaces})
    park_id = park_id + 1
    if park_id > totalParks:
        park_id = 1

