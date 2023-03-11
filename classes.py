import pygame, numpy, socket

class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "localhost"
		self.port = 4242
		self.addr = (self.server, self.port)
		self.id = self.connect()

	def connect(self):
		try:
			self.client.connect(self.addr)
			return self.client.recv(2048).decode()
		except:
			pass

	def send(self, data):
		try:
			self.client.send(str(data).encode())
		except socket.error as e:
			print(e)

	def listen(self):
		try:
			return self.client.recv(2048).decode()
		except socket.error as e:
			print(e)


class Sprite(pygame.sprite.Sprite):
	def __init__(self, image, x, y):
		super().__init__()
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
	
	def update(self):
		pass

	def draw(self, screen):
		screen.blit(self.image, self.rect)

class Player(Sprite):
	def __init__(self, x, y):
		super().__init__("./assets/p1_front.png", x, y)
		self.stand_image = self.image
		self.j_image = pygame.image.load("./assets/p1_jump.png")

		self.w_cycle = [
			pygame.image.load(f"./assets/p1_walk{i:0>2}.png") 
			for i in range(1, 12)
		]

		self.w_index = 0
		self.facing_left = False
		self.network = Network()
		self.id = self.network.id

		self.vsp = 0
		self.speed = 4
		self.gravity = 1
		self.j_speed = 20
		self.data_players = ""
		self.prev_key = pygame.key.get_pressed()

	def walk_animation(self):
		self.image = self.w_cycle[self.w_index]
		if self.facing_left:
			self.image = pygame.transform.flip(self.image, True, False)

		if self.w_index >= len(self.w_cycle) - 1:
			self.w_index = 0
		else:
			self.w_index += 1

	def jump_animation(self):
		self.image = self.j_image
		if self.facing_left:
			self.image = pygame.transform.flip(self.image, True, False)

	def update(self, boxes):
		hsp = 0
		onground = self.check_collision(0, 1, boxes)

		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT]:
			self.facing_left = True
			self.walk_animation()
			hsp -= self.speed
		elif key[pygame.K_RIGHT]:
			self.facing_left = False
			self.walk_animation()
			hsp = self.speed
		else:
			self.image = self.stand_image
			if self.facing_left:
				self.image = pygame.transform.flip(self.image, True, False)

		if key[pygame.K_UP] and onground:
			self.vsp = -self.j_speed

		if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
			if self.vsp < -5:
				self.vsp = -5
		
		if key[pygame.K_ESCAPE]:
			pygame.quit()
			exit()

		self.prev_key = key

		if self.vsp < 10 and not onground:
			self.jump_animation()
			self.vsp += self.gravity

		if self.vsp > 0:
			self.vsp += 0

		self.move(hsp, self.vsp, boxes)

	def move (self, x, y, boxes):
		dx = x
		dy = y

		while self.check_collision(0, dy, boxes):
			dy -= numpy.sign(y)
		while self.check_collision(dx, dy, boxes):
			dx -= numpy.sign(x)
		self.rect.move_ip([dx, dy])

		msg = "UPDATE ("
		msg += f"\n{self.id},{self.rect.x},{self.rect.y},{self.facing_left},{self.w_index}"
		msg += "\n)"

		self.network.send(msg)

	def check_collision(self, x, y, ground):
		self.rect.move_ip([x, y])
		collide = pygame.sprite.spritecollideany(self, ground)
		self.rect.move_ip([-x, -y])
		return collide
	
	def listen(self):
		while True:
			self.data_players = self.network.listen()


class OtherPlayer(Sprite):
	def __init__(self, x, y):
		super().__init__("./assets/p1_front.png", x, y)
		self.stand_image = self.image
		self.j_image = pygame.image.load("./assets/p1_jump.png")

		self.w_cycle = [
			pygame.image.load(f"./assets/p1_walk{i:0>2}.png")
			for i in range(1, 12)
		]

		self.w_index = 0
		self.old_w_index = 0
		self.old_y = self.rect.y
		self.facing_left = False
	
	def update(self):
		if self.old_w_index != self.w_index:
			self.walk_animation()
			self.old_w_index = self.w_index
		else:
			self.image = self.stand_image

		if self.old_y != self.rect.y:
			self.jump_animation()
			self.old_y = self.rect.y
		
	def walk_animation(self):
		self.image = self.w_cycle[self.w_index]
		if self.facing_left:
			self.image = pygame.transform.flip(self.image, True, False)

	def jump_animation(self):
		self.image = self.j_image
		if self.facing_left:
			self.image = pygame.transform.flip(self.image, True, False)

class Box(Sprite):
	def __init__(self, x, y):
		super().__init__("./assets/boxAlt.png", x, y)