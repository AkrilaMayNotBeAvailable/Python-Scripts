from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageOps
from math import ceil

#==============================================================
# @AkrilaMayNotBeAvailable 
#--------------------------------------------------------------
# Este código foi feito como exercício para uma turma na qual
# prestei monitoria no ano de 2023 na UFRGS.
# Os casos de erro ---não foram tratados---
# Tab width convension = 2
#==============================================================

# ConvertUpdate : Int PIL.Image -> Tkinter.Image
# Dado um índice e uma imagem do módulo Pillow atualiza a versão da imagem 
# no índice informado para uma Imagem do módulo Tkinter.
def ConvertUpdate(index, pillow_image):
	update = ImageTk.PhotoImage(pillow_image)
	image_list[index] = update
	DrawImages()

# DrawImages : none -> none
# Inicialmente, limpa o canvas e após desenha todas as imagens em image_list
def DrawImages():
  canvas.delete("all")  # Clear the canvas
  for i, photo in enumerate(image_list):
    x, y = image_coords[i]
    canvas.create_image(x, y, anchor="nw", image=photo)  					# Display the Tkinter Image on the canvas
        
# LoadImage : none -> none
# Busca um caminho dado pelo usuário em uma interface de busca do Tkinter
# uma imagem de qualquer formato e atribuí os tamanhos da imagem, o caminho e a
# própria imagem para listas diferentes. Também atualiza uma lista interna do programa.
# *This goes inside a button command parameter
def LoadImage():
	file_path = filedialog.askopenfilename(title="Open Image File")
	if file_path:
		image = Image.open(file_path) 																# Open Image
		# Image Lists update:
		image_sizes.append((image.width, image.height)) 							# Update Image Size list
		image_path.append(file_path) 																	# Update File Path list
		image_list.append(ImageTk.PhotoImage(image)) 									# Adds to List as Tkinter Image: 
		image_coords.append((int(move_x.get()), int(move_y.get())))  	# Updates image coordinates list
		DrawImages()
		
	# Atualiza a Combo Box baseada nos novos valores
	image_index = len(image_list) - 1
	index_box['values'] = list(range(image_index + 1))
	index_box.current(image_index)
		
# SaveCanvasImage : none -> none
# Utiliza-se a função PostScript para salvar os dados do canvas em uma imagem no formato
# .eps e após a criação do arquivo, é realizada a abetura deste arquivo .eps utilizando Pillow 
# e agora é realizada a conversão para .png, com alguma perca de qualidade.
# Outros métodos: BytesIO, Image.grab(), módulo MSS
# **Note que apesar da qualidade, é mais que suficiente para um programa surperficial.
# *This goes inside a button command parameter
def SaveCanvasImage():
  file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
  if file_path:
    canvas.update()
    # Postscript, por padrão tem um valor fixo de pagewidth/height, deve ser modificado para fins de qualidade da imagem.
    canvas.postscript(file=file_path + '.eps', colormode='color', pagewidth=canvas.winfo_reqwidth(), pageheight=canvas.winfo_reqheight())
    img = Image.open(file_path + '.eps')
    img.save(file_path, format="png", quality=100)

# MoveImagePosition: none -> none
# Modifica a posição de uma imagem carregada no programa em um elemento Canvas,
# dadas as coordenadas em campos de entrada do usuário.
# *This goes inside a button command parameter        
def MoveImagePosition():
	index = int(index_box.get())
	image_coords[index] = (int(move_x.get()), int(move_y.get()))
	DrawImages()

# ResizeImage : none -> none
# Modifica o tamanho de uma imagem já carregada no programa e atualiza
# os valores de altura e largura em uma lista, depois atualiza o canvas
# com a nova imagem.
# *Laboratório de Grad. INF UFRGS não estava reconhecendo Image.Resampling.LANCZOS
# * Possível FIX -> resample=Resampling.LANCZOS
# *This goes inside a button command parameter
def ResizeImage():
	# Verifica índice atual e recebe os dados nos campos de entrada do usuário
	index = int(index_box.get())
	image_sizes[index] = (int(mod_width.get()), int(mod_height.get()))
	# Verificação de índice na lista
	if 0 <= index < len(image_list):
		image = image_list[index]
		resized_image = ImageTk.getimage(image)
		width, height = image_sizes[index]
		resized_image = resized_image.resize((width, height), Image.Resampling.LANCZOS) # **
		resized_image = ImageTk.PhotoImage(resized_image)
		image_list[index] = resized_image
		DrawImages()

