import os
import shutil
from model import model_prediction
import argparse
from test import download_image

def predict(args):
    # Delete previous prediction and croppped object.
    for i in os.listdir("./runs/detect"):
            shutil.rmtree(f"./runs/detect/{i}")
    for i in os.listdir("./Cropped_images"):
        os.remove(f"./Cropped_images/{i}")
    # if path is provided
    if args.path:
        # New Predictions    
        result = model_prediction(args.path)
        result.save()
    # if url is provided
    else:
        print('URL excuated')
        save_path = './test_data/' + args.filename
        download_image(args.url,save_path)
        result = model_prediction(save_path)
        result.save()

        # Creating DataFrame of the results. Use saved to crop the image
    df = result.pandas().xyxy[0]
    df.to_csv('results.csv', index = False)
    print(df[['confidence', 'class']])

def arg(add_help = True):
    parser = argparse.ArgumentParser(description= 'Testing the project', add_help= add_help)
    parser.add_argument('--path', default= None, type= str, help=  'pass the image path')
    parser.add_argument('--filename', default= None, type= str,  help = 'Write name of the file')
    parser.add_argument('--url', default= None, type= str, help = 'pass url to the image')

    return parser.parse_args()

if __name__ == '__main__':
    args = arg()
    predict(args)