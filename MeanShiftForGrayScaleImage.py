#Mean Shift Segmentation for Grayscale images Image_House and Image_Hill_House

from PIL import Image
import numpy
import scipy
import math
from scipy.misc import toimage
from scipy.misc import imsave
import cv2
import random

#reading image

i = Image.open('Image_House.jpg')
# or i = Image.open('Image_Hill_House.jpg')

(width,height) = i.size

im = numpy.array(Image.open('Image_House.jpg'))
# or im = numpy.array(Image.open('Image_Hill_House.jpg'))

length=width*height

#creating rgb,xy array to save image metrics with one extra column for mark up
p=numpy.zeros(shape=(length,4), dtype=int)
pixarray=numpy.array(p)


#final array for conversion
resultArray=numpy.zeros(shape=(height,width), dtype=int)

#insering data into the feature space metrics 
z=0
for x in range (0,height-1):
    for y in range (0,width-1):
        grey=im[x,y]
        pixarray[z,0]=x
        pixarray[z,1]=y
        pixarray[z,2]=grey
        z=z+1

#thresholds
meanshift=1
hs=40
hr=20
iterValue=5

#list for adding auxiliary data
auxlist =([])


#Mean Shift performaing function
def meanShift(meanArr):
    cmplist=([])
    naList = ([])
    global pixarray
    lengthPixArray = len(pixarray)
    
    # Initializing values   
    if(meanArr=="success"):
        index = random.randint(0,lengthPixArray-1)
        xinit = pixarray[index,0]
        yinit = pixarray[index,1]
        greyinit = pixarray[index,2]
        
    else:   
        xinit = meanArr[0]
        yinit = meanArr[1]
        greyinit = meanArr[2]

    
    count=0
    xsum=0
    ysum=0
    greysum=0

    #Calculating Euclidian distance and qualifying thresholded values
    for i in range(0, lengthPixArray-1):
        dists = math.sqrt(abs((xinit-pixarray[i,0])*(yinit-pixarray[i,0])+(yinit-pixarray[i,1])*(yinit-pixarray[i,1])))
        distr = math.sqrt(abs((greyinit-pixarray[i,2])*(greyinit-pixarray[i,2])))
        if(dists<hs and distr<hr):
            cmplist.append(pixarray[i])
            (xsum)=(xsum)+pixarray[i,0]
            (ysum)=(ysum)+pixarray[i,1]
            (greysum)=(greysum)+pixarray[i,2]
            count=count+1
        else:
            naList.append(i)
            
     
    if (count==0):
        return "success"
    
    #Calculating mean     
    xmean=float(xsum/count)
    ymean=float(ysum/count)
    greymean=float(greysum/count)
    
    meandistance = math.sqrt(abs((greymean-greyinit)))
    
    #If new and original mean is less than iter
    if(meandistance<iterValue):
        for i in range(0,len(cmplist)-1):
            cmplist[i][2]=int(greymean)
            auxlist.append(cmplist[i])
        
        p=numpy.zeros(shape=(len(naList),4), dtype=int)
        tempArray=numpy.array(p)
        iterIndex=0
        for j in range(0,len(naList)-1):
            tempArray[iterIndex][0]=pixarray[naList[j]][0]
            tempArray[iterIndex][1]=pixarray[naList[j]][1]
            tempArray[iterIndex][2]=pixarray[naList[j]][2]
            iterIndex=iterIndex+1
        pixarray=tempArray
    
    #If new and original mean is less than iter        
    else:
        arr = numpy.array([xmean,ymean,greymean])
        return arr
        
    
    return "success"
    
# calling meanShift ()  function
result="success"
while(len(pixarray)>1):
    print(len(pixarray),"is length")
    result = meanShift(result)

resultArray=numpy.zeros(shape=(height,width), dtype=int)

#Displaying final reuslt
for a in range(0,len(auxlist)-1):
    resultArray[auxlist[a][0]][auxlist[a][1]] = auxlist[a][2]
    
cv2.imwrite("Image_House_Output.jpg",resultArray)