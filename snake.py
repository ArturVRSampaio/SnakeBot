import pygame, random, sys
from pygame.locals import *
from Sbot import Sbot

def morde(snakepos):
	cobra = list(snakepos)
	cabeca= str(cobra[0][0])+ str(cobra[1][0])
	
	for x in range(1, len(cobra)-1):
		if (str(cobra[0][x]) + str(cobra[1][x]) == str(cabeca)):
			return True
	return False
	
while True:
	restart = False
	
	controle = Sbot()
	largura = 600
	
	
	snakepos = [[280, 280, 280 ], [280, 260, 240]]
	
	dirs = lastdirs = 1
	score = 0
	
	applepos = [(random.randrange(0, largura,20)), (random.randrange(0, largura,20))]
	pygame.init()
	s=pygame.display.set_mode((largura, largura))
	pygame.display.set_caption('Snake')
	appleimage = pygame.Surface((19, 19))
	appleimage.fill((0, 255, 0))
	img = pygame.Surface((19, 19))
	img.fill((255, 0, 0))

	f = pygame.font.SysFont('Arial', 20)
	
	clock = pygame.time.Clock()
	
	while (restart !=True):
		#print("loop")
		restart = False
		clock.tick(10)
		i = len(snakepos)-1

		for e in pygame.event.get():
			if e.type == QUIT:
				sys.exit(0)
		


		if (str(applepos[0])+ str(applepos[1]) == str(snakepos[0][0]) + str(snakepos[1][0])):
			score+=1
			snakepos.append(0)
			snakepos[0].append(0)
			snakepos[1].append(0)
			applepos = [(random.randrange(0, largura,20)), (random.randrange(0, largura,20))]
			#print(applepos)
		
		if morde(snakepos):
			print("se mordeu")
			restart =True

		if snakepos[0][0] < 0 or snakepos[0][0] > largura or snakepos[1][0] < 0 or snakepos[1][0] > largura:
			print("Parede")
			restart = True

		i = len(snakepos)
		while i >= 1:
			snakepos[0][i] = snakepos[0][i-1]
			snakepos[1][i] = snakepos[1][i-1]
			i -= 1

		dirs = controle.controle(applepos, snakepos, lastdirs)

		lastdirs = dirs
		
		if lastdirs==1:
			snakepos[1][0] += 20
		#	print("BAIXO")
		elif lastdirs==2:
			snakepos[1][0] -= 20
		#	print("CIMA")
		elif lastdirs==3:
			snakepos[0][0] += 20
		#	print("DIREITA")
		elif lastdirs==6:
			snakepos[0][0] -= 20
		#	print("ESQUERDA")	
		
		s.fill((0, 0, 0))	
				

		for i in range(0, len(snakepos[0])):
			s.blit(img, (snakepos[0][i], snakepos[1][i]))


		s.blit(appleimage,(applepos[0],applepos[1]))
		t=f.render(str(score), True, (0, 255, 0))
		s.blit(t, (20, 20))
		pygame.display.update()
