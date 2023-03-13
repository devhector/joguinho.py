from classes import *
from _thread import *

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
	data = data[2:-2]
	data = data.split(",")
	other.rect.x = int(data[1])
	other.rect.y = int(data[2])
	other.facing_left = data[3] == "True"
	other.w_index = int(data[4])
	other.update()
	return other

def get_coins(data):
	coins = pygame.sprite.Group()
	for coin in data:
		coin = coin.split(",")
		coins.add(
			Coin(
					int(coin[1]),
					int(coin[2]),
					int(coin[0]),
					coin[3] == "True"
				)
		)
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

def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Joguinho maneiro")
	clock = pygame.time.Clock()

	font = pygame.font.Font("./assets/font/Bubble_Bobble.ttf", 75)
	text = font.render("Waiting for another player", True, (240, 162, 60))
	textRect = text.get_rect()
	textRect.center = (WIDTH // 2, HEIGHT // 2)

	player = Player(40, 500)
	other = OtherPlayer(0, 0)

	flag = False

	boxes = pygame.sprite.Group()
	create_phase2(boxes)

	player.listen_thread = start_new_thread(player.listen, ())

	while True:
		player.network.send("GET_COINS (\n\n)")
		method, data = parser(player.data_players)
		print (data)
		if len(data) > 0:
			if method == "COINS":
				coins = get_coins(data)
				break

	while True:

		print("data players: ", player.data_players)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			pygame.quit()
			quit()

		msg = "GAME (\n\n)"
		player.network.send(msg)
		method, data = parser(player.data_players)
		screen.fill(BACKGROUND)
		screen.blit(text, textRect)
		pygame.display.update()

		if len(data) > 0:
			if method == "GAME" and data == "start":
				break

	run = True
	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		method, data = parser(player.data_players)

		if len(data) > 0:
			if method == "UPDATE_USERS":
				other = update_users(data, other)
		else:
			other.rect.x = WIDTH + 50
			other.rect.y = HEIGHT + 50

		screen.fill(BACKGROUND)
		other.draw(screen)
		player.update(boxes)
		player.draw(screen)
		coins.update()
		coins.draw(screen)
		boxes.draw(screen)
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	main()