from tkinter import*
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from classes import Usuario,Livro
from database import BD_FireBase
ALTURA_PADRAO = 2
LARGURA_PADRAO = 40
TAMANHO_BORDA_BOTAO = 8
TIPO_BORDA_BOTAO = RIDGE
COR_FUNDO = '#105e74'
FONTE_PADRAO = ("Comic Sans MS",15,"bold")
ALTURA_ENTRY_PADRAO = 8
diretorio_imagens = 'images/'

Bd = BD_FireBase()
user = Usuario(Bd.banco)
livro = Livro(Bd.banco)


class Gerenciador(tk.Tk):

	def __init__(self,*args,**wargs):
	
		tk.Tk.__init__(self,*args,**wargs)
		tk.Tk.iconbitmap(self,default = diretorio_imagens+'icone.ico' )
		tk.Tk.wm_title(self, 'SDLIB version 1.0.15082019-pt-br')
		tk.Tk.background='black'
		self.auto = self
		self.container = Frame(self)
		self.container.pack(side='top',fill='both',expand=True)
		self.container.grid_rowconfigure(0,weight=1)
		self.container.grid_columnconfigure(0,weight=1)
		
		self.TELAS = [Login, MenuPrincipal, MenuLivros, MenuUsuarioAdm,
					LivroAdicionar, LivroAtualizar, LivroBuscar, LivroRemover,
					UsuarioAdmAdd, UsuarioAdmGerenciarDados,UsuarioAdmTrocarSenha,
					Sobre]
		
		self.frames = {}
		
		for tela in (self.TELAS):
			frame = tela(self.container,self)
			self.frames[tela] = frame
			frame.grid(row=0,column=0,stick='nsew')
		self.show_frame(Login)
		
	def show_frame(self,count):
		self.atualizar(count)
		frame = self.frames[count]
		frame.tkraise()
	def atualizar(self,count):
		self.TELAS.remove(count)
		self.TELAS.append(count)
		del self.frames[count]
		frame = count(self.container,self)
		self.frames[count] = frame
		frame.grid(row=0,column=0,stick='nsew')
