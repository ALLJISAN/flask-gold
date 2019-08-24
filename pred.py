import os,subprocess
import json
import cv2
import numpy as np
def predict(imgName):
    img=cv2.imread("./static/photo/{}".format(imgName))
    x,y,z=img.shape
    rand=np.random.random(1)
    img=img[int((x-50)*rand[0]):int((x-50)*rand[0]+51),int((y-50)*rand[0]):int((y-50)*rand[0]+51)]
    cv2.imwrite("./static/photo/neo-{}".format(imgName),img)

    template="python3 ./lable_image.py --graph=./output/retraiin_graph.pb --labels=./output/output_labels.txt --input_layer=Placeholder --output_layer=final_result --image=./static/photo/{}".format("neo-"+imgName)

    p=subprocess.Popen(template,shell=True,stdout=subprocess.PIPE)
    out=p.stdout.readlines()
    message=[]
    for line in out:
        message.append(str(line)[2:len(line)-2])
    return message
    
