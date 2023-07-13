import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps


class ImageManipulationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Photoshop App")
        self.geometry("800x600")
        self.resizable(0, 0)
        self.image = None
        self.file_path = None

        self.left_side = ttk.Frame(self, width=200, height=0)
        self.left_side.pack(side="left", fill="y")
        self.left_side.pack_propagate(False)

        self.canvas = tk.Canvas(self, width=600, height=600, background='black')
        self.canvas.pack()

        self.menu_buttons = []
        self.hidden_buttons = []

        self.create_menu_buttons()
        self.create_flip_buttons()
        self.create_color_effect_buttons()
        self.create_resize_panel()

    def create_menu_buttons(self):
        load_btn = ttk.Button(self.left_side, text="Carregar imagem", command=self.load_image)
        flip_btn = ttk.Button(self.left_side, text="Inverter imagem", command=self.toggle_flip_buttons)
        color_btn = ttk.Button(self.left_side, text="Efeitos de cor", command=self.toggle_color_effect_buttons)
        quit_btn = ttk.Button(self.left_side, text="Sair", command=self.destroy)

        self.menu_buttons.extend([load_btn, flip_btn, color_btn, quit_btn])

        for i, button in enumerate(self.menu_buttons):
            button.place(x=5, y=20 + i * 30, width=180)

    def create_flip_buttons(self):
        flip_horizontal_btn = ttk.Button(self.left_side, text="Inverter horizontalmente", command=self.flip_image_horizontal)
        flip_vertical_btn = ttk.Button(self.left_side, text="Inverter verticalmente", command=self.flip_image_vertical)

        self.hidden_buttons.extend([flip_horizontal_btn, flip_vertical_btn])

    def create_color_effect_buttons(self):
        grayscale_btn = ttk.Button(self.left_side, text="Escala de cinza", command=self.grayscale_effect)
        negative_btn = ttk.Button(self.left_side, text="Efeito de cor negativa", command=self.negative_effect)
        original_btn = ttk.Button(self.left_side, text="Retornar imagem original", command=self.return_to_monke)

        self.hidden_buttons.extend([grayscale_btn, negative_btn, original_btn])

    def create_resize_panel(self):
        height_lbl = ttk.Label(self.left_side, text="Altura")
        width_lbl = ttk.Label(self.left_side, text="Largura")

        self.height_box = ttk.Entry(self.left_side)
        self.width_box = ttk.Entry(self.left_side)

        resize_btn = ttk.Button(self.left_side, text="Redimensionar Imagem", command=self.resize_image)

        items = [height_lbl, width_lbl, self.height_box, self.width_box, resize_btn]
        for i, item in enumerate(items):
            x_pos = 20 + i * 100
            if isinstance(item, ttk.Entry):
                item.place(x=12 + (i - 2) * 100 , y=420, width=70)
            elif isinstance(item, ttk.Button):
                item.place(x=10, y=450, width=180)
            else:
            		item.place(x=x_pos, y=400, width=70)

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Abrir arquivo de imagem")
        if file_path:
            self.file_path = file_path
            image = Image.open(file_path)
            image = image.resize((600, 600), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)

    def flip_image_horizontal(self):
        if self.image:
            image = self.image_to_pillow()
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            self.image = self.pillow_to_image(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.show_error("Erro ao tentar inverter a imagem", "Insira uma imagem para inverter!")

    def flip_image_vertical(self):
        if self.image:
            image = self.image_to_pillow()
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            self.image = self.pillow_to_image(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.show_error("Erro ao tentar inverter a imagem", "Insira uma imagem para inverter!")

    def grayscale_effect(self):
        if self.image:
            image = self.image_to_pillow()
            image = image.convert("L")
            self.image = self.pillow_to_image(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.show_error("Falha na troca de cor", "Insira uma imagem para aplicar o efeito de cor!")

    def negative_effect(self):
        if self.image:
            image = self.image_to_pillow()
            image = image.convert('RGB')
            image = ImageOps.invert(image)
            self.image = self.pillow_to_image(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.show_error("Falha na troca de cor", "Insira uma imagem para aplicar o efeito de cor negativa!")

    def return_to_monke(self):
        if self.file_path:
            image = Image.open(self.file_path)
            self.image = self.pillow_to_image(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.show_error("Não foi possível retornar a imagem", "Não foi encontrada a imagem original.")

    def resize_image(self):
        if self.image:
            new_width = int(self.width_box.get())
            new_height = int(self.height_box.get())

            if new_width and new_height:
                if new_width <= 600 or new_height <= 600:
                    image = self.image_to_pillow()
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    self.image = self.pillow_to_image(image)
                    self.canvas.create_image(0, 0, anchor="nw", image=self.image)
                else:
                    self.show_error("Dimensões de redimensionamento inválidas", "As dimensões devem ser menores que 600x600")
            else:
                self.show_error("Tamanhos não encontrados", "Informe altura e largura para continuar!")
        else:
            self.show_error("Erro de redimensionamento", "Insira a imagem para prosseguir")

    def toggle_flip_buttons(self):
        self.toggle_buttons([self.hidden_buttons[0], self.hidden_buttons[1]])

    def toggle_color_effect_buttons(self):
        self.toggle_buttons([self.hidden_buttons[2], self.hidden_buttons[3], self.hidden_buttons[4]])

    def toggle_buttons(self, buttons):
        for button in self.hidden_buttons:
            button.place_forget()

        for button in buttons:
            button_index = self.hidden_buttons.index(button)
            if button_index < 2:
            	button.place(x=5, y=20 + (button_index + len(self.menu_buttons) + 1) * 30, width=180)
            else:
            	button.place(x=5, y=20 + ((button_index - 2) + len(self.menu_buttons) + 1) * 30, width=180)

    def image_to_pillow(self):
        return ImageTk.getimage(self.image)

    def pillow_to_image(self, image):
        return ImageTk.PhotoImage(image)

    def show_error(self, title, message):
        messagebox.showerror(title=title, message=message)


if __name__ == "__main__":
    app = ImageManipulationApp()
    app.mainloop()

