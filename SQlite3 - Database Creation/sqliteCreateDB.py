import sqlite3

# Dada uma estrutura de tabela SQlite, cria uma TABLE de SQlite em um arquivo .db
def CreateTable(struture):
	cursor = conn.cursor()
	cursor.execute(struture)
	print("Tabela criada com sucesso")

# CRUD -> Create values on tables.
def InsertValues():
	while True:
		cursor = conn.cursor()
		itemName = input('Nome do item: ')
		if not itemName:
			break;
		itemCategory = input('Categoria: ')
		itemDescript = input('Descrição: ')
		itemShopID = input('Identificação de Shop: ')

		cursor.execute("""
		INSERT INTO items (nome, category, description, shop)
		VALUES (?, ?, ?, ?)
		""", (itemName, itemCategory, itemDescript, itemShopID))

		conn.commit()
		print("Dados inseridos na tabela.")

# CRUD -> Read
def ShowTable(structure):
	cursor = conn.cursor()
	cursor.execute(structure)
	
	print("-" * 100)
	for linha in cursor.fetchall():
		print(linha)
	print("-" * 100)
			
# CRUD -> Update
def UpdateValues():
	while True:
		cursor = conn.cursor()
		identificator = int(input('Informe o ID do item: '))
		if identificator == 0:
			break;
			
		itemName = input('Nome do item: ')
		itemCategory = input('Categoria: ')
		itemDescript = input('Descrição: ')
		itemShopID = input('Identificação de Shop: ')

		cursor.execute(""" UPDATE items 
		SET nome = ?, category = ?, description = ?, shop = ? 
		WHERE id = ?
		""", (itemName, itemCategory, itemDescript, itemShopID, identificator))
		
		conn.commit()
		print(f"Updated register: {identificator}")

# CRUD -> Delete
def DeleteItem():
	while True:
		cursor = conn.cursor()
		identificator = int(input('Informe o ID do que deseja remover: '))
		if identificator == 0:
			break;
		
		cursor.execute("""DELETE FROM items 
		WHERE id = ?
		""", (identificator,))
		
		conn.commit()
		print(f"Removed register: {identificator}")

# Inicia Conexão
conn = sqlite3.connect('itemData.db')

# Items Table
#id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#nome TEXT NOT NULL,
#category TEXT NOT NULL,
#description TEXT NOT NULL,
#shop INTEGER NOT NULL
while True:
	print("1. Inserir Elementos") # Create
	print("2. Mostrar a tabela") # Read
	print("3. Atualizar item na tabela") # Update
	print("4. Remover item da tabela") # Delete
	print("0. Fechar Aplicação")

	menuOption = int(input('Infome a opção: '))
	if menuOption == 0:
		break;
	
	match menuOption:
		case 1:
			InsertValues()
		case 2:
			ShowTable(""" SELECT * FROM items; """)
		case 3:
			UpdateValues()
		case 4:
			DeleteItem()
			
			
# Fecha conexão
conn.close()
