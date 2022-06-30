import pygame
import random
import time

class Game():
	def __init__(self,player,draw_constants):
		pygame.init()
		self.player = player
		self.draw_constants = draw_constants

		self.obstacles = []
		self.items = []

		self.floor = pygame.Rect(0,500,800,100)
		self.cloudimg = pygame.image.load('cloud.png')
		self.heartimg = pygame.image.load('heart.png')
		self.greenheart = pygame.image.load('greenheart.png')

		self.sound1 = pygame.mixer.Sound('sound1.wav')
		self.sound2 = pygame.mixer.Sound('sound2.wav')
		self.music_bg = pygame.mixer.music.load('music.ogg')
		#pygame.mixer.music.play(-1)

		self.lifes = 8
		self.counter = 0

		self.start = time.time()
		self.stop = time.time()
		self.secondspassed = 0

	def draw(self,screen):
		pygame.font.init()
		myfont = pygame.font.SysFont('Arial', 50)

	
		pygame.draw.rect(screen,(20,200,20),self.floor)
		screen.blit(pygame.transform.scale(self.cloudimg,(800,500)),(0,0))

		self.player.draw(screen)

		for i in range(self.lifes):
			screen.blit(pygame.transform.scale(self.heartimg,(50,50)),(750-50*i,0))

		for o in self.obstacles:
			o.draw(screen)

		for item in self.items:
			item.draw(screen)

		pygame.draw.circle(screen,(255,0,0),(int(self.player.x_pos),int(self.player.y_pos)),12)

		textsurface = myfont.render("Sekunden: " + str(self.secondspassed), False, (228,148,95))
		screen.blit(textsurface,(450,50))




	def nextState(self):

		if self.lifes <= 0:
			pygame.event.post(pygame.event.Event(pygame.QUIT))


		self.stop = time.time()
		self.secondspassed = int(self.stop - self.start)


		self.counter += 1
		self.counter %= 25

		if self.counter == 7:
			self.obstacles += [Obstacle(800,random.randint(350,480),-random.randint(3,10),0,15,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))]
			if random.randint(1,2) == 1:
				self.items += [Item(800,random.randint(350,450),30,30,-random.randint(3,10),0,self.greenheart)]


		self.player.move()

		for o in self.obstacles:

			if o.collide(self.player):
				pygame.mixer.Sound.play(self.sound1)
				self.lifes -= 1
				self.obstacles.remove(o)

			if o.isGone():
				self.obstacles.remove(o)
			else:
				o.approach()

		for item in self.items:

			if item.collide(self.player):
				pygame.mixer.Sound.play(self.sound2)
				self.lifes += 1
				self.items.remove(item)

			if item.isGone():
				if item in self.items:
					self.items.remove(item)
			else:
				item.move()







class Player():
	def __init__(self,y_pos,y_vel,x_pos,width,height):
		self.y_pos = y_pos
		self.y_vel = y_vel
		self.x_pos = x_pos
		self.width = width
		self.height = height

	def move(self):
		"Calculate position of player on next frame."

		#move in direction
		self.y_pos += self.y_vel

		
		if not self.isOnFloor():
			#gravity
			self.y_vel += 0.8
		else:
			self.y_vel = 0
			self.y_pos = 500


	def jump(self):
		"Initiates jump of player."

		self.y_vel = -18

	def isOnFloor(self):
		return self.y_pos >= 500

	def draw(self,screen):
		pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.x_pos,self.y_pos-self.height,self.width,self.height))


class Obstacle():
	def __init__(self,x_pos,y_pos,x_vel,y_vel,radius,col):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.x_vel = x_vel
		self.y_vel = y_vel
		self.radius = radius
		self.col = col

	def approach(self):
		self.x_pos += self.x_vel

	def isGone(self):
		return self.x_pos + self.radius <= 0

	def draw(self,screen):
		pygame.draw.circle(screen,self.col,(self.x_pos,self.y_pos),self.radius)

	def dist(self,player):
		#gerade oben
		e1 = abs(self.y_pos - player.y_pos)

		#gerade rechts
		e2 = abs(self.x_pos - player.x_pos - player.width)

		#gerade unten
		e3 = abs(self.y_pos - player.y_pos - player.height)

		#gerade links
		e4 = abs(self.x_pos - player.x_pos)

		return (e1,e2,e3,e4)

	def collide(self,player):
		return self.x_pos < player.x_pos + 2*self.radius and self.x_pos + player.width > player.x_pos and self.y_pos < player.y_pos + 2*self.radius and player.height +self.y_pos > player.y_pos



