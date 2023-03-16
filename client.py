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


def get_coins(data):
	coins = pygame.sprite.Group()
	try:
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

	boxes = pygame.sprite.Group()
	create_phase2(boxes)

	player.listen_thread = start_new_thread(player.listen, ())

	while True:
		player.network.send("GET_COINS (\n\n)")
		method, data = parser(player.data_players)
		print (data)
		if len(data) > 0:
			if method == "UPDATE_COINS":
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

		player.network.send("GAME (\n\n)")
		method, data = parser(player.data_players)
		screen.fill(BACKGROUND)
		screen.blit(text, textRect)
		pygame.display.update()

		if len(data) > 0:
			if method == "GAME" and data == "start":
				break

	win_player = ''
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
			if method == "GAME_OVER":
				win_player = data[0]
				run = False
		else:
			other.rect.x = WIDTH + 50
			other.rect.y = HEIGHT + 50

		screen.fill(BACKGROUND)
		other.update(coins)
		other.draw(screen)
		player.update(boxes, coins)
		player.draw(screen)
		coins.update()
		coins.draw(screen)
		boxes.draw(screen)
		pygame.display.update()

	font2 = pygame.font.Font("./assets/font/Bubble_Bobble.ttf", 30)
	created_text = font2.render("Created by: HECTOR and KATHE", True, (240, 102, 60))
	text = font.render(f"GAME OVER!", True, (240, 162, 60))

	if win_player == player.id:
		text_final = font.render(f"YOU WIN!", True, (240, 162, 90))
	else:
		text_final = font.render(f"YOU LOSE!", True, (240, 162, 90))
	
	text2 = font.render("PRESS ESC TO QUIT", True, (240, 162, 60))
	textRect = text.get_rect()
	textRect2 = text2.get_rect()
	textRectFinal = text_final.get_rect()
	textRectCreated = created_text.get_rect()

	textRectCreated.center = (WIDTH // 2, HEIGHT // 2 - 200)
	textRectFinal.center = (WIDTH // 2, HEIGHT // 2 - 100)
	textRect.center = (WIDTH // 2, HEIGHT // 2)
	textRect2.center = (WIDTH // 2, HEIGHT // 2 + 100)

	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			pygame.quit()
			quit()
		screen.fill(BACKGROUND)
		screen.blit(created_text, textRectCreated)
		screen.blit(text, textRect)
		screen.blit(text_final, textRectFinal)
		screen.blit(text2, textRect2)
		pygame.display.update()


	pygame.quit()

if __name__ == "__main__":
	main()
