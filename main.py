import cv2
import Person
import math
import time

personSize1 = 60000
personSize2 = 100000
persons = []
contours = []
pid = 1
tp = 0
body_cascade = cv2.CascadeClassifier('C:/Users/Aldo/Documents/Aldo/Trabajo/haarcascade_fullbody.xml')
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture(0)
_, rawImage = cap.read()
firstFrame = cv2.cvtColor(rawImage, cv2.COLOR_BGR2GRAY)
w = cap.get(3)
h = cap.get(4)
rangeLeft = int(1.1 * (w / 3))
rangeRight = int(1.9 * (w / 3))
midLine = int(2.5 * (w / 6))
xCenter = 0
new = True
test = ()
color = []
p = 0


def people_tracking(rects):
    global pid
    global xCenter
    global yCenter
    global w
    global h
    global new
    for x, y, w, h in rects:
        new = True
        xCenter = x + w / 2
        yCenter = y + h / 2
    inActiveZone = xCenter in range(rangeLeft, rangeRight)
    for index, p in enumerate(persons):
        dist = math.sqrt((xCenter - p.getX()) ** 2 + (yCenter - p.getY()) ** 2)
        if type(w) is type(test) or type(h) is type(test):
            break
        if dist <= int(w) / 2 and dist <= int(h) / 2:
            if inActiveZone:
                new = False
                if abs(p.getX() - xCenter) > w*0.15:
                    if p.getTest():
                        p.stoptimer()
                else:
                    if p.add2timer() == 3:
                        global tp
                        print("[INFO] persona " + str(index + 1) + " estatica")
                        tp += 1
                        color[index] = 1
                        p.stoptimer()
                p.updateCoords(xCenter, yCenter)
                break
            else:
                print("[INFO] persona " + str(index + 1) + " removida")
                persons.pop(index)
                color.pop(index)
    if new is True and inActiveZone:
        print("[INFO] nueva persona " + str(pid))
        color.append(0)
        p = Person.Person(pid, xCenter, yCenter, time.time())
        persons.append(p)
        pid += 1


while True:

    print(color)
    _, rawImage = cap.read()
    if rawImage is not None:
        gray = cv2.cvtColor(rawImage, cv2.COLOR_BGR2GRAY)
        #bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        found, w = hog.detectMultiScale(gray, winStride=(8, 8), padding=(32, 32), scale=1.05)
        personContours = []
        for x, y, w, h in found:
            helper = []
            if personSize1 < (w*h) < personSize2:
                helper.append(x)
                helper.append(y)
                helper.append(w)
                helper.append(h)
                personContours.append(helper)
        contours = personContours
        people_tracking(contours)

    (grabbed, rawImage) = cap.read()
    img = rawImage.copy()
    i = 0
    for x, y, w, h in contours:
        try:
            if color[i] == 1:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            i += 1
        except:
            continue

    cv2.imshow('People', img)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        print("[INFO] " + str(tp) + " personas vieron tu anuncio.")
        break
