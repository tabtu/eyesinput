#!/usr/bin/env python
#coding=utf-8
import os
#from PIL import Image, ImageDraw
import cv2

def detect_object(image):
    '''检测图片，获取人脸在图片中的坐标'''
    grayscale = cv2.CreateImage((image.width, image.height), 8, 1)
    cv2.CvtColor(image, grayscale, cv2.CV_BGR2GRAY)

    cascade = cv2.Load("data/haarcascades/haarcascade_frontalface_alt.xml")
    rect = cv2.HaarDetectObjects(grayscale, cascade, cv2.CreateMemStorage(), 1.1, 2,
        cv2.CV_HAAR_DO_CANNY_PRUNING, (20,20))

    result = []
    for r in rect:
        result.append((r[0][0], r[0][1], r[0][0]+r[0][2], r[0][1]+r[0][3]))

    return result

def process(infile):
    '''在原图上框出头像并且截取每个头像到单独文件夹'''
    image = cv2.imread(infile);
    #if image:
    faces = detect_object(image)

    im = Image.open(infile)
    path = os.path.abspath(infile)
    save_path = os.path.splitext(path)[0]+"_face"
    try:
        os.mkdir(save_path)
    except:
        pass
    if faces:
        draw = ImageDraw.Draw(im)
        count = 0
        for f in faces:
            count += 1
            draw.rectangle(f, outline=(255, 0, 0))

        drow_save_path = os.path.join(save_path,"out.jpg")
        im.save(drow_save_path, "JPEG", quality=80)
    else:
        print("Error: cannot detect faces on %s" % infile)

if __name__ == "__main__":
    process("checkFace2.jpg")