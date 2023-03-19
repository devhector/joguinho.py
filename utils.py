from classes import *

FPS = 60
WIDTH = 900
HEIGHT = int(WIDTH * 0.8)
BACKGROUND = (100, 42, 0)

def create_phase(boxes):
	for bx in range(0, 400, 70):
		boxes.add(Box(bx, 300))
	for bx in range(400, 800, 70):
		boxes.add(Box(bx, 600))
	boxes.add(Box(330, 230))
	boxes.add(Box(320, 480))
	boxes.add(Box(360, 500))
	boxes.add(Box(100, 70))

def create_phase2(boxes):
	#caixas inferiores esquerda
	for bx in range(40, 170, 70):
		boxes.add(Box(bx, 670))
	
	#caixas superiores direita 
	for bx in range(650, 900, 70):
		boxes.add(Box(bx, 110))

	#caixas a esquerda
	for by in range(110, 680, 70):
		boxes.add(Box(580, by))

	b = [3, 7]
	for i in b:
		a = (i * 70) + 180
		boxes.add(Box(860, a))
		boxes.add(Box(650, a))

	boxes.add(Box(40, 410))
	boxes.add(Box(40, 110))
	boxes.add(Box(240, 260))
	boxes.add(Box(240, 565))
	boxes.add(Box(450, 670))
	boxes.add(Box(510, 180))

def update_users(data, other):
	try:
		data = data[2:-2]
		data = data.split(",")
		other.rect.x = int(data[1])
		other.rect.y = int(data[2])
		other.facing_left = data[3] == "True"
		other.w_index = int(data[4])
	except:
		pass
	return other


def create_coins(data):
	coins = pygame.sprite.Group()
	try:
		for coin in data:
			coin = coin.split(",")
			print("id coin: ", coin[0])
			coins.add(
				Coin(
					int(coin[1]),
					int(coin[2]),
					int(coin[0]),
					coin[3] == "True"
					)
			)
	except:
		pass
	return coins

def parser(data):
	if data == "":
		return "", []
	method = data.split(" ")[0]
	data = data.split(" ")[1]
	data = data[2:-2]
	if "\n" in data:
		data = data.split("\n")
	return method, data

def create_text(text, x, y, color, size):
	font = pygame.font.Font("./assets/font/Bubble_Bobble.ttf", size)
	text = font.render(text, True, color)
	textRect = text.get_rect()
	textRect.center = (x, y)
	return text, textRect