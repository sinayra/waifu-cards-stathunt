import os
import cv2
import numpy as np
from PIL import Image
from pathlib import Path

def imagesDifference( imageA, imageB ):
    A = list(Image.open(imageA, r'r').convert(r'RGB').getdata())
    B = list(Image.open(imageB, r'r').convert(r'RGB').getdata())
    if (len(A) != len(B)): return -1
    diff = []
    for i in range(0, len(A)):
        diff += [abs(A[i][0] - B[i][0]), abs(A[i][1] - B[i][1]), abs(A[i][2] - B[i][2])]
    return (sum(diff) / len(diff))

def main():
    path, dirs, files = next(os.walk("./stats"))
    file_count = len(files)
    
    for i in range(file_count):
        first_stat = './stats/stat' + str(i) + '.webp'
        first_stat_path = Path(first_stat)
        if first_stat_path.exists():
            for j in range(i + 1, file_count):
                second_stat = './stats/stat' + str(j) + '.webp'
                second_stat_path = Path(second_stat)

                if second_stat_path.exists():
                    difference = imagesDifference(first_stat, second_stat)

                    if difference < 5:
                        os.remove(second_stat)

main()