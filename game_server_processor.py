import socket
import threading




class Client:
	def __init__(self, port=2700):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_ip = "localhost"
		self.server_port = port
		self.server_socket.connect((self.server_ip, self.server_port))		


	def send(self, data):
		self.server_socket.send(data.encode("utf-8"))

	def receive(self):
		return self.server_socket.recv(1024).decode("utf-8")
	
	def close(self):
		self.server_socket.close()

	def __del__(self):
		self.server_socket.close()

	def __repr__(self):
		return f"Client(ip={self.server_ip}, port={self.server_port})"
	
	def __enter__(self):
		return self



class GameClient(Client):
	def __init__(self, port=2700):
		super().__init__(port)

	def cl_join(self, username):
		self.send(f"cl_join {username}")

	
	def cl_leave(self, username):
		self.send(f"cl_leave {username}")

	def cl_move(self, username, direction):
		self.send(f"cl_move {username} {direction}")

	def sv_start(self):
		self.send("sv_start")

	def sv_stop(self):
		self.send("sv_stop")

	def sv_pause(self):
		self.send("sv_pause")

	def sv_resume(self):
		self.send("sv_resume")

	def sv_restart(self):
		self.send("sv_restart")

	def sv_info(self):
		self.send("sv_info")
		self.server_socket.settimeout(1)
		data = None
		try:
			data = self.receive()
			data = data.split(" ")
			data = {"status": data[0], "p1": data[1], "p2": data[2], "p1pos": data[3], "p2pos": data[4], "p1score": data[5], "p2score": data[6], "p1x": data[7], "p1y": data[8], "p2x": data[9], "p2y": data[10], "ballx": data[11], "bally": data[12]}
		except socket.timeout:
			data = "No data received"
		return data
	
