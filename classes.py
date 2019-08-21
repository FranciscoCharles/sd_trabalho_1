#modulo de dados
import pyrebase
import time
from datetime import datetime
import urllib3
class Usuario(object):
	def __init__(self, bd):
		self.bd = bd
		self.data = {'nome' : None,
					'password' : None,
					'adm': None,
					'id' : None}
	def create_user(self, nome=None, password=None, prioridade=True, id=None):
		now = datetime.now()
		#now.year, now.month, now.day, now.hour, now.minute, now.second
		if id == None:
			id = str(now.day)+str(now.month)+str(now.year)+str(now.hour)+str(now.minute)+str(now.second)
			self.get_id_valide()
		self.data = {
					'nome' : nome,
					'password' : password,
					'adm': prioridade,
					'id' : id}
	def copy(self):
		user = Usuario(self.bd)
		user.data = self.data.copy()
		return user
	def add(self):
		self.bd.child().child('usuarios').child(self.data['id']).set(self.data)
	def update(self):
		id = self.data['id']
		del self.data['id']
		self.bd.child().child('usuarios').child(id).update(self.data)
		self.data['id'] = id
	def remove(self):
		self.bd.child().child('usuarios').child(self.data['id']).remove()
	def show_user(self):
		for id,name in self.get_all_users():
			print('user: ',name,' id: ',id)
	def get_all_users(self):
		lista  = self.bd.child().child('usuarios').get().each()
		if lista:
			return [(i.key(),i.val()['nome']) for i in lista]
		return None
	def get_user(self):
		for user in self.bd.child().child('usuarios').get().each():
			dados = user.val()
			if (dados['id'] == self.data['id']) and (dados['password'] == self.data['password']):
				self.data = dados.copy()
				return True
		return False
	def user_authentication(self):
		lista  = self.bd.child().child('usuarios').get().each()
		if lista:
			for i in lista:
				data = i.val()
				if (i.key() == self.data['id']) and (data['password'] == self.data['password']):
					return True
		return False
	def get_id_valide(self):
		while self.user_id_exists() and (self.data['id']==None):
			now = datetime.now()
			self.data['id'] = str(now.day)+str(now.month)+str(now.year)+str(now.hour)+str(now.minute)+str(now.second)
	def user_id_exists(self):
		lista  = self.bd.child().child('usuarios').get()
		keys = [obj.key() for obj in lista.each()]
		return self.data['id'] in keys
	
class Livro(object):

	def __init__(self, bd):
		self.bd = bd
		self.data = {
					'nome' : None,
					'autor' : None,
					'qt_paginas' : None,
					'ano' : None,
					'id': None,
					'qt_total': None,
					'disponivel': None}
					
	def create_book(self, titulo=None, autor=None,qt_paginas=None, ano=None,qt_total=None,disponivel=None,id=None):
		now = datetime.now()
		if id == None:
			id = str(now.day)+str(now.month)+str(now.year)+str(now.hour)+str(now.minute)+str(now.second)
		self.data = {
					'titulo' : titulo,
					'autor' : autor,
					'qt_paginas' : qt_paginas,
					'ano' : ano,
					'id': id,
					'qt_total': qt_total,
					'disponivel': disponivel}
	def copy(self):
		book = Livro()
		book.data = self.data.copy()
		return book
	def add(self):
		self.bd.child().child('livros').child(self.data['id']).set(self.data)
	def update(self):
		id = self.data['id']
		del self.data['id']
		self.bd.child().child('livros').child(id).update(self.data)
		self.data['id'] = id
	def remove(self):
		self.bd.child().child('livros').child(self.data['id']).remove()
	def show_book(self):
		for id,title in self.get_all_books():
			print('book: ',title,' id: ',id)
	def get_all_books(self):
		lista  = self.bd.child().child('livros').get().each()
		if lista:
			return [(i.key(),i.val()['titulo']) for i in lista]
		return None
	def book_id_exists(self):
		lista  = self.bd.child().child('livros').get()
		keys = [obj.key() for obj in lista.each()]
		return self.data['id'] in keys
	def get_book(self):
		lista  = self.bd.child().child('livros').get().each()
		if lista:
			for i in lista:
				data = i.val()
				if (i.key() == self.data['id']):
					return self.copy()
		return None
if __name__ == '__main__':
	pass
	