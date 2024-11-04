import socketio

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server.")

@sio.event
def disconnect():
    print("Disconnected from the server.")

@sio.on('add_prosumer')
def add_prosumer(data):
    print("New prosumer added: ", data)

@sio.on('add_consumer')
def add_consumer(data):
    print("New consumer added: ", data)

sio.connect('http://localhost:4000')

# Wait indefinitely to keep the client running
sio.wait()
