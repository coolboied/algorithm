import sys
import re
import random

class Command:
	def __init__(self):
		self.command_list = []
		self.expess = []
		self.var = {}
		self.var_value={}
	def command_clear(self):
		self.command_list = []
	def read_var(self,exp):
		var, ex_exp = exp.split('=')
		ex_exp=ex_exp.rstrip('\n')
		self.var[var] = ex_exp
	def random_var(self):
		for key in self.var.keys():
			self.var_value[key] = Command.random_exchange(self.var[key])
		#print(self.var)
		#print(self.var_value)
	def read_expess(self,expess):
		self.expess.append(expess)

	def cover_value(self, key):
		values = Command.all_value(self.var[key])
		for value in values:
			for expess in self.expess:
				expess = re.sub(r'\{'+key+'\}',value,expess)
				command = self.create_command(expess)
				self.command_list.append(command)

	def all_value(ex_exp):
		str_split = ex_exp.split(':')
		result=[]
		if len(str_split) == 2:
			if str_split[0] == 'num':
				num_start, num_end = str_split[1].split('-',1)
				for num in range(int(num_start), int(num_end)):
					result.append(str(num))
			elif str_split[0] == 'enum':
				enums = str_split[1].split("/")
				for enum in enums:
					result.append(enum)
		return result


	def random_exchange(ex_exp):
		str_split = ex_exp.split(':')
		result=''
		if len(str_split) == 2:
			if str_split[0] == 'num':
				num_start, num_end = str_split[1].split('-',1)
				num = random.randint(int(num_start),int(num_end))
				result=str(num)

			elif str_split[0] == 'str':
				num_start = 0
				num_end = 0
				str_range = []
				tmp = str_split[1].split('-',2)
				if len(tmp) == 2:
					num_start = tmp[0]
					num_end = tmp[1]
					str_range = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
				else:
					num_start = tmp[0]
					num_end = tmp[1]
					str_range = list(tmp[2])
				num = random.randint(int(num_start), int(num_end))
				str_new = ''.join(random.sample(str_range,num))
				result=str_new
			elif str_split[0] == 'enum':
				enums = str_split[1].split("/")
				num = random.randint(0, len(enums)-1)
				result=enums[num]
			return result
		return ex_exp

	def create_command(self,command):
		#print(self.var_value)

		for key in self.var_value.keys():
			reObj = re.compile('\{'+key+'\}')
			command = reObj.sub(self.var_value[key],command)
			command=command.rstrip('\n')
		return command

	def create_command_list(self):
		for expess in self.expess:
			command = self.create_command(expess)
			self.command_list.append(command)

	def change_seq_random(command):
		command_ = re.sub(':*;$','',command)
		try:
			head, paras = command_.split(':::',1)
			para_list = paras.split(',')
			command_new = head+":::"
			while len(para_list)>0:
				index = random.randint(0,len(para_list)-1)
				command_new = command_new+para_list[index]+','
				del para_list[index]
			command_new=command_new.rstrip(',')
			command_new = command_new+';'
			return command_new
		except:
			return command

	def out_put(self,wfile="result.txt"):
		wFile = open(wfile,"w+");
		for command in self.command_list:
			wFile.write(command+'\n');

input_file = sys.argv[1]

pFile = open(input_file);

com = Command()
create_rule = -1
commands_num = 0
cover_key = '' 
case_name = ''
for line in pFile:
	try:
		head,exp = line.split(':',1)
	except:
		head = ''
		exp = ''
	if head == 'case':
		if create_rule == 0:
			for i in range(commands_num):
				com.random_var()
				com.create_command_list()
			com.out_put(wfile=case_name)
		elif create_rule == 1:
			com.random_var()
			com.cover_value(cover_key)
			com.out_put(wfile=case_name)


		com = Command()
		case_name, case_exp = exp.split(" ", 1)
		tmp1, tmp2 = case_exp.split(":",1)
		if tmp1 == 'AllCover':
			create_rule = 1
			cover_key = tmp2.rstrip('\n')
		else:
			create_rule = 0
			commands_num = int(tmp2)

	elif head == 'var':
		com.read_var(exp)
	else:
		com.read_expess(line)

if create_rule == 0:
	for i in range(commands_num):
		com.random_var()
		com.create_command_list()
elif create_rule == 1:
	com.random_var()
	com.cover_value(cover_key)
com.out_put(wfile=case_name)
	
	
pFile.close();
