from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room

app=Flask(__name__)
app.config['SECRET KEY'] = 'secret!'
socketio = SocketIO(app, logger=True, engineio_logger=True)
app.run(debug=True)
socketio.run(app)

@app.route('/',methods=['GET','POST'])
def index():
	return render_template("default.html")

@app.route('/user',methods=['GET','POST'])
def user():
	username=request.args.get("username")
	roomid=request.args.get("roomid")
	return render_template("user.html",username=username,roomid=roomid)

@socketio.on('send_message')
def handleMessage(data):
	# print('Message: '+ msg)
	# send(msg, broadcast=True)
	app.logger.info("{} has sent message to the room {} : {}".format(data['username'],data['room'],data['message']))
	socketio.emit('receive_message',data,room=data['room'])
	print(data['room'])
	# return render_template("user.html",username=username)

@socketio.on('join_room')
def handleJoinRoom(data):
	app.logger.info("{} has joined the room {}".format(data['username'],data['room']))
	join_room(data['room'])
	socketio.emit('join_room_announcement',data,room=data['room'])

# if __name__ == '__main__':
	# socketio.run(app)


