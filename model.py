import torch
import cv2

def model_prediction(image_path):
    print("****************Model Loading Start***************")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s',_verbose=False)
    # model = YOLO('yolov5n.pt')
    # image_path = 'G:\ObjectDetection\dog.jpg'
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model(image)
    
    return results