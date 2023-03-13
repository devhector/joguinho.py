import socket
from _thread import *

players = []
score = []

coins = [
	'0,20,20,False',
	'1,20,320,False',
	'2,220,170,False',
	'3,220,475,False',
	'4,430,580,False',
	'5,840,160,False',
	'6,840,300,False',
	'7,840,440,False',
	'8,840,580,False',
	'9,630,160,False',
	'10,630,300,False',
	'11,630,440,False',
	'12,630,580,False',
]

def parser(data):
	method = data.split(" ")[0]
	aux = data.split(" ")[1]
	aux = aux[2:-2]
	data = aux.split("\n")
	return method, data

def threaded_client(conn, player):
	conn.send(str(player).encode())

	while True:
		try:
			data = conn.recv(2048).decode()
			if not data:
				print(f"Jogador {player} desconectado")
				players[player] = "-42"
				break
			else:
				method, data = parser(data)

				if method == "UPDATE":
					players[player] = data

					msg = "UPDATE_USERS ("
					for _id, content in enumerate(players):
						if _id != player and content != "-42":
							msg += f"\n{content}"
					msg += "\n)"
					conn.sendall(str(msg).encode())

				if method == "GAME" and len(players) > 1:
					msg = "GAME (\nstart\n)"
					conn.send(str(msg).encode())
				
				if method == "GET_COINS":
					msg = "COINS ("
					for coin in coins:
						msg += f"\n{coin}"
					msg += "\n)"
					conn.send(str(msg).encode())

		
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

	s.listen(2)
	print("Aguardando conexão, servidor iniciado")

	player = 0
	while True:
		conn, addr = s.accept()
		print("Conectado a:", addr)

		players.append("-42")
		score.append(0)
		start_new_thread(threaded_client, (conn, player))
		player += 1

main()

