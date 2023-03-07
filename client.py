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


def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Joguinho maneiro")
	clock = pygame.time.Clock()

	player = Player(100, 200)
	players = {}

	boxes = pygame.sprite.Group()
	create_phase(boxes)

	player.listen_thread = start_new_thread(player.listen, ())

	run = True
	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		print("player.data_players: " + player.data_players)
		if player.data_players != "":
			data_players = player.data_players[1:-1]
			data_players = data_players.split("),(")
			players_list = [p.replace("'", "") for p in data_players]
			players_list = [p.replace(" ", "") for p in players_list]
			for p in players_list:
				p = p.split(",")
				if p != ['']:
					if p[0] != str(player.id):
						if p[0] in players:
							players[p[0]].rect.x = int(p[1])
							players[p[0]].rect.y = int(p[2])
							players[p[0]].facing_left = p[3] == "True"
							players[p[0]].w_index = int(p[4])
							players[p[0]].update()
						else:
							players[p[0]] = OtherPlayer(int(p[1]), int(p[2]))

		screen.fill(BACKGROUND)
		for i in players:
			players[i].draw(screen)

		player.update(boxes)
		player.draw(screen)
		boxes.draw(screen)
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	main()