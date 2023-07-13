from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror

from PIL import ImageTk, Image, ImageOps

from pdb import set_trace as pause
# pip install pillow --upgrade

WIDTH = 600
HEIGHT = 600
VERTICALSPACING = 30
BTNSIZE = 180
MARGIN = 5
hidden_buttons = []  # Lista para armazenar os botões ocultos

# Functions:
#========================================
def TkinterToImage(imageTk):
    return ImageTk.getimage(imageTk) # Converte uma instância de ImageTk em uma instância de Image
def ImageToTkinter(image):
	return ImageTk.PhotoImage(image) # Converte uma instância de Image em uma instância de ImageTk

def LoadImage():
	try:
		global filePath # Não tem como fazer sem ser global, ou ela vai ser objeto ou uma var global
		filePath = filedialog.askopenfilename(title="Open Image File")
		if filePath:
			global image # Essa referência deve ser global? Caso não seja ela não é carregada
			image = Image.open(filePath) # Abre a imagem com a estrutura do módulo Pillow
			image = image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS) # Modifica o tamanho da imagem para o tamanho do canvas
			image = ImageTk.PhotoImage(image) # Transforma a imagem em uma estrutura válida para Tkinter
			canvas.create_image(0, 0, anchor="nw", image=image)	# Atualiza o Canvas com a imagem
	except:
		print("Error while trying to load image with LoadImage()")
    

# Flip Image in horizontal axis
#================================================= 
def FlipImageHorizontal():
	try:
		global image
		image = TkinterToImage(image) # Converter Tk para Pillow
		image = image.transpose(Image.FLIP_LEFT_RIGHT)
		image = ImageToTkinter(image) # Converte Pillow para Tk
		canvas.create_image(0, 0, anchor="nw", image=image)	# Atualiza o Canvas com a imagem
		
	except:
		showerror(title='Flip Image Error', message='Please select an image to flip!')
		
# Flip Image in vertical axis
#================================================= 	
def FlipImageVertical():
	try:
		global image
		image = TkinterToImage(image) # Converter Tk para Pillow
		image = image.transpose(Image.FLIP_TOP_BOTTOM)
		image = ImageToTkinter(image) # Converte Pillow para Tk
		canvas.create_image(0, 0, anchor="nw", image=image) # Atualiza imagem no canvas	
	except:
		showerror(title='Flip Image Error', message='Please select an image to flip!')

# Applies Grayscale effect on a image
#================================================= 	
def GrayscaleEffect():
	try:
		global image
		image = TkinterToImage(image) # Converter Tk para Pillow
		image = image.convert("L")
		image = ImageToTkinter(image) # Converte Pillow para Tk
		canvas.create_image(0, 0, anchor="nw", image=image) # Atualiza imagem no canvas	
	except:
		showerror(title='Color conversion fail', message='The color conversion failed.')

# Applies Negative effect on a image
#===================================================
def NegativeEffect():
	try:
		global image
		image = TkinterToImage(image) # Converter Tk para Pillow
		image = image.convert('RGB')
		image = ImageOps.invert(image)
		image = ImageToTkinter(image) # Converte Pillow para Tk
		canvas.create_image(0, 0, anchor="nw", image=image) # Atualiza imagem no canvas	
	except:
		showerror(title='Color conversion fail', message='The color conversion failed.')

# Returns to original image
#===================================================
def ReturnToMonke():
	try:
		global image, filePath
		image = Image.open(filePath)
		
		
			
		image = ImageToTkinter(image) # Converte Pillow para Tk
		canvas.create_image(0, 0, anchor="nw", image=image) # Atualiza imagem no canvas
	except:
		showerror(title="Couldn't return to original image", message='Failed to return to original image')
		
# Resize Image based on User input
#===================================================
def ResizeImage():
	try:
		global image
		newWidth = int(heightBox.get())
		newHeight = int(widthBox.get())
		
		if newWidth and newHeight:
			if newWidth <= WIDTH or newHeight <= HEIGHT:
				image = TkinterToImage(image) # Converter Tk para Pillow
				image = image.resize((newWidth, newHeight), Image.Resampling.LANCZOS)
				image = ImageToTkinter(image) # Converte Pillow para Tk
				canvas.create_image(0, 0, anchor="nw", image=image) # Atualiza imagem no canvas
			else:
				print("User has informed values higher than Canvas size.")
		else:
			print("User haven't informed height and width")
	except:
		showerror(title="Cloudn't resize image", message="Inform new width and height!")
