from flask import Flask, render_template
import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/productdetails')
def productdetails():
    return render_template('productdetails.html')


@app.route('/productdetails1')
def productdetails1():
    return render_template('productdetails1.html')


@app.route('/productdetails2')
def productdetails2():
    return render_template('productdetails2.html')


@app.route('/productdetails3')
def productdetails3():
    return render_template('productdetails3.html')


@app.route('/productdetails4')
def productdetails4():
    return render_template('productdetails4.html')


@app.route('/productdetails5')
def productdetails5():
    return render_template('productdetails5.html')

@app.route('/productdetails6')
def productdetails6():
    return render_template('productdetails6.html')


@app.route('/productdetails7')
def productdetails7():
    return render_template('productdetails7.html')




#Try now 
@app.route('/trynow')
def tryNow():

    cap = cv2.VideoCapture(0)
    detector = PoseDetector()

    shirtFolderPath = "C:/Users/user/Desktop/newwwww/Virtual-Dressing-Room-main/Resources/Shirts"
    listShirts = os.listdir(shirtFolderPath)
    #print(listShirts)
    fixedRatio = 262/190  # widthOfShirt/WidthOfPoint 11 to 12
    shirtRatioHeightWidth = 581/440
    imageNumber = 0
    imgButtonRight = cv2.imread("Resources/button.png",cv2.IMREAD_UNCHANGED)
    imgButtonLeft = cv2.flip(imgButtonRight,1)
    counterRight = 0
    counterLeft = 0
    selectionSpeed = 50
    width = 1500
    height = 1080
    dim = (width, height)

    flag = True

    while flag:
        success, img = cap.read()
        if img is not None:
            frame = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            img = detector.findPose(img)
            # img = cv2.flip(img,1)
            lmlist, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
            if lmlist:
                # center = bboxInfo["center"]
                lm11 = lmlist[11][1:3]
                lm12 = lmlist[12][1:3]
                imgShirt = cv2.imread(os.path.join(shirtFolderPath,listShirts[imageNumber]),cv2.IMREAD_UNCHANGED)

                widthOfShirt = int((lm11[0]-lm12[0])*fixedRatio)
                print(widthOfShirt)
                if imgShirt is None:
                    print("None image")
                else:
                    imgShirt = cv2.resize(imgShirt,(widthOfShirt, int(widthOfShirt*shirtRatioHeightWidth)))
                currentScale = (lm11[0]-lm12[0]) / 190
                offset = int(44 * currentScale), int(48 * currentScale)

                try:
                    img = cvzone.overlayPNG(img, imgShirt, (lm12[0]-offset[0],lm12[1]-offset[1]))
                except:
                    pass

                img = cvzone.overlayPNG(img,imgButtonRight,(490,293))
                img = cvzone.overlayPNG(img, imgButtonLeft, (25, 293))

                if lmlist[16][1] < 170:
                    counterRight += 1
                    cv2.ellipse(img, (88, 360), (66, 66), 0, 0,
                                counterRight*selectionSpeed, (0, 255, 0), 20)
                    if counterRight*selectionSpeed > 360:
                        counterRight = 0
                        if imageNumber < len(listShirts)-1:
                            imageNumber += 1
                elif lmlist[15][1] > 500:
                    counterLeft += 1
                    cv2.ellipse(img, (550, 360), (66, 66), 0, 0,
                               counterLeft * selectionSpeed, (0, 255, 0), 20)
                    if counterLeft * selectionSpeed > 360:
                        counterLeft = 0
                        if imageNumber > 0:
                            imageNumber -= 1
                else:
                    counterRight = 0
                    couterLeft = 0

            cv2.imshow("archange", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyWindow("archange")

#Try now ends here


if __name__ == "__main__":
    app.run()