# AuxSwapIndex : Int Int -> Update Array
# Dados dois índices dentro do tamanho de image_list,
# Troca a posição dos índices na lista, de forma que o primeiro parâmetro troca com o segundo parâmetro
# *This can't go inside a button.
def AuxSwapIndex(index1, index2):
  if 0 <= index1 < len(image_list) and 0 <= index2 < len(image_list):
    # Swap the images in the image_list
    image_list[index1], image_list[index2] = image_list[index2], image_list[index1]
    DrawImages()
    
# SwapIndex : none -> none
# Modifica a posição de duas imagens dentro de uma lista baseado no valor dos campos de entrada:
# first_swap e second_swap.
# Atualiza a imagem no Canvas.
# *This goes inside a button command parameter
def SwapIndex():
  index1 = int(first_swap.get())
  index2 = int(second_swap.get())
  AuxSwapIndex(index1, index2)
  DrawImages()
  
# FlipHorizontal : none -> none
# Dado um índice, inverte horizontalmente uma imagem na lista image_list
# Atualiza a imagem no Canvas.
# *This goes inside a button command parameter
def FlipHorizontal():
	index = int(index_box.get())
	if 0 <= index < len(image_list):
		image = image_list[index]
		flipped_image = ImageTk.getimage(image)
		flipped_image = flipped_image.transpose(Image.FLIP_LEFT_RIGHT) # Vertical é FLIP_TOP_BOTTOM
		ConvertUpdate(index, flipped_image)

# Grayscale : none -> none
# Dada uma imagem da lista image_list, converte suas cores para
# tons de cinza.
# Atualiza a imagem no Canvas.
def Grayscale():
	index = int(index_box.get())
	if 0 <= index < len(image_list):
		image = image_list[index]
		gray_version = ImageTk.getimage(image)
		gray_version = gray_version.convert("L")
		ConvertUpdate(index, gray_version)

# Negative : none -> none
# Dada uma imagem da lista image_list, remove o canal Alpha independente
# do formato e realiza a operação de inversão de cores no pixels da imagem.
# Atualiza a imagem no Canvas.	
def Negative():
	index = int(index_box.get())
	if 0 <= index < len(image_list):
		image = image_list[index]
		negative_version = ImageTk.getimage(image)
		negative_version = negative_version.convert('RGB')
		negative_version = ImageOps.invert(negative_version)
		ConvertUpdate(index, negative_version)

# OriginalImage : none -> none
# Baseado na lista image_path, busca novamente a imagem no armazenamento interno
# e retorna ela para o Canvas com o mesmo tamanho que foi salvo pela última vez no
# programa.
# Atualiza a imagem no Canvas.
def OriginalImage():
	index = int(index_box.get())
	if 0 <= index < len(image_list):
		image = image_list[index]
		# Recarrega a imagem original -- Possível erro caso a imagem não exista mais
		originalImage = Image.open(image_path[index])
		# Retorna última altura e largura salva no programa e faz o resize da imagem
		width, height = image_sizes[index]
		originalImage = originalImage.resize((width, height), Image.Resampling.LANCZOS)
		# Atualiza a imagem
		ConvertUpdate(index, originalImage)

# CreateButton : tkinter.frame, int, int, int, int, string, func() -> tkinter.Button
# Dadas uma frame, 4 inteiros representando a linha, coluna em uma grade,
# a quantidade de colunas que o botão irá ocupar na grade, o tamanho do botão,
# um texto para botão e uma função de comando, cria um objeto do tipo botão
# do módulo Tkinter.
def CreateButton(parent, linha, coluna, spamColuna, largura, texto, funcao):
  button = ttk.Button(parent, text=texto, width=largura, command=funcao)
  button.grid(row=linha, column=coluna, columnspan=spamColuna, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)
  
