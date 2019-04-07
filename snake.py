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
			print (cabeca)
			print (str(x)+str(y))
			return True
	
	return False
	

def collide(x1, x2, y1, y2, w1, w2, h1, h2):

	if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
		return True
	else:
		return False
	
while True:
	restart = False
	
	controle = Sbot()
	altura = largura = 600


	snakeposx = [280, 280, 280, 280, 280]
	snakeposy = [280, 260, 240, 220, 200]
	dirs = lastdirs = 1
	score = 0
	
	applepos = (random.randrange(0, altura,20), random.randrange(0, largura,20))
	pygame.init()
	s=pygame.display.set_mode((altura, largura))
	pygame.display.set_caption('Snake')
	appleimage = pygame.Surface((19, 19))
	appleimage.fill((0, 255, 0))
	img = pygame.Surface((19, 19))
	img.fill((255, 0, 0))

	f = pygame.font.SysFont('Arial', 20)
	
	clock = pygame.time.Clock()
	
	while restart !=True:
		restart = False
		clock.tick(10)
		i = len(snakeposx)-1

		for e in pygame.event.get():
			if e.type == QUIT:
				ssnakeposy.exit(0)
		

		if collide(snakeposx[0], applepos[0], snakeposy[0], applepos[1], 20, 20, 20, 20):
			score+=1
			snakeposx.append(1)
			snakeposy.append(1)
			applepos=(random.randrange(0,altura,20), random.randrange(0,largura,20))
			
		
		#print(applepos)

		if morde(snakeposx, snakeposy):
			print("se mordeu")
			restart =True

		if snakeposx[0] < 0 or snakeposx[0] > largura or snakeposy[0] < 0 or snakeposy[0] > altura:
			print("Parede")
			restart = True

		i = len(snakeposx)-1
		
		while i >= 1:
			snakeposx[i] = snakeposx[i-1]
			snakeposy[i] = snakeposy[i-1]
			i -= 1
		
		#print (snakeposx)
		#print (snakeposy)

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