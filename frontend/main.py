
from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)

@app.route('/index.html')
def ind():
    return render_template('index.html')

@app.route('/about.html')
def fir():
    return render_template('about.html')


@app.route('/team.html')
def team():
    return render_template('team.html')

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
