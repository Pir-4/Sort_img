__author__ = 'Valentin'

import os
import shutil
from datetime import datetime
from PIL import Image,ExifTags,ImageChops
import sys
import argparse


def CreateParser():
    parser=argparse.ArgumentParser()
    parser.add_argument('-p','--path')
    parser.add_argument('-y','--year',action='store_const',const=True, default=False)
    parser.add_argument('-m','--month',action='store_const',const=True, default=False)
    parser.add_argument('-d','--day',action='store_const',const=True, default=False)
    parser.add_argument('-s','--similar',action='store_const',const=True, default=False)
    return parser
def CheckNamespace(namespace):
    if namespace.day:
        namespace.month = True
        namespace.year = True
    elif namespace.month:
        namespace.year = True
    return namespace
def FindSimilar(path):
    print("**Search for similar images**")
    list = os.listdir(path)
    error_list = []
    imgs = {}

    for el in list:
        file = path + str("/") + el
        try:
            img = Image.open(file)
            imgs.setdefault(img,file)
        except:
            error_list.append(file)

    path_imgs =[]
    copy_imgs = {}
    imgs_obj = imgs.keys()
    length = len(imgs_obj)
    for i in range(0,length-1):
        img1 = imgs_obj[i]
        for f in range(i+1,length):
            img2 = imgs_obj[f]
            try:
                if (ImageChops.difference(img1,img2).getbbox() is None):
                    print (imgs.get(imgs_obj[i]) + " : " + imgs.get(imgs_obj[f]))
                    copy_imgs.setdefault(imgs.get(imgs_obj[i]),imgs.get(imgs_obj[f]))
                    if imgs.get(imgs_obj[i]) not in path_imgs:
                        path_imgs.append(imgs.get(imgs_obj[i]))
            except:
                k=1
    imgs.clear()
    del imgs
    path = path+"/"+"Similar"
    if not os.path.exists(path):
            os.mkdir(path)

    file=open(path+"/"+"Similar.txt","a+")
    for elem in copy_imgs.keys():
        st = str(elem)+" : "+str(copy_imgs.get(elem))+"\n"
        file.write(st)
    file.close()

    for img in path_imgs:
        shutil.move(img,path)

    print("**End**")

def getDateShooting(path):
    print("**Indexing creation dates**")
    list = os.listdir(path)
    dist = {}
    error_list = []

    for el in list:
        file = path + str("/") + el
        try:
            img = Image.open(file)
            data = {
                    ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in ExifTags.TAGS
                    }
            dist.setdefault(file,datetime.strptime(data["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S"))

        except:
            error_list.append(file)

    print("**End**")
    return dist
def getNameDirectory(datetime,namespace):
    name = ""
    if namespace.day:
        name = name + str(datetime.day) + "."
    if namespace.month:
        if len(str(datetime.month)) == 1:
            name = name + "0" + str(datetime.month) + "."
        else:
            name = name + str(datetime.month) +" ."
    if namespace.year:
        name = name + str(datetime.year) + "."
    return name

def CreateDirectory(DateShooting,path,namespace):
    date = []
    for key in DateShooting.keys():
        datetime = DateShooting.get(key)
        if datetime not in date:
            date.append(datetime)

    for time in date:
        name = getNameDirectory(time,namespace)
        if not os.path.exists(path+"/"+str(name)):
            os.mkdir(path+"/"+str(name))


    return date
def getSaveDirectory(img_date,date,namespace):
    if namespace.day:
        for el in date:
            if el == img_date:
                return getNameDirectory(el,namespace)
    if namespace.month:
        for el in date:
            if el.year == img_date.year and el.month == img_date.month:
                return getNameDirectory(el,namespace)
    if namespace.year:
        for el in date:
            if el.year == img_date.year:
                return getNameDirectory(el,namespace)

def MovetoFile(path,date,DateShooting,namespace):
    print("**Sorting**")
    dist = {}
    for key in DateShooting.keys():
        dist.setdefault(key,DateShooting.get(key))

    DateShooting.clear()
    del DateShooting

    for key in dist:
        shutil.move(key,path+"/"+str(getSaveDirectory(dist.get(key),date,namespace)))
    print("**End**")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = CreateParser()
        namespace = CheckNamespace(parser.parse_args(sys.argv[1:]))
        print(namespace)
        path = namespace.path
        if os.path.isdir(path):
            if namespace.similar:
                FindSimilar(path)
            if namespace.year:
                DateShooting = getDateShooting(path)
                date = CreateDirectory(DateShooting,path,namespace)
                MovetoFile(path,date,DateShooting,namespace)
        else:
            print("is not directory")
    else:
        print("input path in directory")
