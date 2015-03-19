import pygame
import random
from pygame.locals import *
from sys import exit
class CellImg(pygame.Surface):
	def __init__(self,chess_color):
		pygame.Surface.__init__(self,(30,30))
		if chess_color == 0:
			pygame.draw.rect(self,pygame.Color(155,155,55), pygame.Rect((1,1),(28,28)))
		if chess_color == 1:
			pygame.draw.rect(self,pygame.Color(255,255,55), pygame.Rect((1,1),(28,28)))
		if chess_color == 2:
			pygame.draw.rect(self,pygame.Color(255,155,55), pygame.Rect((1,1),(28,28)))

class MessBox(pygame.Surface):
	def __init__(self,mess):
		pygame.Surface.__init__(self,(400,30))
		self.font = pygame.font.SysFont("arial", 20);
		w,h = self.font.size(mess)
		pygame.draw.rect(self,pygame.Color(255,255,255), pygame.Rect((2,2),(396,26)))
		self.blit( self.font.render(mess, True, (0, 0, 0)), ((400-w)/2, (30-h)/2))

class Player:
	def mouse_click(self,board,x,y):
		i = x//30
		j = y//30
		if board.layout[j][i] != 0:
			return False
		board.layout[j][i] = 1
		return True

class AI:
	def play(self, board):
		i = random.randint(0, 14)
		j = random.randint(0, 14)
		board.layout[j][i] = 2

class Board(pygame.Surface):
	def __init__(self):
		pygame.Surface.__init__(self,(450,450))
		self.layout = [[0 for col in range(15)] for row in range(15)]

	def is_in_borad(self,x,y):
		if x-15>0 and y-15>0 and x<465 and y < 465:
			return True
		return False
		

class Screen:
	def run(self):
		pygame.init()
		screen = pygame.display.set_mode((480, 480), 0, 32)
		pygame.display.set_caption("五子棋")

		self.place_waring = 0

		board = Board()
		player = Player()
		ai = AI()

		while True:
			for i in range(15):
						for j in range(15):	
							cell = CellImg(board.layout[i][j])
							board.blit(cell,(30*j,30*i))

			screen.blit(board,(15,15))
			if self.place_waring > 0 :
				mess_box = MessBox("can't place here")
				screen.blit(mess_box,(40,400))
				self.place_waring = self.place_waring - 1
				#print("warning", self.place_waring)
			pygame.display.update()

			event = pygame.event.poll()
			if event.type == QUIT:
				exit()
			if event.type == MOUSEBUTTONUP:
				print(event)
				if event.button == 1:
					x,y = event.pos
					if board.is_in_borad(x,y):
						if not player.mouse_click(board,x-15,y-15):
							self.place_waring = 60 
						else:
							ai.play(board)

screen = Screen()
screen.run()
