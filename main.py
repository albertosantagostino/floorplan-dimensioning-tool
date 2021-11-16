#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrypoint
"""

import cv2
import math
import sys
import time

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askfloat

import ipdb

HV_THRESHOLD = 20

def click_event(event, x, y, flags, params):

    image = params[0]
    coordinates = params[1]
    lookup_coordinates = params[2]
    
    if event == cv2.EVENT_LBUTTONDOWN:

        if not params[4]:
            if len(coordinates) < 2:
                print(x, ' ', y)
                coordinates.append((x, y))
                image = cv2.circle(image, (x, y),
                                radius=2,
                                color=(0, 0, 255),
                                thickness=2)
                cv2.imshow('img', image)

            if len(coordinates) == 2:
                x1, y1, x2, y2 = \
                    coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1]

                orientation = ''
                if abs(x1 - x2) <= HV_THRESHOLD:
                    x2 = x1
                    orientation = 'vertical'
                elif abs(y1 - y2) <= HV_THRESHOLD:
                    y2 = y1
                    orientation = 'horizontal'
                    print("H")

                cv2.line(image, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
                cv2.imshow('img', image)

                size = askfloat(title="Set size", prompt="Size? [m]")

                if orientation == 'vertical':
                    params[3] = abs(y1-y2) / float(size)

                elif orientation == 'horizontal':
                    params[3] = abs(x1-x2) / float(size)
                params[4] = True

        else:
            if len(lookup_coordinates) < 2:
                lookup_coordinates.append((x, y))
            if len(lookup_coordinates) == 2:
                x1, y1, x2, y2 = \
                    lookup_coordinates[0][0], lookup_coordinates[0][1], lookup_coordinates[1][0], lookup_coordinates[1][1]
                orientation = ''
                if abs(x1 - x2) <= HV_THRESHOLD:
                    x2 = x1
                    real_length = abs(y2 - y1) / params[3]
                    orientation = 'vertical'
                elif abs(y1 - y2) <= HV_THRESHOLD:
                    y2 = y1
                    real_length = abs(x2 - x1) / params[3]
                    orientation = 'horizontal'
                else:
                    real_length = math.sqrt(abs(x2 - x1)**2 + abs(y2 - y1)**2) / params[3]


                if orientation == 'vertical':
                    cv2.putText(image, f'{real_length:.2f}',  (x1, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif orientation == 'horizontal':
                    cv2.putText(image, f'{real_length:.2f}',  (x2, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(image, f'{real_length:.2f}',  (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.line(image, (x1, y1), (x2, y2), color=(255, 0, 0), thickness=1)
                cv2.imshow('img', image)
                print(f"Length of segment is ~ {real_length:.2f} m")
                params[2] = []
                

def main():
    Tk().withdraw()
    #filename = askopenfilename()
    filename = ''
    try:
        image = cv2.imread(filename)
    except Exception as ex:
        print(ex)
        sys.exit(1)
    
    
    cv2.imshow('img', image)
    coordinates = []
    lookup_coordinates = []
    ratio = 0.0
    scale_set = False
    cv2.setMouseCallback('img', click_event, [image, coordinates, lookup_coordinates, ratio, scale_set])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