class Item():
	def __init__(self,x_pos,y_pos,height,width,x_vel,y_vel,image):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.height = height
		self.width = width
		self.x_vel = x_vel
		self.y_vel = y_vel
		self.image = image

	def move(self):
		self.x_pos += self.x_vel
		self.y_pos += self.y_vel

	def isGone(self):
		return self.x_pos + self.width <= 0

	def draw(self,screen):
		screen.blit(pygame.transform.scale(self.image,(self.width,self.height)),(self.x_pos,self.y_pos))

	def collide(self,player):

		if not self.x_pos <= player.x_pos + player.width:
			return False
		else:
			if not self.y_pos +self.height >= player.y_pos - player.height:
				return False
			else:
				if self.y_pos +self.height <= player.y_pos:
					return True
				else:
					return False

		"""
		a = self.x_pos + self.width <= player.x_pos
		b = self.y_pos + self.height <= player.y_pos
		c = self.x_pos >= player.x_pos + player.width
		d = self.y_pos >= player.y_pos + player.height

		return not a and not b and not c and not d
		"""


		"""

		sol = [False,False,False,False]

		xc = self.x_pos
		yc = self.y_pos
		r = self.radius

		#gerade oben
		x1 = player.x_pos
		x2 = player.x_pos + player.width
		y1 = player.y_pos
		y2 = player.y_pos

		s1 = solve_quadratic(x1**2-2*x1*x2+x2**2+y1**2-2*y1*y2+y2**2  ,  2*x1*x2-2*x1*xc-2*x2**2+2*x2*xc + 2*y1*y2-2*y1*yc-2*y2**2+2*y2*yc  ,  x2**2-2*x2**2*xc+xc**2 + y2**2-2*y2**2*yc+yc**2 - r**2)

		if not s1 == "nS":
			if (s1[0] >= 0 and s1[0] <= 1) or (s1[1] >= 0 and s1[1] <= 1):
				sol[0] = True



		#gerade rechts
		x1 = player.x_pos + player.width
		x2 = player.x_pos + player.width
		y1 = player.y_pos
		y2 = player.y_pos + player.height

		s2 = solve_quadratic(x1**2-2*x1*x2+x2**2+y1**2-2*y1*y2+y2**2  ,  2*x1*x2-2*x1*xc-2*x2**2+2*x2*xc + 2*y1*y2-2*y1*yc-2*y2**2+2*y2*yc  ,  x2**2-2*x2**2*xc+xc**2 + y2**2-2*y2**2*yc+yc**2 - r**2)

		if not s2 == "nS":
			if (s2[0] >= 0 and s2[0] <= 1) or (s2[1] >= 0 and s2[1] <= 1):
				sol[1] = True




		#gerade unten
		x1 = player.x_pos + player.width
		x2 = player.x_pos
		y1 = player.y_pos + player.height
		y2 = player.y_pos + player.height

		s3 = solve_quadratic(x1**2-2*x1*x2+x2**2+y1**2-2*y1*y2+y2**2  ,  2*x1*x2-2*x1*xc-2*x2**2+2*x2*xc + 2*y1*y2-2*y1*yc-2*y2**2+2*y2*yc  ,  x2**2-2*x2**2*xc+xc**2 + y2**2-2*y2**2*yc+yc**2 - r**2)

		if not s3 == "nS":
			if (s3[0] >= 0 and s3[0] <= 1) or (s3[1] >= 0 and s3[1] <= 1):
				sol[2] = True




		#gerade links
		x1 = player.x_pos
		x2 = player.x_pos
		y1 = player.y_pos + player.height
		y2 = player.y_pos

		s4 = solve_quadratic(x1**2-2*x1*x2+x2**2+y1**2-2*y1*y2+y2**2  ,  2*x1*x2-2*x1*xc-2*x2**2+2*x2*xc + 2*y1*y2-2*y1*yc-2*y2**2+2*y2*yc  ,  x2**2-2*x2**2*xc+xc**2 + y2**2-2*y2**2*yc+yc**2 - r**2)

		if not s4 == "nS":
			if (s4[0] >= 0 and s4[0] <= 1) or (s4[1] >= 0 and s4[1] <= 1):
				sol[3] = True




		print(s1,s2,s3,s4)
		return True in sol

		"""






		"""
		a = self.x_pos + 2*self.radius < player.x_pos
		b = self.y_pos + 2*self.radius < player.y_pos
		c = self.x_pos > player.x_pos + player.width
		d = self.y_pos > player.y_pos + player.height

		return not a and not b and not c and not d
		"""


		"""
		return self.dist(player)[0] < self.radius and (self.dist(player)[1] < self.radius or self.dist(player)[3] < self.radius) or \
		self.dist(player)[1] < self.radius and (self.dist(player)[0] < self.radius or self.dist(player)[2] < self.radius) or \
		self.dist(player)[2] < self.radius and (self.dist(player)[1] < self.radius or self.dist(player)[3] < self.radius) or \
		self.dist(player)[3] < self.radius and (self.dist(player)[0] < self.radius or self.dist(player)[2] < self.radius)
		"""

		"""
		return self.dist(player)[0] < self.radius and self.dist(player)[1] < self.radius or \
		self.dist(player)[1] < self.radius and self.dist(player)[2] < self.radius or \
		self.dist(player)[2] < self.radius and self.dist(player)[3] < self.radius or \
		self.dist(player)[3] < self.radius and self.dist(player)[0] < self.radius
		"""



def solve_quadratic(a,b,c):
	D = b**2 - 4*a*c
	if D < 0:
		return "nS"
	else:
		return ((-b + D**(1/2)) / (2*a) , (-b - D**(1/2)) / (2*a))

print(solve_quadratic(1,0,0))


"""
"test"
player = Player(0,0)
player.jump()

for i in range(25):
	player.move()

	print(int(player.y_pos)*"#")
"""

