import os
import cv2
import pandas as pd
import time
import shutil
from model import model_prediction
from crop import object_crop
import argparse
import requests
from io import BytesIO
from PIL import Image

def download_image(url, save_path):
    try:
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Read the content of the response
            image_content = BytesIO(response.content)
            img = Image.open(image_content)
            img.save(save_path)
            print(f"Image downloaded and saved as {save_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return str(save_path)

def test(args):
    '''
    When calling the test function without any image path as input. 
    It will show an image before crop and after crop and also show a detected object. 
    It means you will choose any image from testing data.
    '''
    # Delete previous prediction and croppped object.
    for i in os.listdir("./runs/detect"):
            shutil.rmtree(f"./runs/detect/{i}")
    for i in os.listdir("./Cropped_images"):
        os.remove(f"./Cropped_images/{i}")
    # if path is provided
    if args.path:
        # New Predictions    
        result = model_prediction(args.path)
        result.save(), result.show()
    # if url is provided
    elif args.url:
        print('URL excuated')
        save_path = './test_data/' + args.filename
        download_image(args.url,save_path)
        result = model_prediction(save_path)
        result.save(), result.show()
    # if nothing is provided
    else:
        # New Predictions    
        result = model_prediction(args.data_path)
        result.save(), result.show()

        # Creating DataFrame of the results. Use saved to crop the image
    df = result.pandas().xyxy[0]
    df.to_csv('results.csv', index = False)
    time.sleep(5)
    
    # Finding csv file.
    for f in os.listdir():
        if f.endswith('.csv'):
            info_path = f

    # use of csv file to get coordinates, width and height to crop the image
    
    if args.path:
        image = cv2.imread(args.path)
        cv2.imshow('Original Sample', image)
        cv2.waitKey(0)
        object_crop(args.path, info_path)
    elif args.url:
        image = cv2.imread(save_path)
        cv2.imshow('Original Sample', image)
        cv2.waitKey(0)
        object_crop(save_path, info_path)
    else:
        image = cv2.imread(args.data_path)
        cv2.imshow('Original Sample', image)
        cv2.waitKey(0)
        object_crop(args.data_path, info_path)

    # Showing Cropped Object
    for i in os.listdir("./Cropped_images"):
        image_path = f"./Cropped_images/{i}"
        image = cv2.imread(image_path)
        if image is not None:
            cv2.imshow(f"{i}", image)
            cv2.waitKey(0)
        else:
            print(f'Error Loading Image: {image_path}')
    cv2.destroyAllWindows()
    print('Predictions Done')

def arg(add_help = True):
    parser = argparse.ArgumentParser(description= 'Testing the project', add_help= add_help)
    parser.add_argument('--data-path', default=r".\test_data\dog.jpg", type= str, help= 'Pass the image path')
    parser.add_argument('--path', default= None, type= str, help=  'pass the image path')
    parser.add_argument('--filename', default= None, type= str,  help = 'Write name of the file')
    parser.add_argument('--url', default= None, type= str, help = 'pass url to the image')

    return parser.parse_args()

if __name__ == '__main__':
    args = arg()
    test(args)
    image_url = 'https://c.pxhere.com/photos/e4/1e/dog_labrador_lab_black_animal_pet_cute_domestic-730606.jpg!d'
    filename = "./test_data/downloaded.jpg"