# ToggleButton: (Front-end Function)
#=================================================
def ToggleButton():
	try:
		global hidden_buttons # Acessa a lista de botões escondidos
		focusedBtn = root.focus_get()

		# Remover todos os botões adicionais da tela
		for button in hidden_buttons:
			button.place_forget()

		hidden_buttons.clear()  # Limpar a lista de botões ocultos

		if focusedBtn == flipBtn:
			hidden_buttons = [flipHorizontal, flipVertical]
		elif focusedBtn == colorBtn:
			hidden_buttons = [grayscaleBtn, negativeBtn, originalBtn]

		# Adicionar apenas os botões relevantes à tela
		for button in hidden_buttons:
			button.place(x=MARGIN, y=20 + (hidden_buttons.index(button) + len(menuBtnList) + 1) * 30, width=BTNSIZE)

	except:
		showerror(title="Error at Show/Hide function", message="Erro ao ativar botões ocultos")

#========================================
# Window Configuration:
#========================================
root = Tk()
root.title("Photoshop App")
mainframe = ttk.Frame(root, padding="3 3 12 12")
root.resizable(0, 0)
root.geometry("800x600")

# Menu side:
#===================================================
leftSide = ttk.Frame(root, width=200, height=0)
leftSide.pack(side="left", fill="y")
leftSide.pack_propagate(False)

# Canvas Side:
#===================================================
canvas = Canvas(root, width=WIDTH, height=HEIGHT, background='black') 
canvas.pack()

# Front End Design Part:
#=================================================================================================
# Main Menu Button instances:
#===================================================
loadBtn = ttk.Button(leftSide, text="Load Image", command=LoadImage)
flipBtn = ttk.Button(leftSide, text="Flip Image", command=ToggleButton)
colorBtn = ttk.Button(leftSide, text="Color Effects", command=ToggleButton)
quitBtn = ttk.Button(leftSide, text="Quit", command=root.destroy)
# Main Button List
menuBtnList = [loadBtn, flipBtn, colorBtn, quitBtn]

# Flip options:
flipHorizontal = ttk.Button(leftSide, text="Flip Horizontally", command=FlipImageHorizontal)
flipVertical = ttk.Button(leftSide, text="Flip Vertically", command=FlipImageVertical)
# Color Effects Buttons
grayscaleBtn = ttk.Button(leftSide, text="Grayscale color Effect", command=GrayscaleEffect)
negativeBtn = ttk.Button(leftSide, text="Negative color Effect", command=NegativeEffect)
originalBtn = ttk.Button(leftSide, text="Return to Original Image", command=ReturnToMonke)

# Resize Panel:
#==============================================
heightLbl = ttk.Label(leftSide, text="Height")
widthLbl = ttk.Label(leftSide, text="Width")

heightBox = ttk.Entry(leftSide)
widthBox = ttk.Entry(leftSide)

resizeBtn = ttk.Button(leftSide, text="Resize image", command=ResizeImage)

boxesList = [heightLbl, widthLbl, heightBox, widthBox, resizeBtn]

# Resize Panel Positions:
#=================================================================
for i, boxes in enumerate(boxesList):
	if type(boxes) == type(heightLbl):	
		boxes.place(x=20 + i * 100, y=400, width=70)
	elif type(boxes) == type(resizeBtn):
		boxes.place(x=MARGIN, y=450, width=BTNSIZE)
	elif type(boxes) == type(heightBox):
		boxes.place(x=MARGIN + (i - 2) * 100 + 2, y= 420,  width=70)
		
# Positioning:
#=================================================================
for i, button in enumerate(menuBtnList):
    button.place(x=MARGIN, y=20 + i * VERTICALSPACING, width=BTNSIZE)

# Keep Window Running:
root.mainloop()
