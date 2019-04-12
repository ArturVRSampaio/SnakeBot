import pygame, random, sys
from pygame.locals import *
from Sbot import Sbot

def morde(snakeposx, snakeposy):
	cobrax = list(snakeposx)
	cobray = list(snakeposy)
	cabeca= str(cobrax[0])+ str(cobray[0])

	cobrax.pop(0)
	cobray.pop(0)
	y= len(cobrax)
	
	for x in range(0, y):
		if (str(cobrax[x]) + str(cobray[x]) == str(cabeca)):
			return True
	return False
	
while True:
	restart = False
	
	controle = Sbot()
	largura = 600
	
	snakeposx = [280, 280, 280, 280, 280]
	snakeposy = [280, 260, 240, 220, 200]
	dirs = lastdirs = 1
	score = 0
	
	applepos = (random.randrange(0, largura,20), random.randrange(0, largura,20))
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
		restart = False
		clock.tick(10)
		i = len(snakeposx)-1

		for e in pygame.event.get():
			if e.type == QUIT:
				sys.exit(0)
		

		if (str(snakeposx[0]) + str(snakeposy[0]) == str(applepos[0]) + str(applepos[1]) ) :
			score+=1
			snakeposx.append(1)
			snakeposy.append(1)
			applepos=(random.randrange(0,largura,20), random.randrange(0,largura,20))
			
		
		#print(applepos)

		if morde(snakeposx, snakeposy):
			print("se mordeu")
			restart =True

		if snakeposx[0] < 0 or snakeposx[0] > largura or snakeposy[0] < 0 or snakeposy[0] > largura:
			print("Parede")
			restart = True

		i = len(snakeposx)-1
		
		while i >= 1:
			snakeposx[i] = snakeposx[i-1]
			snakeposy[i] = snakeposy[i-1]
			i -= 1
		

		dirs = controle.controle(applepos, snakeposx, snakeposy, lastdirs)

		lastdirs = dirs
		
		if lastdirs==1:
			snakeposy[0] += 20
		#	print("BAIXO")
		elif lastdirs==2:
			snakeposy[0] -= 20
		#	print("CIMA")
		elif lastdirs==3:
			snakeposx[0] += 20
		#	print("DIREITA")
		elif lastdirs==6:
			snakeposx[0] -= 20
		#	print("ESQUERDA")	
		
		s.fill((0, 0, 0))	
		
		for i in range(0, len(snakeposx)):
			s.blit(img, (snakeposx[i], snakeposy[i]))
			
		s.blit(appleimage, applepos)
		t=f.render(str(score), True, (0, 255, 0))
		s.blit(t, (20, 20))
		pygame.display.update()
