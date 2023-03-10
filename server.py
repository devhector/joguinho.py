import socket
from _thread import *

players = []

def threaded_client(conn, player):
	conn.send(str(player).encode())

	while True:
		try:
			data = conn.recv(2048).decode()
			if not data:
				print("Desconectado")
				players.remove(player)
				print(players)
				break
			else:
				players[player] = data
				message = [p for i, p in enumerate(players) if i != player and p != "-42"]
				print(message)
				conn.sendall(str(message).encode())
		
		except:
			break
	conn.close()

def main():

	server = "localhost"
	port = 4242

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		s.bind((server, port))
	except socket.error as e:
		print("bind erro: " + str(e))

	s.listen(4)
	print("Aguardando conexão, servidor iniciado")

	player = 0
	while True:
		conn, addr = s.accept()
		print("Conectado a:", addr)

		players.append("-42")
		start_new_thread(threaded_client, (conn, player))
		player += 1

main()

