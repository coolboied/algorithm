import os

#皇后位置
q_place =[
		(0,-1),
		(0,0),
		(0,0),
		(0,0),
		(0,0),
		(0,0),
		(0,0),
		(0,0),
		]

def is_able(x,y, num):
	for i in range(num):
		x_,y_ = q_place[i]
#是否同行
		if x==x_:
			return False
#是否同列
		if y==y_:
			return False
#是否同斜线
		if (x-x_)==(y-y_) or (x-x_) == (y_-y):
			return False
	return True

def input_(num):
	x_,y_ = q_place[num]
	if x_ == 0 and y_ == 0:
		x_1,y_1 = q_place[num-1]
		x_=x_1
		y=y_1
	for i in range(x_,8):
		start_y = 0 
		if i == x_:
			start_y = y_+1
		for j in range(start_y,8):
			if is_able(i,j,num):
				return (i,j)
	return(-1,-1)

def show_result():
	for i in range(8):
		for j in range(8):
			if (i,j) in q_place:
				print('q',end = '')
			else:
				print('_',end = '')
		print()



num = 0
result_num = 1
while True:
	x,y = input_(num)
	if x == -1:
		if num == 0:
			break
		q_place[num] = (0,0)
		num = num-1
	else:
		#print(num,'has been put',x,y)
		q_place[num] = (x,y)
		num = num+1
	if num == 8:
		num = 7
		print('result_num',result_num)
		result_num=result_num+1
		show_result()

