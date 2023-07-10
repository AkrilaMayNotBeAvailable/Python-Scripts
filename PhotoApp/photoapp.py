from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import PIL
from PIL import ImageTk, Image
# pip install pillow --upgrade

WIDTH = 600
HEIGHT = 600
filePath = ""
is_flipped = False
flip_options = False

# Functions:
#========================================
def open_image():
    global imgPath
    imgPath = filedialog.askopenfilename(title="Open Image File")
    if imgPath:
        global image # Instância (Image)
        image = Image.open(imgPath) # Abre a imagem
        image = image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS) # Modifica o tamanho da imagem para o tamanho do canvas
            
        image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=image)

'''
Tratamento da imagem:
	Abrir com Pillow (Image.open(file_path))
	Modificar o que deseja
	Criar instância modificada e atualizar ImageTk.PhotoImage()
	
# If not flipped Vertical:
# If not flipped Horinzontal:

'''

# Test purrposes
#=================================================
def flip_image_V():
    try:
        global image, photo_image, is_flipped
        if not is_flipped:
            # open the image and flip it left and right
            image = Image.open(imgPath).transpose(Image.FLIP_TOP_BOTTOM)
            is_flipped = True
        else:
            # reset the image to its original state
            image = Image.open(imgPath)
            is_flipped = False
        # resize the image to fit the canvas
        image = image.resize((WIDTH, HEIGHT), Image.LANCZOS)
        # convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        photo_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=photo_image)

    except:
        showerror(title='Flip Image Error', message='Please select an image to flip!')

# Test purrposes
#================================================= 
def flip_image_H():
    try:
        global image, photo_image, is_flipped
        if not is_flipped:
            # open the image and flip it left and right
            image = Image.open(imgPath).transpose(Image.FLIP_LEFT_RIGHT)
            is_flipped = True
        else:
            # reset the image to its original state
            image = Image.open(imgPath)
            is_flipped = False
        # resize the image to fit the canvas
        image = image.resize((WIDTH, HEIGHT), Image.LANCZOS)
        # convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        photo_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=photo_image)

    except:
        showerror(title='Flip Image Error', message='Please select an image to flip!')
        

        
        
def FlipOptions():
	try:
		global flip_options
		if not flip_options:
			flip_options = True
			flipH_btn.place(x=5, y=170, width=180)
			flipV_btn.place(x=5, y=200, width=180)
			
		else:
			flip_options = False
			flipH_btn.place_forget()
			flipV_btn.place_forget()
	except:
		showerror(title="Error at Show/Hide function", message="This isn't working...") 
      
#========================================
# Window Configuration:
#========================================
root = Tk()
root.title("Photoshop App")
mainframe = ttk.Frame(root, padding="3 3 12 12")
root.resizable(0, 0)
root.geometry("800x600")

''' Front-end stuff
#s = ttk.Style()
#s.configure('Danger.TFrame', background='red', borderwidth=5, relief='raised')

#methods for align
# .pack(side="left or right or top or bottom")
# .place(x=Number, y=Number)
# .grid(row=Number, column=Number)
'''

# Menu side:
#===================================================
leftSide = ttk.Frame(root, width=200, height=0)
leftSide.pack(side="left", fill="y")
leftSide.pack_propagate(False)

# Creates each button instance
#===================================================
loadBtn = ttk.Button(leftSide, text="Load Image", command=open_image)

#		Flipping Functions:
cutBtn = ttk.Button(leftSide, text="Flip Image", command=FlipOptions)
flipH_btn = ttk.Button(leftSide, text="Flip Horizontally", command=flip_image_H)
flipV_btn = ttk.Button(leftSide, text="Flip Vertically", command=flip_image_V)


colorBtn = ttk.Button(leftSide, text="Color Effects")
quitBtn = ttk.Button(leftSide, text="Quit")



#===================================================
# Front-end stuff
# 	Positions:
loadBtn.place(x=5, y=20, width=180)
cutBtn.place(x=5, y=50, width=180)
colorBtn.place(x=5, y=80, width=180)
quitBtn.place(x=5, y=110, width=180)




#Canvas Side:
canvas = Canvas(root, width=WIDTH, height=HEIGHT, background='black')
canvas.pack()


# Keep Window Running:
root.mainloop()
