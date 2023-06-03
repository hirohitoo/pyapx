#opencv_acquire_streaming_images

import cv2
import time

vid = cv2.VideoCapture(0)

while True:

    ret, frame = vid.read()
#    frame=frame[0:600,0:800]
    #frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('USB camera', frame)
    time.sleep(1)
    if cv2.waitKey(4) & 0xFF == ord('q'):
        break


vid.release()
cv2.destroyAllWindows()

app = Flask(__name__)

@app.route('/')
#@limiter.limit("3/minute")
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        time.sleep(1)
        frame = camera.get_frame()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),mimetype='multipart/x-mixed-replace; boundary=frame')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int('8080'),debug=True) 