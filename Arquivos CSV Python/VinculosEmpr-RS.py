import csv
#===============================================
# Monitoria de introdução à programação:
#-----------------------------------------------
# Objetivo: Dado um arquivo CSV disponibilizado no site:
# https://dados.rs.gov.br/dataset/dee-3677
# Retornar uma lista de dados legíveis com o seguinte formato:
# Indíce | Município | Vínculos-Empregatícios
# 1        Alegrete            10
# 2        Porto Alegre       120
# ...
#===============================================
# Função de busca:
def Municipios(src, municipios, ano, msg):
	index = 0                         # Conta índice
	print("=" * 100)                  # Estético
	print(msg)                        # Parâmetro do programador
	print("=" * 100)                  # Estético
	print(f'Indice\tNome do Município\t\t\tVínculos')

  # Verificação dos dados contidos na Estr. de Dados do Município, passado como parâmetro
	for municipio, dados in municipios.items(): 
		if municipio.startswith(src.upper()):         # Os nomes são todos iniciados em maiúsculas
				print(f'{index+1}\t{municipio:<35}\t{dados[ano]:20}')
				index += 1

# Arquivo:
'''
  Note que a mensagem deve ser modificada na passagem da função
  dependendo do arquivo.
'''
#arquivo = "VinculoEmpregaticioAte14.csv"
#arquivo = "VinculoEmpregaticioAte17.csv"
#arquivo = "VinculoEmpregaticioAte24.csv"
#arquivo = "VinculoEmpregaticioAte29.csv"
arquivo = "VinculoEmpregaticioAte39.csv"
#arquivo = "VinculoEmpregaticioAte49.csv"
#arquivo = "VinculoEmpregaticioAte60.csv"
#arquivo = "VinculoEmpregaticioMais60.csv"

# Associa o ano com a coluna específica do CSV:
anoColuna = {
  2010 : 4,
  2011 : 5,
  2012 : 6,
  2013 : 7,
  2014 : 8,
  2015 : 9,
  2016 : 10,
  2017 : 11,
  2018 : 12,
  2019 : 13,
  2020 : 14
}

# Dicionário para armazenar os dados dos municípios
municipios_dados = {}

with open(arquivo, 'r', encoding='latin1') as f:
	leitor = csv.reader(f)
	cabecalhos = next(leitor)
	for row in leitor:
		municipio = row[0]
		dados = {int(ano): row[coluna] for ano, coluna in anoColuna.items()}
		municipios_dados[municipio] = dados

while True:
	ano = int(input('Informe o ano para busca entre 2010 e 2020 ou zero para encerrar: '))
	if not ano:
		break
	# Ano Válido:
	if ano >= 2010 and ano <= 2020:
		# Busca por inicial de municípios:
		inicial_muni = (input('Informe a inicial do município do RS que deseja buscar: '))
		Municipios(inicial_muni, municipios_dados, ano, "Vínculos Empregatícios nas idades de 30 à 39 anos")
	else:
		# Caso de Erro:
		print("O ano escolhido não tem dados, informe novamente ou zero para encerrar o programa.")

		
