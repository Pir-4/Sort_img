__author__ = 'Valentin'

import os
import shutil
from PIL import Image,ImageChops
import sys
import argparse

def CreateParser():
    parser=argparse.ArgumentParser()
    parser.add_argument('-p1','--path1')
    parser.add_argument('-p2','--path2')

    return parser
def CheckNamespace(namespace):
    if not os.path.isdir(namespace.path1):
        print(namespace.path1 + " is not directory")
        exit(1)
    if not os.path.isdir(namespace.path2):
        print(namespace.path2 + " is not directory")
        exit(1)
    return namespace

def getListImgs(path):
    imgs = {}
    nsme_list = os.listdir(path)
    error_list = []
    for el in nsme_list:
        file = path + "/" + el
        try:
            img = Image.open(file)
            imgs.setdefault(img,file)
        except:
            error_list.append(file)

    return imgs
def Compare(dist_1, dist_2):
    print("**Compare directories**")
    list_1 = dist_1.keys()
    list_2 = dist_2.keys()
    path = []
    dist = {}
    for img1 in list_1:
        for img2 in list_2:
            try:
                if (ImageChops.difference(img1,img2).getbbox() is None):
                    path.append(dist_2.get(img2))
                    dist.setdefault(dist_1.get(img1),dist_2.get(img2))
                    print (dist_2.get(img2))
                    break
            except:
                found = True


    print("**End**")

    return path,dist
def setFoundImg(found_img,path_dir):
    path_dir = path_dir+"/"+"Found"
    if not os.path.exists(path_dir):
            os.mkdir(path_dir)

    for img in found_img:
        try:
            shutil.move(img,path_dir)
        except:
            print("Error move: "+ str(img))
    return  path_dir

def SeveCoppyFile(path,dist):
    file=open(path+"/"+"Copy.txt","a+")
    for elem in dist.keys():
        st = str(elem)+" : "+str(dist.get(elem))+"\n"
        file.write(st)
    file.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = CreateParser()
        namespace = CheckNamespace(parser.parse_args(sys.argv[1:]))
        print(namespace)
        list_1 = getListImgs(namespace.path1)
        list_2 = getListImgs(namespace.path2)
        print(namespace.path1 + " : "+str(len(list_1)))
        print(namespace.path2 + " : "+str(len(list_2)))
        found_img,dist_img = Compare(list_1,list_2)
        print("Found : "+str(len(found_img)))

        list_1.clear()
        list_2.clear()
        del list_1
        del list_2

        path_dir = setFoundImg(found_img,namespace.path2)
        SeveCoppyFile(path_dir,dist_img)