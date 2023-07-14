import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps

# Visualization Notes: Tab width = 2

# Editor de imagens: Class -> Tkinter object
# Classe que contém todos os dados do programa
# __init__(self) equivale ao root.tk()
class ImageManipulationApp(tk.Tk):
    def __init__(self):
        super().__init__() # Essa classe pode utilizar todos os métodos declarados pela classe pai
        self.title("Photoshop App") # Título
        self.geometry("800x600")    # Tamanho da Janela
        self.resizable(0, 0)        # Não permite resize da janela
        #====================
        self.image = None           # Instância de uma imagem Pillow OU ImageTk
        self.file_path = None       # Caminho para a imagem
      	#====================
	
	      # Frame para alocar botões no canto esquerdo da tela:
	      #=======================================================
        self.left_side = ttk.Frame(self, width=200, height=0)
        self.left_side.pack(side="left", fill="y")
        self.left_side.pack_propagate(False)

	      # Canvas para alocar a imagem na tela
	      #=======================================================
        self.canvas = tk.Canvas(self, width=600, height=600, background='black')
        self.canvas.pack()

	      # Listas de botões:
	      #=======================================================
        self.menu_buttons = []
        self.hidden_buttons = []

	      # Métodos para instânciar os botões no programa:
	      #=======================================================
        self.create_menu_buttons()
        self.create_flip_buttons()
        self.create_color_effect_buttons()
        self.create_resize_panel()
        
#======================================================
# Definição de Funções para criação de elementos na GUI
#======================================================
    def create_menu_buttons(self):
        # Cria uma série de botões que são principais na tela:
        #======================================================
        load_btn = ttk.Button(self.left_side, text="Carregar imagem", command=self.load_image)
        flip_btn = ttk.Button(self.left_side, text="Inverter imagem", command=self.toggle_flip_buttons)
        color_btn = ttk.Button(self.left_side, text="Efeitos de cor", command=self.toggle_color_effect_buttons)
        quit_btn = ttk.Button(self.left_side, text="Sair", command=self.destroy)

        # Adiciona os botões um a um na lista declarada em root:
        self.menu_buttons.extend([load_btn, flip_btn, color_btn, quit_btn])

        # Posiciona os botões um a um na interface gráfica:
        for i, button in enumerate(self.menu_buttons):
            button.place(x=5, y=20 + i * 30, width=180)

    def create_flip_buttons(self):
        # Cria os botões de inversão de imagem, estes ficam invisíveis até que solicitados pelo botão principal
        flip_horizontal_btn = ttk.Button(self.left_side, text="Inverter horizontalmente", command=self.flip_image_horizontal)
        flip_vertical_btn = ttk.Button(self.left_side, text="Inverter verticalmente", command=self.flip_image_vertical)

        # Adiciona os botões escondidos na lista apropriada:
        self.hidden_buttons.extend([flip_horizontal_btn, flip_vertical_btn])

    def create_color_effect_buttons(self):
        # Cria os botões que aplicam efeitos sobre as cores da imagem, também ficam invisíveis até que solicitados
        grayscale_btn = ttk.Button(self.left_side, text="Escala de cinza", command=self.grayscale_effect)
        negative_btn = ttk.Button(self.left_side, text="Efeito de cor negativa", command=self.negative_effect)
        original_btn = ttk.Button(self.left_side, text="Retornar imagem original", command=self.return_to_monke)

        # Adiciona os botões escondidos na lista:
        self.hidden_buttons.extend([grayscale_btn, negative_btn, original_btn])

    def create_resize_panel(self):
        # Cria dois elementos do tipo Label, que agem como um rótulo textual na tela:
        height_lbl = ttk.Label(self.left_side, text="Altura")
        width_lbl = ttk.Label(self.left_side, text="Largura")
        #=======================================================
        # Cria dois elementos do tipo Entry, que recebem input do usuário:
        self.height_box = ttk.Entry(self.left_side)
        self.width_box = ttk.Entry(self.left_side)
        #=======================================================
        # Cria um botão que ao ser clicado, chama uma função utilizando os elementos Entry dessa função
        resize_btn = ttk.Button(self.left_side, text="Redimensionar Imagem", command=self.resize_image)
        # Cria lista para armazenar todos elementos:
        items = [height_lbl, width_lbl, self.height_box, self.width_box, resize_btn]
        #=======================================================
        # Front-end:
        # Posiciona todos os itens da lista de forma específica para design
        for i, item in enumerate(items):
            x_pos = 20 + i * 100
            if isinstance(item, ttk.Entry):
                item.place(x=12 + (i - 2) * 100 , y=420, width=70)
            elif isinstance(item, ttk.Button):
                item.place(x=10, y=450, width=180)
            else:
            		item.place(x=x_pos, y=400, width=70)