#tela de login
class Login(Frame):
	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		
		logo = PhotoImage(file=diretorio_imagens+"icone.png")
		self.frame_logo = Frame(self,bg=COR_FUNDO,pady=10)
		self.frame_logo.pack()
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		
		self.frame_usuario = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame_usuario.pack()
		self.login = Label(self.frame_usuario,border=2,relief=RIDGE,text="Login : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.senha = Label(self.frame_usuario,border=2,relief=RIDGE,text="Senha : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		
		self.entrada_login = Entry(self.frame_usuario,width=40)
		self.entrada_senha = Entry(self.frame_usuario,width=40,show="*",)
		
		self.login.grid(row=0,column=0)
		self.senha.grid(row=1,column=0)
		
		self.entrada_login.grid(row=0,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_senha.grid(row=1,column=1,ipady=ALTURA_ENTRY_PADRAO)
		
		self.frame_botoes = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame_botoes.pack()
		self.botao_entrar = Button(self.frame_botoes,border=8,relief=RAISED,font=FONTE_PADRAO, text = "Entrar", width=LARGURA_PADRAO//3,bg='#f0f0f0',command = lambda:self.valida_dados(controler),activebackground='green')
		self.botao_entrar.grid(row=0,column=0)
		self.botao_fechar = Button(self.frame_botoes,border=8,relief=RAISED,font=FONTE_PADRAO, text = "Fechar", width=LARGURA_PADRAO//3,bg='#f0f0f0',command = self.quit, activebackground='green')
		self.botao_fechar.grid(row=0,column=2)
		self.botao_sobre = Button(self.frame_botoes,border=8,relief=RAISED,font=FONTE_PADRAO, text="Sobre", command= lambda: controler.show_frame(Sobre),width=LARGURA_PADRAO//3,bg='#f0f0f0')
		self.botao_sobre.grid(row=0,column=1,padx=10)
		self.botao_entrar.bind('<Enter>',self.btentrar_muda_cor)
		self.botao_entrar.bind('<Leave>',self.btentrar_padrao)
		self.botao_fechar.bind('<Enter>',self.btfechar_muda_cor)
		self.botao_fechar.bind('<Leave>',self.btfechar_padrao)
		self.botao_sobre.bind('<Enter>',self.btsobre_muda_cor)
		self.botao_sobre.bind('<Leave>',self.btsobre_padrao)
		
	def btentrar_padrao(self,event):
		self.botao_entrar["background"] = '#f0f0f0'
	def btentrar_muda_cor(self,event):
		self.botao_entrar["background"] = 'green'
	def btfechar_padrao(self,event):
		self.botao_fechar["background"] = '#f0f0f0'
	def btfechar_muda_cor(self,event):
		self.botao_fechar["background"] = 'green'
	def btsobre_padrao(self,event):
		self.botao_sobre["background"] = '#f0f0f0'
	def btsobre_muda_cor(self,event):
		self.botao_sobre["background"] = 'green'
	def valida_dados(self,controler):
		global user
		try:
			login = self.entrada_login.get()
			senha = self.entrada_senha.get()
			user.data['id'] = login
			user.data['password'] = senha
			if(login=='' and senha==''):
				messagebox.showwarning("Aviso", "Preencha os Campos")
			elif(login==''):
				messagebox.showwarning("Aviso", "Preencha o Campo Login")
			elif(senha==''):
				messagebox.showwarning("Aviso", "Preencha o Campo Senha")
			elif(user.user_authentication()):
				user.get_user()
				messagebox.showinfo("Acesso", user.data['nome']+" seja bem vindo ao nosso sistema.")
				controler.show_frame(MenuPrincipal)
			else:
				self.limpar_campos()
				messagebox.showerror("Erro", "Login ou Senha Invalidos")
		except:
			messagebox.showerror("Erro", "Ops...Ocorreu um erro!\nVerifique sua conecao com a internet!")
	def limpar_campos(self):
		self.entrada_senha.delete(0, END)
#tela de menus
class MenuPrincipal(Frame):

	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		logo = PhotoImage(file=diretorio_imagens+"icone.png")
		self.frame_logo = Frame(self,bg=COR_FUNDO,pady=10)
		self.frame_logo.pack()
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		self.frame_menu = Frame(self, bg = COR_FUNDO,pady=20)
		self.frame_menu.pack()
		self.botao_usuario = Button(self.frame_menu,border=TAMANHO_BORDA_BOTAO,relief=TIPO_BORDA_BOTAO, text = "Menu Usuarios",width = LARGURA_PADRAO,height=ALTURA_PADRAO,command = lambda:controler.show_frame(MenuUsuarioAdm),activebackground='green',font=FONTE_PADRAO)
		self.botao_livros = Button(self.frame_menu,border=TAMANHO_BORDA_BOTAO,relief=TIPO_BORDA_BOTAO, text = "Menu Livros",width = LARGURA_PADRAO,height=ALTURA_PADRAO,command = lambda:controler.show_frame(MenuLivros),activebackground='green',font=FONTE_PADRAO)
		self.botao_voltar = Button(self.frame_menu,border=TAMANHO_BORDA_BOTAO,relief=TIPO_BORDA_BOTAO, text = "Sair",width = LARGURA_PADRAO,height=ALTURA_PADRAO,command = lambda:controler.show_frame(Login),activebackground='green',font=FONTE_PADRAO)
		self.botao_usuario.pack()
		self.botao_livros.pack()
		self.botao_voltar.pack()
		self.botao_usuario.bind('<Enter>',self.btusuario_muda_cor)
		self.botao_usuario.bind('<Leave>',self.btusuario_padrao)
		self.botao_livros.bind('<Enter>',self.btlivros_muda_cor)
		self.botao_livros.bind('<Leave>',self.btlivros_padrao)
		self.botao_voltar.bind('<Enter>',self.btvoltar_muda_cor)
		self.botao_voltar.bind('<Leave>',self.btvoltar_padrao)
		
	def btusuario_padrao(self,event):
		self.botao_usuario["background"] = '#f0f0f0'
	def btusuario_muda_cor(self,event):
		self.botao_usuario["background"] = 'green'
	def btlivros_padrao(self,event):
		self.botao_livros["background"] = '#f0f0f0'
	def btlivros_muda_cor(self,event):
		self.botao_livros["background"] = 'green'
	def btvoltar_padrao(self,event):
		self.botao_voltar["background"] = '#f0f0f0'
	def btvoltar_muda_cor(self,event):
		self.botao_voltar["background"] = 'green'
class MenuLivros(Frame):

	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		logo = PhotoImage(file=diretorio_imagens+"icone_livro.png")		
		self.frame_logo = Frame(self,bg=COR_FUNDO,padx=200,pady=50)
		self.frame_logo.grid(row=0,column=0)
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		self.frame_menu = Frame(self, bg = COR_FUNDO,pady=80)
		self.frame_menu.grid(row=0,column=1)
		self.botao_adcionar = Button(self.frame_menu,border=TAMANHO_BORDA_BOTAO,relief=RAISED, text = "Adcionar",width = LARGURA_PADRAO,height=ALTURA_PADRAO,command = lambda:controler.show_frame(LivroAdicionar),activebackground='green',font=FONTE_PADRAO,highlightcolor='GREEN')		
		self.botao_atualizar = Button(self.frame_menu,border=TAMANHO_BORDA_BOTAO,relief=RAISED, text = "Gerenciar dados",width = LARGURA_PADRAO,height=ALTURA_PADRAO,command = lambda:controler.show_frame(LivroAtualizar),activebackground='green',font=FONTE_PADRAO)
		self.botao_remover = Button(self.frame_menu,border=TAMANHO_BORDA_BOTAO,relief=RAISED, text = "Realizar devolução",width = LARGURA_PADRAO,height=ALTURA_PADRAO,command = lambda:controler.show_frame(LivroRemover),activebackground='green',font=FONTE_PADRAO)
		self.botao_voltar = Button(self.frame_menu,border=TAMANHO_BORDA_BOTAO,relief=RAISED, text = "Voltar",width = LARGURA_PADRAO,height=ALTURA_PADRAO,command = lambda:controler.show_frame(MenuPrincipal),activebackground='green',font=FONTE_PADRAO)
		self.botao_adcionar.pack()
		self.botao_atualizar.pack()
		self.botao_remover.pack()
		self.botao_voltar.pack()
		#eventos
		self.botao_adcionar.bind('<Enter>',self.btadd_muda_cor)
		self.botao_adcionar.bind('<Leave>',self.btadd_padrao)
		self.botao_atualizar.bind('<Enter>',self.btatualizar_muda_cor)
		self.botao_atualizar.bind('<Leave>',self.btatualizar_padrao)
		self.botao_remover.bind('<Enter>',self.btremover_muda_cor)
		self.botao_remover.bind('<Leave>',self.btremover_padrao)
		self.botao_voltar.bind('<Enter>',self.btvoltar_muda_cor)
		self.botao_voltar.bind('<Leave>',self.btvoltar_padrao)
		
	def btadd_padrao(self,event):
		self.botao_adcionar["background"] = '#f0f0f0'
	def btadd_muda_cor(self,event):
		self.botao_adcionar["background"] = 'green'
	def btatualizar_padrao(self,event):
		self.botao_atualizar["background"] = '#f0f0f0'
	def btatualizar_muda_cor(self,event):
		self.botao_atualizar["background"] = 'green'
	def btremover_padrao(self,event):
		self.botao_remover["background"] = '#f0f0f0'
	def btremover_muda_cor(self,event):
		self.botao_remover["background"] = 'green'
	def btvoltar_padrao(self,event):
		self.botao_voltar["background"] = '#f0f0f0'
	def btvoltar_muda_cor(self,event):
		self.botao_voltar["background"] = 'green'
#telas de funcionalidades de usuario
class MenuUsuarioAdm(Frame):

	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		logo = PhotoImage(file=diretorio_imagens+"icone_usuario.png")		
		self.frame_logo = Frame(self,bg=COR_FUNDO,padx=200,pady=50)
		self.frame_logo.grid(row=0,column=0)
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		self.frame_menu = Frame(self, bg = COR_FUNDO,pady=80)
		self.frame_menu.grid(row=0,column=1)
		self.botao_adcionar = Button(self.frame_menu,border=TAMANHO_BORDA_BOTAO,relief=TIPO_BORDA_BOTAO, text = "Adcionar",width = LARGURA_PADRAO,height=ALTURA_PADRAO,command = lambda:controler.show_frame(UsuarioAdmAdd),activebackground='green',font=FONTE_PADRAO)
		self.botao_gerenciar = Button(self.frame_menu,border=TAMANHO_BORDA_BOTAO,relief=TIPO_BORDA_BOTAO, text = "Gerenciar dados",width = LARGURA_PADRAO,height=ALTURA_PADRAO,command = lambda:controler.show_frame(UsuarioAdmGerenciarDados),activebackground='green',font=FONTE_PADRAO)
		self.botao_voltar = Button(self.frame_menu,border=TAMANHO_BORDA_BOTAO,relief=TIPO_BORDA_BOTAO, text = "Voltar",width = LARGURA_PADRAO,height=ALTURA_PADRAO,command = lambda:controler.show_frame(MenuPrincipal),activebackground='green',font=FONTE_PADRAO)
		self.botao_adcionar.pack()
		self.botao_gerenciar.pack()
		self.botao_voltar.pack()
		
class UsuarioAdmAdd(Frame):
	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		
		logo = PhotoImage(file=diretorio_imagens+"icone_user_add.png")		
		self.frame_logo = Frame(self,bg=COR_FUNDO,pady=50)
		self.frame_logo.pack()
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		
		self.frame = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame.pack()
		
		self.nome = Label(self.frame,border=2,relief=RIDGE,text="Nome : ",width=int(LARGURA_PADRAO/2),font=FONTE_PADRAO)
		self.password = Label(self.frame,border=2,relief=RIDGE,text="Password : ",width=int(LARGURA_PADRAO/2),font=FONTE_PADRAO)
		self.repete_password = Label(self.frame,border=2,relief=RIDGE,text="Repita o Password : ",width=int(LARGURA_PADRAO/2),font=FONTE_PADRAO)
		
		self.entrada_nome = Entry(self.frame,width=50)
		self.entrada_password = Entry(self.frame,width=50,show='*')
		self.entrada_repete_password = Entry(self.frame,width=50,show='*')
		
		self.nome.grid(row=0,column=0)
		self.password.grid(row=1,column=0)
		self.repete_password.grid(row=2,column=0)
		
		self.entrada_nome.grid(row=0,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_password.grid(row=1,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_repete_password.grid(row=2,column=1,ipady=ALTURA_ENTRY_PADRAO)
		
		self.frame_adm = Frame(self,pady=10)
		self.frame_adm.pack()
		
		self.admtmp = IntVar()
		self.adm = True
		self.administrador = Radiobutton(self.frame_adm,text="Administrador",padx = 20,value=1,variable=self.admtmp)
		self.administrador.select()
		self.administrador.pack(side = LEFT)
		self.simples = Radiobutton(self.frame_adm,text="Usuario Simples",padx = 20,value=2,variable=self.admtmp)
		self.simples.pack(side = LEFT)
		
		self.frame_botoes = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame_botoes.pack()
		self.botao_salvar = Button(self.frame_botoes,border=8,relief=RAISED,font=FONTE_PADRAO, text = "Salvar",width = int(LARGURA_PADRAO/3),command = lambda:self.valida_dados(controler),activebackground='green',bg='#f0f0f0')
		self.botao_salvar.grid(row=0,column=0)
		self.botao_cancelar = Button(self.frame_botoes,border=8,relief=RAISED,font=FONTE_PADRAO, text = "Cancelar",width = int(LARGURA_PADRAO/3),command = lambda:controler.show_frame(MenuUsuarioAdm),activebackground='green',bg='#f0f0f0')
		self.botao_cancelar.grid(row=0,column=10)
		
		
	def valida_dados(self, controler):
		global user
		
		nome = self.entrada_nome.get()
		password = self.entrada_password.get()
		rpassword = self.entrada_repete_password.get()
		user.data['password'] = password
		
		if self.admtmp.get() == 1:
			self.adm = True
		else:
			self.adm = False
			
		
		if(nome=='' and password=='' and rpassword==''):
			messagebox.showwarning("Aviso", "Preencha os Campos")
		elif(nome==''):
			messagebox.showwarning("Aviso", "Preencha o Nome!")
		elif(password==''):
			messagebox.showwarning("Aviso", "Preencha o Password!")
		elif(rpassword==''):
			messagebox.showwarning("Aviso", "repita o Password!")
		elif(password != rpassword):
			messagebox.showwarning("Aviso", "passwords diferem!")
		else:
			messagebox.showinfo("Sucesso","Usuario criado com sucesso.")
			user.create_user(nome,password)
			user.data['adm'] = self.adm
			user.add()
			controler.show_frame(MenuUsuarioAdm)
class UsuarioDevolucao(Frame):
	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		
		logo = PhotoImage(file=diretorio_imagens+"icone_usuario.png")		
		self.frame_logo = Frame(self,bg=COR_FUNDO,pady=50)
		self.frame_logo.pack()
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		
		self.frame = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame.pack()
		
		self.nome = Label(self.frame,border=2,relief=RIDGE,text="Nome : ",width=int(LARGURA_PADRAO/2),font=FONTE_PADRAO)
		self.password = Label(self.frame,border=2,relief=RIDGE,text="Password : ",width=int(LARGURA_PADRAO/2),font=FONTE_PADRAO)
		self.repete_password = Label(self.frame,border=2,relief=RIDGE,text="Repita o Password : ",width=int(LARGURA_PADRAO/2),font=FONTE_PADRAO)
		
		self.entrada_nome = Entry(self.frame,width=50)
		self.entrada_password = Entry(self.frame,width=50,show='*')
		self.entrada_repete_password = Entry(self.frame,width=50,show='*')
		
		self.nome.grid(row=0,column=0)
		self.password.grid(row=1,column=0)
		self.repete_password.grid(row=2,column=0)
		
		self.entrada_nome.grid(row=0,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_password.grid(row=1,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_repete_password.grid(row=2,column=1,ipady=ALTURA_ENTRY_PADRAO)
		
		self.frame_botoes = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame_botoes.pack()
		self.botao_salvar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Salvar",width = int(LARGURA_PADRAO/3),command = lambda:self.valida_dados(controler),activebackground='green')
		self.botao_salvar.grid(row=0,column=0)
		self.botao_cancelar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Cancelar",width = int(LARGURA_PADRAO/3),command = lambda:self.limpar_campos(controler),activebackground='green')
		self.botao_cancelar.grid(row=0,column=10)
		
	def valida_dados(self, controler):
		global user
		
		nome = self.entrada_nome.get()
		password = self.entrada_password.get()
		rpassword = self.entrada_repete_password.get()
		user.data['password'] = password
		user.data['adm'] = True
		
		if(nome=='' and password=='' and rpassword==''):
			messagebox.showwarning("Aviso", "Preencha os Campos")
		elif(nome==''):
			messagebox.showwarning("Aviso", "Preencha o Nome!")
		elif(password==''):
			messagebox.showwarning("Aviso", "Preencha o Password!")
		elif(rpassword==''):
			messagebox.showwarning("Aviso", "repita o Password!")
		elif(password != rpassword):
			messagebox.showwarning("Aviso", "passwords diferem!")
		else:
			messagebox.showinfo("Sucesso","Usuario criado com sucesso.")
			user.create_user(nome,password)
			user.add()
			controler.show_frame(MenuUsuarios)
class MenuUsuarioComum(Frame):
	def __init__(self,parent,controler):
		pass
class UsuarioComumAdd(Frame):
	def __init__(self,parent,controler):
		pass
class UsuarioComumPedido(Frame):
	def __init__(self,parent,controler):
		pass
class UsuarioComumRenovar(Frame):
	def __init__(self,parent,controler):
		pass
class UsuarioAdmGerenciarDados(Frame):
	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		self.controler = controler
		logo = PhotoImage(file=diretorio_imagens+"icone_usr_conf.png")		
		self.frame_logo = Frame(self,bg=COR_FUNDO,padx=100,pady=100)
		self.frame_logo.grid(row=0,column=0)
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		
		self.frame = Frame(self, bg = COR_FUNDO,padx=50,pady=50)
		self.frame.grid(row=0,column=1)
		self.frame_form = Frame(self.frame, bg = COR_FUNDO,pady=10)
		self.frame_form.grid(row=0,column=1)
		self.id = Label(self.frame_form,border=2,relief=RIDGE,text="ID : ",font=FONTE_PADRAO,width=10)
		self.id.grid(row=0,column=0)
		self.entrada_id = Entry(self.frame_form,width=30)
		self.entrada_id.grid(row=0,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.nome = Label(self.frame_form,border=2,relief=RIDGE,text="Nome : ",font=FONTE_PADRAO,width=10)
		self.nome.grid(row=1,column=0)
		self.entrada_nome = Entry(self.frame_form,width=30)
		self.entrada_nome.grid(row=1,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.botao_buscar = Button(self.frame_form,border=2,relief=RAISED,text="Buscar",width=10, command=self.buscar_usuario,font=("Comic Sans MS",12,"bold"))
		self.botao_buscar.grid(row=1,column=2)
		
		self.frame_tabela = Frame(self.frame, bg = COR_FUNDO,padx=0,pady=10)
		self.frame_tabela.grid(row=1,column=1)
		self.label1 = Label(self.frame_tabela,border=2,relief=RIDGE,text="Resultado",font=FONTE_PADRAO,width=10)
		self.label1.grid(row=0,column=0)
		
		self.dataCols = ['ID','Nome']
		self.tree = ttk.Treeview(self.frame_tabela,columns=self.dataCols, show='headings')
		self.tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
		#diminue a largura da coluna
		self.tree.column("ID",minwidth=30,width=100)
		self.tree.column("Nome",minwidth=100,width=200)
		# Barras de rolagem
		ysb = ttk.Scrollbar(self.frame_tabela,orient=VERTICAL, command=self.tree.yview)
		xsb = ttk.Scrollbar(self.frame_tabela,orient=HORIZONTAL, command=self.tree.xview)
		self.tree['yscroll'] = ysb.set
		self.tree['xscroll'] = xsb.set
		ysb.grid(row=1, column=1, sticky=tk.N + tk.S)
		xsb.grid(row=2, column=0, sticky=tk.E + tk.W)
		# Define o textos do cabeçalho (nome em maiúsculas)
		for c in self.dataCols:
			self.tree.heading(c, text=c.title())
		self.tree.bind('<Button>',self.item_atual)
		self.frame_botao = Frame(self.frame,bg = COR_FUNDO,padx=0,pady=10)
		self.frame_botao.grid(row=3,column=1)
		#place_forget()
		self.mostarbt = False
		self.botao_voltar = Button(self.frame_botao,border=2,relief=TIPO_BORDA_BOTAO,text="Voltar",width=10, command=lambda:self.voltar(controler),font=("Comic Sans MS",11,"bold"))
		self.botao_voltar.grid(row=0,column=2)
		#2182019203132
	def voltar(self,controler):
		controler.show_frame(MenuUsuarioAdm)
	def item_atual(self,event):
		if self.tree.selection():
			if not self.mostarbt:
				self.botao_atualizar = Button(self.frame_botao,border=2,relief=TIPO_BORDA_BOTAO,text="Trocar senha",width= 10, command=self.trocar_senha,font=("Comic Sans MS",11,"bold"))
				self.botao_atualizar.grid(row=0,column=0)
				self.botao_remover = Button(self.frame_botao,border=2,relief=TIPO_BORDA_BOTAO,text="Remover",width=10, command=self.remover_usuario,font=("Comic Sans MS",11,"bold"))
				self.botao_remover.grid(row=0,column=1)
			self.mostarbt = True
		else:
			if self.mostarbt:
				self.botao_atualizar.destroy()
				self.botao_remover.destroy()
				self.mostarbt = False
	def buscar_usuario(self):
		global user
		user_id = self.entrada_id.get()
		user_nome = self.entrada_nome.get()
		#print(self.tree.selection())
		#print(self.tree.focus())
		#print(self.tree.index(self.tree.focus()))
		#print(self.tree.get_children(self.tree.index(self.tree.focus())))
		#print(self.tree.get_children([self.tree.selection()])['values'])
		#item = self.tree.item(self.tree.focus())['values']
		#print(item)
		#self.tree.delete(self.tree.focus())
		if ((not self.tree.selection()) or self.tree.get_children()) and self.mostarbt:
			self.botao_atualizar.destroy()
			self.botao_remover.destroy()
			self.mostarbt = False
		for i in self.tree.get_children():
			self.tree.delete(i)
		for id,nome in user.get_all_users():
			if (user_nome or user_id) and ((id==user_id) or (user_nome in nome)):
				self.tree.insert('', 'end', values  = [id,nome])
	def remover_usuario(self):
		global user
		user.data['id'],user.data['nome'] = self.tree.item(self.tree.focus())['values']
		self.tree.delete(self.tree.focus())
		user.remove()
		messagebox.showinfo("Comfirmação", "Remoção realizada com sucesso!")
	def trocar_senha(self):
		global user
		user.data['id'] = self.tree.item(self.tree.focus())['values'][0]
		user.get_user_not_password()
		self.controler.show_frame(UsuarioAdmTrocarSenha)
class UsuarioAdmTrocarSenha(Frame):
	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		
		logo = PhotoImage(file=diretorio_imagens+"icone_usr_conf.png")
		self.frame_logo = Frame(self,bg=COR_FUNDO,pady=50)
		self.frame_logo.pack()
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		
		self.frame = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame.pack()
		Label(self.frame,border=2,relief=RIDGE,text='Trocar Senha',width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.senha = Label(self.frame,border=2,relief=RIDGE,text='Senha : ',width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.rsenha = Label(self.frame,border=2,relief=RIDGE,text='repita a senha : ',width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.senha.grid(row=0,column=0)
		self.rsenha.grid(row=1,column=0)
		
		self.entrada_senha = Entry(self.frame,width=80)
		self.entrada_rsenha = Entry(self.frame,width=80)
		
		self.entrada_senha.grid(row=0,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_rsenha.grid(row=1,column=1,ipady=ALTURA_ENTRY_PADRAO)
		
		self.frame_botoes = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame_botoes.pack()
		self.botao_comfirmar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Trocar",width = int(LARGURA_PADRAO/3),command = lambda:self.valida_dados(controler),activebackground='green')
		self.botao_comfirmar.grid(row=0,column=0)
		self.botao_cancelar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Cancelar",width = int(LARGURA_PADRAO/3),command = lambda:controler.show_frame(MenuUsuarioAdm),activebackground='green')
		self.botao_cancelar.grid(row=0,column=10)
		
	def valida_dados(self, controler):
		global user
		senha = self.entrada_senha.get()
		rsenha = self.entrada_rsenha.get()
		
		if(senha=='' and rsenha==''):
			messagebox.showwarning("Aviso", "Preencha os Campos.")
		elif(senha==''):
			messagebox.showwarning("Aviso", "Digite a nova Senha.")
		elif(rsenha==''):
			messagebox.showwarning("Aviso", "Repita a nova Senha.")
		elif(senha==rsenha):
			user.get_user_not_password()
			user.data['password'] = senha
			user.update()
			messagebox.showinfo("Sucesso", user.data['nome']+"Sua senha foi atualizada.")
			controler.show_frame(MenuUsuarioAdm)
		else:
			messagebox.showerror("Erro", "Senhas diferentes!")
		
#telas de funcionalidades de livros
class LivroAdicionar(Frame):
	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		
		logo = PhotoImage(file=diretorio_imagens+"icone_livro.png")		
		self.frame_logo = Frame(self,bg=COR_FUNDO,pady=50)
		self.frame_logo.pack()
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		
		self.frame = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame.pack()
		
		self.titulo = Label(self.frame,border=2,relief=RIDGE,text="Titulo : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.autor = Label(self.frame,border=2,relief=RIDGE,text="Autor : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.qtd_paginas = Label(self.frame,border=2,relief=RIDGE,text="Qtd paginas : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.ano = Label(self.frame,border=2,relief=RIDGE,text="Ano : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.qtd = Label(self.frame,border=2,relief=RIDGE,text="qtd livros : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		
		self.entrada_titulo = Entry(self.frame,width=50)
		self.entrada_autor = Entry(self.frame,width=50)
		self.entrada_qtd_paginas = Entry(self.frame,width=50)
		self.entrada_ano = Entry(self.frame,width=50)
		self.entrada_qtd = Entry(self.frame,width=50)
		
		self.titulo.grid(row=0,column=0)
		self.autor.grid(row=1,column=0)
		self.qtd_paginas.grid(row=2,column=0)
		self.ano.grid(row=3,column=0)
		self.qtd.grid(row=4,column=0)
		
		self.entrada_titulo.grid(row=0,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_autor.grid(row=1,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_qtd_paginas.grid(row=2,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_ano.grid(row=3,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_qtd.grid(row=4,column=1,ipady=ALTURA_ENTRY_PADRAO)
		
		self.frame_botoes = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame_botoes.pack()
		self.botao_salvar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Salvar",width = int(LARGURA_PADRAO/3),command = lambda:self.valida_dados(controler),activebackground='green',bg= '#f0f0f0')
		self.botao_salvar.grid(row=0,column=0)
		self.botao_cancelar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Cancelar",width = int(LARGURA_PADRAO/3),command = lambda:self.limpar_campos(controler),activebackground='green',bg= '#f0f0f0')
		self.botao_cancelar.grid(row=0,column=10)
		
		self.botao_salvar.bind('<Enter>',self.btsalvar_muda_cor)
		self.botao_salvar.bind('<Leave>',self.btsalvar_padrao)
		self.botao_cancelar.bind('<Enter>',self.btcancelar_muda_cor)
		self.botao_cancelar.bind('<Leave>',self.btcancelar_padrao)
		
	def btsalvar_padrao(self,event):
		self.botao_salvar["background"] = '#f0f0f0'
	def btsalvar_muda_cor(self,event):
		self.botao_salvar["background"] = 'green'
	def btcancelar_padrao(self,event):
		self.botao_cancelar["background"] = '#f0f0f0'
	def btcancelar_muda_cor(self,event):
		self.botao_cancelar["background"] = 'green'
	def valida_dados(self,controler):
		global livro
		titulo = self.entrada_titulo.get()
		autor = self.entrada_autor.get()
		qtd_paginas = self.entrada_qtd_paginas.get()
		ano = self.entrada_ano.get()
		qtd = self.entrada_qtd.get()
		if(titulo=='' and autor=='' and qtd_paginas=='' and ano=='' and qtd==''):
			messagebox.showwarning("Aviso", "Preencha os Campos")
		elif(titulo==''):
			messagebox.showwarning("Aviso", "Preencha o Campo titulo")
		elif(autor==''):
			messagebox.showwarning("Aviso", "Preencha o Campo autor")
		elif(ano==''):
			messagebox.showwarning("Aviso", "Preencha o Campo ano")
		else:
			livro.create_book(self, titulo, autor,qtd_paginas, ano,qtd,qtd)
			livro.add()
			messagebox.showinfo("Comfirmação","Livro cadastrado com sucesso.")
			controler.show_frame(MenuLivros)
		
class LivroBuscar(Frame):
	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		
		logo = PhotoImage(file=diretorio_imagens+"icone_buscar_livro.png")		
		self.frame_logo = Frame(self,bg=COR_FUNDO,pady=50)
		self.frame_logo.pack()
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		
		self.frame = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame.pack()
		
		self.titulo = Label(self.frame,border=2,relief=RIDGE,text="Titulo : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.autor = Label(self.frame,border=2,relief=RIDGE,text="Autor : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.ano = Label(self.frame,border=2,relief=RIDGE,text="Ano : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		
		self.entrada_titulo = Entry(self.frame,width=80)
		self.entrada_autor = Entry(self.frame,width=80)
		self.entrada_ano = Entry(self.frame,width=80)
		
		self.titulo.grid(row=0,column=0)
		self.autor.grid(row=1,column=0)
		self.ano.grid(row=2,column=0)
		
		self.entrada_titulo.grid(row=0,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_autor.grid(row=1,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_ano.grid(row=2,column=1,ipady=ALTURA_ENTRY_PADRAO)
		
		self.frame_botoes = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame_botoes.pack()
		self.botao_buscar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Buscar",width = int(LARGURA_PADRAO/3),command = lambda:self.valida_dados(controler),activebackground='green')
		self.botao_buscar.grid(row=0,column=0)
		self.botao_cancelar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Cancelar",width = int(LARGURA_PADRAO/3),command = lambda:self.limpar_campos(controler),activebackground='green')
		self.botao_cancelar.grid(row=0,column=10)	
	def valida_dados(self, controler):
		controler.show_frame(MenuLivros)
	def limpar_campos(self, controler):
		self.entrada_titulo.delete(0, END)
		self.entrada_autor.delete(0, END)
		self.entrada_ano.delete(0, END)
		controler.show_frame(MenuLivros)
class LivroAtualizar(Frame):
	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		
		logo = PhotoImage(file=diretorio_imagens+"icone_livro.png")		
		self.frame_logo = Frame(self,bg=COR_FUNDO,pady=50)
		self.frame_logo.pack()
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		
		self.frame = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame.pack()
		
		self.titulo = Label(self.frame,border=2,relief=RIDGE,text="Titulo : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.autor = Label(self.frame,border=2,relief=RIDGE,text="Autor : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.qtd_paginas = Label(self.frame,border=2,relief=RIDGE,text="Qtd paginas : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.ano = Label(self.frame,border=2,relief=RIDGE,text="Ano : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		
		self.entrada_titulo = Entry(self.frame,width=80)
		self.entrada_autor = Entry(self.frame,width=80)
		self.entrada_qtd_paginas = Entry(self.frame,width=80)
		self.entrada_ano = Entry(self.frame,width=80)
		
		self.titulo.grid(row=0,column=0)
		self.autor.grid(row=1,column=0)
		self.qtd_paginas.grid(row=2,column=0)
		self.ano.grid(row=3,column=0)
		
		self.entrada_titulo.grid(row=0,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_autor.grid(row=1,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_qtd_paginas.grid(row=2,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_ano.grid(row=3,column=1,ipady=ALTURA_ENTRY_PADRAO)
		
		self.frame_botoes = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame_botoes.pack()
		self.botao_salvar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Atualizar",width = int(LARGURA_PADRAO/3),command = lambda:self.valida_dados(controler),activebackground='green')
		self.botao_salvar.grid(row=0,column=0)
		self.botao_cancelar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Cancelar",width = int(LARGURA_PADRAO/3),command = lambda:self.limpar_campos(controler),activebackground='green')
		self.botao_cancelar.grid(row=0,column=10)
	def valida_dados(self, controler):
		controler.show_frame(MenuLivros)
	def limpar_campos(self, controler):
		self.entrada_titulo.delete(0, END)
		self.entrada_autor.delete(0, END)
		self.entrada_ano.delete(0, END)
		controler.show_frame(MenuLivros)
class LivroRemover(Frame):
	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		
		logo = PhotoImage(file=diretorio_imagens+"icone_remover_livro.png")		
		self.frame_logo = Frame(self,bg=COR_FUNDO,pady=50)
		self.frame_logo.pack()
		self.logo = Label(self.frame_logo,bg=COR_FUNDO)
		self.logo["image"] = logo
		self.logo.image = logo
		self.logo.pack()
		
		self.frame = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame.pack()
		
		self.titulo = Label(self.frame,border=2,relief=RIDGE,text="Titulo : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.autor = Label(self.frame,border=2,relief=RIDGE,text="Autor : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		self.ano = Label(self.frame,border=2,relief=RIDGE,text="Ano : ",width=int(LARGURA_PADRAO/3),font=FONTE_PADRAO)
		
		self.entrada_titulo = Entry(self.frame,width=80)
		self.entrada_autor = Entry(self.frame,width=80)
		self.entrada_ano = Entry(self.frame,width=80)
		
		self.titulo.grid(row=0,column=0)
		self.autor.grid(row=1,column=0)
		self.ano.grid(row=2,column=0)
		
		self.entrada_titulo.grid(row=0,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_autor.grid(row=1,column=1,ipady=ALTURA_ENTRY_PADRAO)
		self.entrada_ano.grid(row=2,column=1,ipady=ALTURA_ENTRY_PADRAO)
		
		self.frame_botoes = Frame(self, bg = COR_FUNDO,pady=10)
		self.frame_botoes.pack()
		self.botao_remover = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Remover",width = int(LARGURA_PADRAO/3),command = lambda:self.valida_dados(controler),activebackground='green')
		self.botao_remover.grid(row=0,column=0)
		self.botao_cancelar = Button(self.frame_botoes,border=8,relief=RIDGE,font=FONTE_PADRAO, text = "Cancelar",width = int(LARGURA_PADRAO/3),command = lambda:self.limpar_campos(controler),activebackground='green')
		self.botao_cancelar.grid(row=0,column=10)
		
	def valida_dados(self, controler):
		controler.show_frame(MenuLivros)
	def limpar_campos(self, controler):
		self.entrada_titulo.delete(0, END)
		self.entrada_autor.delete(0, END)
		self.entrada_ano.delete(0, END)
		controler.show_frame(MenuLivros)
class Sobre(Frame):
	def __init__(self,parent,controler):
		Frame.__init__(self,parent)
		self['bg'] = COR_FUNDO
		
		self.frame_titulo = Frame(self, bg = COR_FUNDO,pady=10,padx=10,height=600,width=900)
		self.frame_titulo.pack()
		self.titulo = Label(self.frame_titulo,border=TAMANHO_BORDA_BOTAO,relief=TIPO_BORDA_BOTAO,text= "Sobre o SDlib",font=FONTE_PADRAO,width=40,height=2)
		self.titulo.grid(row=0,column=1)
		self.frame_texto = Frame(self, bg = COR_FUNDO,pady=10,padx=10,height=4,width=10)
		self.frame_texto.pack()
		texto = "\nO SDlib foi desenvolvido para gerenciar um biblioteca ficticia.\n"
		texto += "O sistema disponibliza as seguintes funcionalidades:\n"
		texto += "\t1 - Gerenciamento de Usuarios.\n"
		texto += "\t2 - Gerenciamento de Livros.\n"
		texto += "Projeto concebido na Discplina de Sistemas Distribuidos na instuição de ensino CSHN-UFPI.\n"
		texto += "Curso de sistemas de informação - 4 periodo.\n"
		texto += "Esse projeto foi implemetado em linguaguem Python 3.7.1.\n"
		texto += "Iniciou no começo de Agosto de 2019.\n"
		texto += "Versao inicial: 1.0.15082019-pt-br\n"
		texto += "Versao atual: 1.0.16082019-pt-br\n"
		texto += "Desenvolvedores:\n"
		texto += "\tFrancisco Charles\n"
		texto += "\tJose Mayke\n"
		mensagem = Label(self.frame_texto,border=TAMANHO_BORDA_BOTAO,relief=TIPO_BORDA_BOTAO,text=texto,justify=LEFT,font=FONTE_PADRAO,width=80)
		mensagem.pack(side=LEFT)
		botao = Button(self,border=8,relief=RAISED,text="Voltar", command= lambda: controler.show_frame(Login),font=FONTE_PADRAO)
		botao.pack()
def main():
	app = Gerenciador()
	app.mainloop()
if __name__ == '__main__':
	main()