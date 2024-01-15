import cv2
import pandas as pd
from PIL import Image 
from crop import object_crop
from model import model_prediction
import time
import os
import shutil
import argparse

def main(args):
    
    # Delete previous prediction and croppped object.
    for i in os.listdir("./runs/detect"):
        shutil.rmtree(f"./runs/detect/{i}")
    for i in os.listdir("./Cropped_images"):
        os.remove(f"./Cropped_images/{i}")


    # New Predictions    
    result = model_prediction(args.data_path)
    # result.show(), result.save()
    result.save()
    if args.showorginalsample:
        result.show() 
    
    # Creating DataFrame of the results. Use saved to crop the image
    df = result.pandas().xyxy[0]
    df.to_csv('results.csv', index = False)
    time.sleep(5)
    
    # Finding csv file.
    for f in os.listdir():
        if f.endswith('.csv'):
            info_path = f

    # use of csv file to get coordinates, width and height to crop the image
    object_crop(args.data_path, info_path)
    print('Predictions Done')


def arg(help = True):
    parser = argparse.ArgumentParser(description= 'Object Detection and Cropping Project', add_help= help)
    parser.add_argument('--data-path', default=r".\test_data\dog.jpg", type= str, help= 'Pass the image path')
    parser.add_argument('--showorginalsample', default= False, type= bool, help= 'Make it true want to see orginal image' )

    return parser.parse_args()

if __name__ == "__main__":
    args = arg()
    main(args)



