from flask import Flask, render_template, Response
import cv2
import os
app = Flask(__name__)

camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)
count = 0
def gen_frames(face_cascade):  # generate frame by frame from camera
    global count
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                img = frame[y:y + h, x:x + w]
                path = "Faces/" + name + "/frame" + str(count) + ".jpg"
                cv2.imwrite(path, img)
                count += 1
            #cv2.imshow("image", frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            if count >= 50:
                frame = cv2.imread("unnamed.jpg")
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                camera.release()
                return (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
try:
    os.mkdir("Faces")
except:
    pass
face_cas = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
name = input("Name of the person : ")
try:
    pth = "Faces/"+name
    os.mkdir(pth)
except:
    pass

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(face_cas), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/thankyou')
def thanks():
    """Video streaming home page."""
    return render_template('thank_you.html')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)