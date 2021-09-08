import cv2
import numpy as np
import glob
import os



path_txt = "D:/data_motor/motobike/TNMT_GAPA/train/labels_txt"
path_output = "D:/data_motor/motobike/TNMT_GAPA/train/labels_plate"
for file in os.listdir(path_txt):
    name = file
    output=""    
    p1 = ()
    p2 = ()
    p3 = ()
    p4 = ()
    with open(path_txt+ '/' + name, "r") as stream:
                    print(name)
                    if name !="classes.txt" :
                        for line in stream.readlines():
                                        line = line.strip()
                                        coord = line.split(" ")
                                        a = coord[0]
                                        # print(a,type(a))
                                        if a=='0' :
                                            p1 = (float(coord[1]),float(coord[2]))
                                        if a=='1' :
                                            p2 = (float(coord[1]),float(coord[2]))
                                        if a=='2' :
                                            p3 = (float(coord[1]),float(coord[2]))
                                        if a=='3' :
                                            p4 = (float(coord[1]),float(coord[2]))
                        xtl = min(p1[0],p3[0])
                        ytl = min(p1[1],p2[1])
                        xbr = max(p2[0],p4[0])
                        ybr = max(p3[1],p4[1])
                        # print(p1)
                        # print(p2)   
                        x = str(abs(xtl+(xbr-xtl)/2))
                        y = str(abs(ytl+(ybr-ytl)/2))
                        w = str(abs(xbr-xtl))
                        h = str(abs(ybr-ytl))
                        class_num ="0"
                        output = "{} {} {} {} {}\n".format(class_num, x, y, w, h)
                        print(output)
                        with open(path_output + '/' + name, 'w') as stream_out:
                                stream_out.write(output)
                        stream_out.close()
    stream.close()                

print("done")
