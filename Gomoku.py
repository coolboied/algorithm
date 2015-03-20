import pygame
import random
from pygame.locals import *
from sys import exit
class CellImg(pygame.Surface):
	def __init__(self,chess_color,white,black):
		pygame.Surface.__init__(self,(30,30))
		if chess_color == 0:
			pygame.draw.rect(self,pygame.Color(255,255,255), pygame.Rect((1,1),(28,28)))
		if chess_color == 1:
			self.blit(white,(1,1))
		if chess_color == 2:
			self.blit(black,(1,1))

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
			return (False,0,0)
		board.layout[j][i] = 1
		return (True,j,i)

class AI:
	def play(self, board):
		x = 0
		y = 0
		max_score = 1 
		for i in range(15):
			for j in range(15):
				if board.layout[i][j] == 0:
					AI_score = self.get_score(board,i,j,2)
					player_score = self.get_score(board,i,j,1)
					score = AI_score + player_score
					#score = 0
					if score > max_score:
						max_score = score
						x = i
						y = j
		print(max_score)
		#player_score = self.get_score(board,7,5,1)
		board.layout[x][y] = 2
		return (x,y)
					

	def get_line_score(self,line,obj, index):
		l_con_num = 0
		l_con = False

		r_con_num = 0
		r_con = False
		for i in range(1,index):
			if line[index-i] == obj:
				l_con_num = l_con_num+1
			elif line[index-i] !=obj:
				if index !=i or line[index-i] ==0:
					l_con = True 
				break
		for i in range(index,15):
			if line[i] == obj:
				r_con_num = r_con_num +1
			elif line[i] !=obj:
				if i !=14 or line[i] ==0:
					r_con = True 
				break
		con_num = l_con_num+r_con_num
		if con_num >=5:
			return 1000
		if con_num ==4 and l_con and r_con:
			return 800
		if con_num == 4 and (l_con or r_con):
			return 100
		if con_num == 3 and l_con and r_con:
			return 90
		if con_num == 3 and (l_con or r_con):
			return 60
		if con_num == 2:
			return 20
		return con_num

	def get_score(self, board, i_, j_, obj):
		line = [0 for i in range(15) ]
		for i in range(15):
			line[i] = board.layout[i_][i]
			line[j_] = obj 
		h_con_num=self.get_line_score(line,obj,j_)

		for i in range(15):
			line[i] = board.layout[i][j_]
			line[i_] = obj 
		w_con_num=self.get_line_score(line,obj,i_)

		ij_diff = i_-j_
		for i in range(15):
			j = i - ij_diff
			if j in range(15):
				line[i] = board.layout[i][j]
			else:
				line[i] = 3
		line[i_] = obj
		s1_score = self.get_line_score(line,obj,i_)

		ij_and = i_+j_
		for i in range(15):
			j = ij_and - i
			if j in range(15):
				line[i] = board.layout[i][j]
			else:
				line[i] = 3
		line[i_] = obj
		s2_score = self.get_line_score(line,obj,i_)

		score = 0
		score1 = 0

		if h_con_num > w_con_num:
			score= h_con_num
		else:
			score= w_con_num

		if s2_score > s1_score:
			score1 = s2_score
		else:
			score1 = s1_score

		if score1 > score:
			return score1
		else:
			return score

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
		pygame.display.set_caption("五子棋")
		screen = pygame.display.set_mode((480, 480), 0, 32)
		self.place_waring = 0

		white= pygame.image.load('white.jpg').convert()
		black= pygame.image.load('black.jpg').convert()

		board = Board()
		player = Player()
		ai = AI()

		while True:
			for i in range(15):
						for j in range(15):	
							cell = CellImg(board.layout[i][j],white,black)
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
						re,i,j= player.mouse_click(board,x-15,y-15)
						if not re:
							self.place_waring = 60 
						else:
							ai.play(board)

if __name__ == "__main__":

	screen = Screen()
	screen.run()
