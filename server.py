from flask import Flask, render_template
from firebase import firebase
from flask_socketio import SocketIO
import time
app = Flask(__name__)
socketio = SocketIO(app)
firebase_db = firebase.FirebaseApplication('https://connection-fee80-default-rtdb.asia-southeast1.firebasedatabase.app/', None)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('get_latest_record')
def get_latest_record():
    while True:
        records = firebase_db.get('/UsersData/uxxtZrqIyjWlh6Z2yRmZpau49Aj2/readings', None)
        latest_timestamp = max(records.keys())
        latest_record = records[latest_timestamp]
        socketio.emit('latest_record', latest_record)
        time.sleep(30)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
