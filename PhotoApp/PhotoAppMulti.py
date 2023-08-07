from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageOps
from math import ceil

# Draw Multiple Images at canvas
def draw_images():
  canvas.delete("all")  # Clear the canvas
  for i, photo in enumerate(image_list):
    x, y = image_coords[i]
    canvas.create_image(x, y, anchor="nw", image=photo)  # Display the PhotoImage on the canvas
        
# Function to handle image loading and adding it to the list
def load_image():
	file_path = filedialog.askopenfilename(title="Open Image File")
	if file_path:
		image = Image.open(file_path)
		image_sizes.append((image.width, image.height))
		# Adds to List as Tkinter Image:
		image_list.append(ImageTk.PhotoImage(image))
		print("Image added to the list.")
		print(image_list)
		image_coords.append((int(move_x.get()), int(move_y.get())))  # Initial position (0, 0)
		draw_images()
		
	# Atualiza a Combo Box baseada nos novos valores
	image_index = len(image_list) - 1
	index_box['values'] = list(range(image_index + 1))
	index_box.current(image_index)
	

# Function to perform a vertical flip on the image at the specified index
def flip_vertical_image():
	index = int(index_box.get())
	if 0 <= index < len(image_list):
		image = image_list[index]
		flipped_image = ImageTk.getimage(image)
		flipped_image = flipped_image.transpose(Image.FLIP_LEFT_RIGHT)
		flipped_image = ImageTk.PhotoImage(flipped_image)
		image_list[index] = flipped_image
		draw_images()
		
# Function to save the whole canvas as an image
def save_canvas_as_image():
  file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
  if file_path:
      canvas.update()
      canvas.postscript(file=file_path + '.eps', colormode='color', pagewidth=1024, pageheight=1024)
      img = Image.open(file_path + '.eps')
      img.save(file_path, format="png", quality=100)
        
def move_image():
	index = int(index_box.get())
	image_coords[index] = (int(move_x.get()), int(move_y.get()))
	draw_images()
	
def resize_image():
	index = int(index_box.get())
	image_sizes[index] = (int(mod_width.get()), int(mod_height.get()))
	if 0 <= index < len(image_list):
		image = image_list[index]
		resized_image = ImageTk.getimage(image)
		width, height = image_sizes[index]
		resized_image = resized_image.resize((width, height), Image.Resampling.LANCZOS)
		resized_image = ImageTk.PhotoImage(resized_image)
		image_list[index] = resized_image
		draw_images()
		
def swap_images(index1, index2):
    if 0 <= index1 < len(image_list) and 0 <= index2 < len(image_list):
        # Swap the images in the image_list
        image_list[index1], image_list[index2] = image_list[index2], image_list[index1]
        draw_images()
	
def swap_selected_images():
    index1 = int(first_swap.get())
    index2 = int(second_swap.get())
    swap_images(index1, index2)
    draw_images()

# Create the main application window
#===================================================
root = Tk()
root.title("Photoshop App")
root.attributes('-zoomed', True) # Linux Ubuntu
#root.state('zoomed') # Windows

root.update()
SCREEN_WIDTH = root.winfo_width()
SCREEN_HEIGHT = root.winfo_height()


HEIGHT = 600
VERTICALSPACING = 30
PADDING_X_GRID = 20
PADDING_Y_GRID = 5
BTNSIZE = 180
MARGIN = 5
image_list = []
image_coords = []
image_sizes = []

# Menu side:
#===================================================
left_side = ttk.Frame(root, width=ceil(0.16*SCREEN_WIDTH), height=0)
left_side.pack(side="left", fill="y")
left_side.pack_propagate(False)



left_side.update()
SIDE_MENU_WIDTH = left_side.winfo_width()

bottom_side = ttk.Frame(left_side, width=SIDE_MENU_WIDTH, height=(0.40*SCREEN_HEIGHT))
bottom_side.pack(side="bottom", fill="x")
bottom_side.pack_propagate(False)


WIDTH = root.winfo_width() - left_side.winfo_width()

# Canvas side:
#===================================================
canvas = Canvas(root, width=WIDTH, height=HEIGHT, background='black') 
canvas.pack()


# Buttons:
#===================================================
# index_box -> Guarda os índices das imagens carregadas no programa.
# load_button -> Inicia a interface de busca por arquivos de imagem, por padrão inicia no diretório deste arquivo.
# flip_button -> Dado um índice de imagem carregada no programa e presente na lista image_list
# inverte a imagem naquele indíce no eixo X
# save_button -> Dado um elemento Canvas, cria um arquivo de imagem .eps (que demora um pouco) e um png a partir deste.
index_box = ttk.Combobox(left_side, state="readonly")
load_button = ttk.Button(left_side, text="Load Image", command=load_image)
flip_button = ttk.Button(left_side, text="Flip Horizontal", command=flip_vertical_image)
save_button = ttk.Button(left_side, text="Save Canvas as Image", command=save_canvas_as_image)

menu_button_list = [index_box, load_button, flip_button, save_button]

for i, button in enumerate(menu_button_list):
	button.place(x=(BTNSIZE-(SIDE_MENU_WIDTH/2))/2 - 20, y=20 + i * VERTICALSPACING, width=BTNSIZE)
#==========================================================================================
# Move Image Position Front-end elements:
#==============================================
label_x = ttk.Label(bottom_side, text="X Pos")
label_y = ttk.Label(bottom_side, text="Y Pos")
move_x = ttk.Entry(bottom_side, width=5)
move_y = ttk.Entry(bottom_side, width=5)
move_x.insert(0, "0")
move_y.insert(0, "0")
move_button = ttk.Button(bottom_side, text="Move Image to", width=20, command=move_image)

label_x.grid(row=0, column=0, padx=PADDING_X_GRID)
label_y.grid(row=0, column=1, padx=PADDING_X_GRID)
move_x.grid(row=1, column=0, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)
move_y.grid(row=1, column=1, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)
move_button.grid(row=2, column=0, columnspan=2, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)
#==========================================================================================
# Resize Image Front-end elements:
#==============================================
label_width = ttk.Label(bottom_side, text="Width")
label_height = ttk.Label(bottom_side, text="Height")
mod_width = ttk.Entry(bottom_side, width=5)
mod_height = ttk.Entry(bottom_side, width=5)
modify_size_button = ttk.Button(bottom_side, text="Change Image Size", width=20, command=resize_image)

label_width.grid(row=3, column=0, padx=PADDING_X_GRID)
label_height.grid(row=3, column=1, padx=PADDING_X_GRID)
mod_width.grid(row=4, column=0, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)
mod_height.grid(row=4, column=1, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)
modify_size_button.grid(row=5, column=0, columnspan=2, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)

#==========================================================================================
# Swap Indexes Front-end elements:
#==============================================
label_swap_first = ttk.Label(bottom_side, text="Desired Index")
label_swap_second = ttk.Label(bottom_side, text="Swap to")
first_swap = ttk.Entry(bottom_side, width=5)
second_swap = ttk.Entry(bottom_side, width=5)
change_index_button = ttk.Button(bottom_side, text="Swap Indexes", width=20, command=swap_selected_images)

label_swap_first.grid(row=6, column=0, padx=PADDING_X_GRID)
label_swap_second.grid(row=6, column=1, padx=PADDING_X_GRID)
first_swap.grid(row=7, column=0, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)
second_swap.grid(row=7, column=1, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)
change_index_button.grid(row=8, column=0, columnspan=2, padx=PADDING_X_GRID, pady=PADDING_Y_GRID)

# Start the Tkinter main loop
root.mainloop()