#==============================================================================================================================
# Funções para modificar imagens:
#==============================================================================================================================
    # Load Image : object(self) -> file_path image
    # Essa função é aplicada como comando em um botão cuja finalidade é carregar uma imagem,
    # 1. Dado um caminho e uma imagem, atualiza os parâmetros image e file_path de self.
    # 2. A imagem passa por um processo de conversão de (Imagem Pillow -> imagem Tkinter)
    # 3. Para fins de design, a imagem recebe um resize para o tamanho máximo do Canvas.
    # 4. Após essas etapas, atualiza o campo Canvas do módulo Tkinter a fim de mostrar a imagem na UI
    def load_image(self):
        file_path = filedialog.askopenfilename(title="Abrir arquivo de imagem")
        if file_path:
            self.file_path = file_path
            image = Image.open(file_path)
            image = image.resize((600, 600), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)

    # Flip Image Horizontal : object(self.ImageTk) -> ImageTk
    # 1. Dado um objeto com um tipo imageTk, realiza a conversão entre imagemTk para Image do módulo Pillow,
    # 2. Aplica a função transpose sobre a imagem para inverter o eixo horizontal da mesma e realiza a conversão de Image para ImageTk novamente. 
    # 3. Atualiza o campo Canvas do módulo Tkinter a fim de mostrar a imagem na UI
    def flip_image_horizontal(self):
        if self.image:
            image = self.image_to_pillow()
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            self.image = self.pillow_to_image(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.show_error("Erro ao tentar inverter a imagem", "Insira uma imagem para inverter!")

    # Flip Image Vertical : object(self.ImageTk) -> ImageTk
    # 1. Dado um objeto com um tipo imageTk, realiza a conversão entre imagemTk para Image do módulo Pillow,
    # 2. Aplica a função transpose sobre a imagem para inverter o eixo vertical da mesma e realiza a conversão de Image para ImageTk novamente. 
    # 3. Atualiza o campo Canvas do módulo Tkinter a fim de mostrar a imagem na UI
    def flip_image_vertical(self):
        if self.image:
            image = self.image_to_pillow()
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            self.image = self.pillow_to_image(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.show_error("Erro ao tentar inverter a imagem", "Insira uma imagem para inverter!")

    # Grayscale Effect : object(self.ImageTk) -> ImageTk
    # 1. Dado um objeto com um tipo imageTk, realiza a conversão entre imagemTk para Image do módulo Pillow,
    # 2. Aplica a função do módulo Pillow para converter as cores da imagem para Luminância (YCrCb)
    # 3. Realiza reconversão entre tipos de imagem. (Image -> ImageTk)
    # 4. Atualiza o campo Canvas do módulo Tkinter para mostrar a imagem na UI
    def grayscale_effect(self):
        if self.image:
            image = self.image_to_pillow()
            image = image.convert("L")
            self.image = self.pillow_to_image(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.show_error("Falha na troca de cor", "Insira uma imagem para aplicar o efeito de cor!")

    # Negative Effect : object(self.ImageTk) -> ImageTk
    # 1. Dado um objeto com um tipo imageTk, realiza a conversão entre imagemTk para Image do módulo Pillow,
    # 2. Converte a imagem, independente do estado atual para uma imagem do tipo 'RGB' (3-canais), é necessário para utilizar ImageOps do módulo Pillow
    # após a conversão, inverte as cores da imagem com a função do módulo.
    # 3. Realiza reconversão entre tipos de imagem. (Image -> ImageTk)
    # 4. Atualiza o campo Canvas do módulo Tkinter para mostrar a imagem na UI
    def negative_effect(self):
        if self.image:
            image = self.image_to_pillow()
            image = image.convert('RGB')
            image = ImageOps.invert(image)
            self.image = self.pillow_to_image(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.show_error("Falha na troca de cor", "Insira uma imagem para aplicar o efeito de cor negativa!")

    # Return to monke (Return to Original) : object(self.ImageTk) -> ImageTk
    # Dado um objeto com file_path não nulo, abre a imagem a partir do arquivo salvo no caminho informado
    # Converte a imagem carregada em uma imagem do tipo ImageTk e atualiza o Canvas para exibir a imagem na UI.
    def return_to_monke(self):
        if self.file_path:
            image = Image.open(self.file_path)
            self.image = self.pillow_to_image(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            self.show_error("Não foi possível retornar a imagem", "Não foi encontrada a imagem original.")

    # Resize Image : object(self.ImageTk) -> ImageTk
    # Dado um objeto com os elementos image (não nulo), width_box e height_box (Entry type, também não nulos)
    # Caso os valores sejam não nulos e menores ou iguais ao tamanho do canvas, converte a imagem (Tk para Pillow)
    # utiliza a função resize do módulo Tk para realizar a modificação de tamanho da imagem, converte a imagem (Pillow para Tk)
    # Atualiza a imagem no Canvas para exibir na UI.
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

    # Toggle Flip Buttons : object(self.hidden_buttons) -> object(self.hidden_buttons)
    # Função auxiliar para o botão principal: flip_btn
    # Passa para a função principal Toggle Buttons as posições dos botões de inversão na lista hidden_buttons
    def toggle_flip_buttons(self):
        self.toggle_buttons([self.hidden_buttons[0], self.hidden_buttons[1]])

    # Toggle Color Effect Buttons : object(self.hidden_buttons) -> object(self.hidden_buttons)
    # Função auxiliar para o botão principal: color_btn
    # Passa para a função principal Toggle Buttons as posições dos botões de efeitos de cores na lista hidden_buttons
    def toggle_color_effect_buttons(self):
        self.toggle_buttons([self.hidden_buttons[2], self.hidden_buttons[3], self.hidden_buttons[4]])

    # Toggle Buttons : object(self.hidden_buttons) list(buttons) -> ???
    # Dado um objeto com o tipo lista hidden_buttons e uma lista de elementos do tipo Button,
    # Remove a UI todos elementos da lista(hidden_buttons), em seguida, posiciona todos elementos da lista(buttons)
    def toggle_buttons(self, buttons):
        for button in self.hidden_buttons:
            button.place_forget()

        for button in buttons:
            button_index = self.hidden_buttons.index(button)
            if button_index < 2:
            	button.place(x=5, y=20 + (button_index + len(self.menu_buttons) + 1) * 30, width=180)
            else:
            	button.place(x=5, y=20 + ((button_index - 2) + len(self.menu_buttons) + 1) * 30, width=180)

    # Image to pillow : object(self.ImageTk) : object(self.Image)
    # Função auxiliar para conversão (ImageTk -> Image)
    # Dado um objeto com um elemento do tipo ImageTk, realiza uma conversão de tipo para Image do módulo Pillow
    def image_to_pillow(self):
        return ImageTk.getimage(self.image)
        
    # Image to pillow : object(self.Image) : object(self.ImageTk)
    # Função auxiliar para conversão (Image -> ImageTk)
    # Dado um objeto com um elemento do tipo Image, realiza uma conversão de tipo para Image do módulo Tkinter
    def pillow_to_image(self, image):
        return ImageTk.PhotoImage(image)

    # Show Error : object(self), string, string -> tk.messageBox
    # Dado um objeto, retorna uma janela de mensagem explicando algum determinado erro.
    def show_error(self, title, message):
        messagebox.showerror(title=title, message=message)
#=====================================================================================================================================


# Chamada principal do programa:
#=========================================
if __name__ == "__main__":
    app = ImageManipulationApp()
    app.mainloop()

