from classes import *
from _thread import *

FPS = 60
WIDTH = 800
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

def update_users(data, other):
	data = data[2:-2]
	data = data.split(",")
	other.rect.x = int(data[1])
	other.rect.y = int(data[2])
	other.facing_left = data[3] == "True"
	other.w_index = int(data[4])
	other.update()
	return other

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

	player = Player(100, 200)
	other = OtherPlayer(100, 200)
	coin = Coin(300, 100)

	flag = False

	boxes = pygame.sprite.Group()
	create_phase(boxes)

	player.listen_thread = start_new_thread(player.listen, ())

	while True:

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
		coin.update()
		coin.draw(screen)
		other.draw(screen)
		player.update(boxes)
		player.draw(screen)
		boxes.draw(screen)
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	main()