from utils import *
from classes import *
from _thread import *

def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Joguinho maneiro")
	clock = pygame.time.Clock()

	text, text_rect = create_text(
		"Waiting for another player",
		WIDTH // 2,
		HEIGHT // 2,
		(240, 162, 60),
		75
	)
	
	player = Player(40, 500)
	other = OtherPlayer(0, 0)

	boxes = pygame.sprite.Group()
	create_phase2(boxes)

	player.listen_thread = start_new_thread(player.listen, ())

	while True:

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
		screen.blit(text, text_rect)
		pygame.display.update()

		if len(data) > 0:
			if method == "GAME" and data == "start":
				player.network.send("GAME_START (\n\n)")
				break

	while True:
		player.network.send("GET_COINS (\n\n)")
		method, data = parser(player.data_players)
		print (data)
		if len(data) > 0:
			if method == "UPDATE_COINS":
				coins = create_coins(data)
				break

	win_player = ''
	run = True
	while run:
		clock.tick(FPS)

		coin_text, coin_rect = create_text(
			f"Coins: {player.coins_collected}",
			WIDTH // 2,
			20,
			(240, 162, 60),
			40
		)

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
		screen.blit(coin_text, coin_rect)
		pygame.display.update()

	authors, authors_rect = create_text(
		"Created by: HECTOR and KATHE",
		WIDTH // 2,
		HEIGHT // 2 - 200,
		(240, 102, 60),
		30
	)

	game_over, game_over_rect = create_text(
		"GAME OVER!",
		WIDTH // 2,
		HEIGHT // 2,
		(240, 162, 60),
		75
	)

	if win_player == player.id:
		text_final, text_final_rect = create_text(
			"YOU WIN!",
			WIDTH // 2,
			HEIGHT // 2 - 100,
			(240, 162, 90),
			75
		)
	else:
		text_final, text_final_rect = create_text(
			"YOU LOSE!",
			WIDTH // 2,
			HEIGHT // 2 - 100,
			(240, 162, 90),
			75
		)
	
	exit_text, exit_text_rect = create_text(
		"Press ESC to exit",
		WIDTH // 2,
		HEIGHT // 2 + 200,
		(240, 162, 60),
		30
	)

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
		screen.blit(authors, authors_rect)
		screen.blit(game_over, game_over_rect)
		screen.blit(text_final, text_final_rect)
		screen.blit(exit_text, exit_text_rect)
		pygame.display.update()


	pygame.quit()

if __name__ == "__main__":
	main()
