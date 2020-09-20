#PyTorch lib
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.utils.data as Data
import torch.nn.functional as F
import torchvision
#Tools lib
import numpy as np
import cv2
import random
import time
import os
import argparse
#Models lib
from models import *
#Metrics lib
from metrics import calc_psnr, calc_ssim
import torch.backends.cudnn as cudnn
import torch.optim
import sys
import dataloader
import net
from torchvision import transforms
from PIL import Image
from tqdm import tqdm



def unfog_image(img):

    #data_foggy = Image.open(image_path)
    #data_foggy = (np.asarray(data_foggy) / 255.0)

    #data_foggy = torch.from_numpy(data_foggy).float()
    #data_foggy = data_foggy.permute(2, 0, 1)
    #data_foggy = data_foggy.cuda().unsqueeze(0)
 
    for i in range(2):
        with torch.no_grad():
            img = unfog_net(img)

    #torchvision.utils.save_image(torch.cat((data_foggy, clean_image),0), "results/" + image_path.split("/")[-1])

    return img


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str)
    parser.add_argument("--output_dir", type=str)
    args = parser.parse_args()
    return args

def align_to_four(img):
    
    #align to four
    a_row = int(img.shape[0]/4)*4
    a_col = int(img.shape[1]/4)*4
    img = img[0:a_row, 0:a_col]
    #print ('after alignment, row = %d, col = %d'%(img.shape[0], img.shape[1]))
    return img


def predict(image):
    image = np.array(image, dtype='float32')/255.
    image = image.transpose((2, 0, 1))
    image = image[np.newaxis, :, :, :]
    image = torch.from_numpy(image)
    image = Variable(image).cuda()

    with torch.no_grad():
        out = model(image)[-1]
        #print("out: ", out)

    for i in range(2):
      with torch.no_grad():
        out = model(out)[-1]


    out = out.data
    #out = out.numpy()
    #out = out.transpose((0, 2, 3, 1))
    #out = out[0, :, :, :]*255.
    
    return out


if __name__ == '__main__':
    args = get_args()

    model = Generator().cuda()
    unfog_net = net.unfog_net().cuda()
    model.load_state_dict(torch.load('./weights/gen.pkl'))
    unfog_net.load_state_dict(torch.load('./weights/net.pth'))

    input_list = sorted(os.listdir(args.input_dir))
    num = len(input_list)
    t0 = time.time()
    for i in tqdm(range(num)):

        #print ('Processing image: %s'%(input_list[i]))

        img = cv2.imread(args.input_dir + input_list[i])
        #print('img_name: ', args.input_dir + input_list[i])
        img = cv2.resize(img, (720, 480))
        img = align_to_four(img)
        norain = predict(img) # 3 times
        clean_image = unfog_net(norain) # 2 times

        clean_image = clean_image.cpu().data.numpy()
        clean_image = clean_image.transpose((0, 2, 3, 1))
        clean_image = clean_image[0, :, :, :] * 255.

        img_name = input_list[i].split('.')[0]
        cv2.imwrite(args.output_dir + img_name + '.jpg', clean_image)
    
    t1 = time.time()
    print("time: ", t1 - t0)

