import numpy as np
import cv2
#img = cv2.imread('1.png')
#cv2.imshow('sample', img)
#cv2.waitKey(0)

namefile = open('names/symbol_name.csv')
lines = namefile.readlines()
for i, line in enumerate(lines):
    print(i, line)