# CreateEntryLabeled : tkinter.frame int, int, string, int
# Dadas uma frame, 2 inteiros representando linha e coluna em uma grade,
# uma texto de descrição para uma etiqueta e a lagura do campo de entrada
# Retorna um campo de entrada de dados de usuário iniciado em zero.
def CreateEntryLabeled(parent, linha, coluna, texto, largura):
  label = ttk.Label(parent, text=texto)
  label.grid(row=linha, column=coluna, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)
  
  entry = ttk.Entry(parent, width=largura)
  entry.insert(0, "0")
  entry.grid(row=linha+1, column=coluna, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)
  
  return entry

# Create the main application window
#===================================================
root = Tk()
root.title("Aplicativo de Edição de Fotos")
root.attributes('-zoomed', True) # Linux Ubuntu
#root.state('zoomed') # Windows
root.update()


# Constants:
#==============================
SCREEN_WIDTH = root.winfo_width()
SCREEN_HEIGHT = root.winfo_height()
PADDING_X_GRID = 20
PADDING_Y_GRID = 2

# Image related structures:
#==============================
image_list = []
image_coords = []
image_sizes = []
image_path = []

# Menu side frame:
#===================================================
left_side = ttk.Frame(root, width=ceil(0.16*SCREEN_WIDTH), height=0)
left_side.pack(side="left", fill="y")
left_side.pack_propagate(False)

left_side.update()

# Constant
SIDE_MENU_WIDTH = left_side.winfo_width()

# Frame inside frame
bottom_side = ttk.Frame(left_side, width=SIDE_MENU_WIDTH, height=(0.40*SCREEN_HEIGHT))
bottom_side.pack(side="bottom", fill="x")
bottom_side.pack_propagate(False)

# Canvas side:
#===================================================
WIDTH = root.winfo_width() - left_side.winfo_width()
HEIGHT = root.winfo_height()
#===================================================
canvas = Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0, borderwidth=0, background='black') 
canvas.pack()

# Buttons:
#===================================================
# index_box -> Guarda os índices das imagens carregadas no programa.
# load_button -> Inicia a interface de busca por arquivos de imagem, por padrão inicia no diretório deste arquivo.
# flip_button -> Dado um índice de imagem carregada no programa e presente na lista image_list
# inverte a imagem naquele indíce no eixo X
# save_button -> Dado um elemento Canvas, cria um arquivo de imagem .eps (que demora um pouco) e um png a partir deste.
#===================================================
# Main Menu Front-End elements:
#===================================================
index_box = ttk.Combobox(left_side, state="readonly")
index_box.grid(row=0, column=0, columnspan=2, padx=PADDING_X_GRID, pady=0)
load_button = CreateButton(left_side, 1, 0, 2, 20, "Carregar Imagem", LoadImage)
flip_button = CreateButton(left_side, 2, 0, 2, 20, "Inverter Horizontal", FlipHorizontal)
grayscale_button = CreateButton(left_side, 3, 0, 2, 20, "Efeito de cor cinza", Grayscale)
negative_button = CreateButton(left_side, 4, 0, 2, 20, "Inverter Cores", Negative)
original_button = CreateButton(left_side, 5, 0, 2, 20, "Imagem Original", OriginalImage)
save_button = CreateButton(left_side, 6, 0, 2, 20, "Salvar Imagem", SaveCanvasImage)
#==============================================
# Move Image Front-end elements:
#==============================================
move_x = CreateEntryLabeled(bottom_side, 0, 0, "Pos: X", 5)
move_y = CreateEntryLabeled(bottom_side, 0, 1, "Pos: Y", 5)
move_button = CreateButton(bottom_side, 2, 0, 2, 20, "Mover Imagem", MoveImagePosition)
#==============================================
# Resize Image Front-end elements:
#==============================================
mod_width = CreateEntryLabeled(bottom_side, 3, 0, "Largura", 5)
mod_height = CreateEntryLabeled(bottom_side, 3, 1, "Altura", 5)
modify_size_button = CreateButton(bottom_side, 5, 0, 2, 20, "Mudar Tamanho", ResizeImage)
#==============================================
# Swap Indexes Front-end elements:
#==============================================
first_swap = CreateEntryLabeled(bottom_side, 6, 0, "Índice 1", 5)
second_swap = CreateEntryLabeled(bottom_side, 6, 1, "Índice 2", 5)
change_index_button = CreateButton(bottom_side, 8, 0, 2, 20, "Trocar Layer", SwapIndex)

# Start the Tkinter main loop
root.mainloop()

