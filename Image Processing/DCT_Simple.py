import numpy as np
import cv2
import matplotlib.pyplot as plt
from pdb import set_trace as pause

np.set_printoptions(precision=2, suppress=True)

# Esse é o bloco inicial
block = [[127, 123, 125, 120, 126, 123, 127, 128],
[142, 135, 144, 143, 140, 145, 142, 140],
[128, 126, 128, 122, 125, 125, 122, 129],
[132, 144, 144, 139, 140, 149, 140, 142],
[128, 124, 128, 126, 127, 120, 128, 129],
[133, 142, 141, 141, 143, 140, 146, 138],
[124, 127, 128, 129, 121, 128, 129, 128],
[134, 143, 140, 139, 136, 140, 138, 141]] 

# Discrete Cossine Transform: Transformada utilizada para compressão de imagens
# Entrada: bloco (Matriz[N][N]) define o bloco em que será aplicada a fórmula matricial da DCT
# N (Valor inteiro) define qual tamanho de blocos será trabalhado (Mais comum: 8)
# Saída: Matriz[N][N] (Float) também conhecida como Matriz da DCT
# será utilizada com blocos de imagem para fins de compressão
# Exemplo:
# N = 8, Print config = (precision=2, suppress=True)
''' Matriz esperada para dctBase:
[[ 0.35  0.35  0.35  0.35  0.35  0.35  0.35  0.35]
 [ 0.49  0.42  0.28  0.1  -0.1  -0.28 -0.42 -0.49]
 [ 0.46  0.19 -0.19 -0.46 -0.46 -0.19  0.19  0.46]
 [ 0.42 -0.1  -0.49 -0.28  0.28  0.49  0.1  -0.42]
 [ 0.35 -0.35 -0.35  0.35  0.35 -0.35 -0.35  0.35]
 [ 0.28 -0.49  0.1   0.42 -0.42 -0.1   0.49 -0.28]
 [ 0.19 -0.46  0.46 -0.19 -0.19  0.46 -0.46  0.19]
 [ 0.1  -0.28  0.42 -0.49  0.49 -0.42  0.28 -0.1 ]]
''' # Note que a "outputMatrix" é dependente da matriz de entrada
def DCT(N, bloco):
	# Cria a matriz base DCT
	dctBase = np.zeros((N, N))
	for u in range(N):
			alpha_u = np.sqrt(1.0/N) if u == 0 else np.sqrt(2.0/N) # Calc de alpha
			for y in range(N):
					phiLin = np.pi * u * (2.0 * y + 1.0) / ( 2.0  * N ) # Fórmula
					dctBase[u][y] = alpha_u * np.cos(phiLin)
	# Aplicação da fórmula matricial utilizando a matriz da DCT e o bloco original
	outputMatrix = np.dot(np.dot(dctBase, bloco), dctBase.T)
			
	return outputMatrix

# Quantização: Matriz para anular coeficientes restantes da aplicação da DCT sobre um bloco
# Entrada: N (Valor inteiro), fator(Valor inteiro), N se refere ao tamanho da matriz
# fator (Valor inteiro) se refere ao nível de compressão da imagem
# bloco (Matriz[N][N]) espera-se uma matriz com a DCT aplicada para realizar a quantização
# Saída: Matriz[N][N] paramétrica sugerida pelo padrão JPEG, já quantizada.
# Exemplo:
''' Matriz esperada em qt:
[[  1.  11.  21.  31.  41.  51.  61.  71.]
 [ 11.  21.  31.  41.  51.  61.  71.  81.]
 [ 21.  31.  41.  51.  61.  71.  81.  91.]
 [ 31.  41.  51.  61.  71.  81.  91. 101.]
 [ 41.  51.  61.  71.  81.  91. 101. 111.]
 [ 51.  61.  71.  81.  91. 101. 111. 121.]
 [ 61.  71.  81.  91. 101. 111. 121. 131.]
 [ 71.  81.  91. 101. 111. 121. 131. 141.]]
''' 
def Quantization(N, fator, bloco):
	# Cria a matriz base qt:
	qt = np.zeros((N, N))
	for i in range(N):
		for j in range(N):
			qtValue = 1 +  (i + j) * fator
			qt[i][j] = qtValue
	# Aplica a fórmula da quantização matricial sobre o bloco da DCT utilizando a matriz qt
	outputMatrix = np.multiply(qt, np.round(np.divide(bloco, qt))).astype(int)
	return outputMatrix
	
# Inverse Discrete Cossine Transform: Transformada inversa do cosseno
# Entrada: N (Valor inteiro), bloco (Matriz[N][N]), N se refere ao tamanho da matriz
# o bloco esperado é uma matriz que esteja processada anteriormente por efeitos da DCT e de uma Quantização
# Saída: Matriz[N][N] com a IDCT aplicada, neste ponto é considerada uma compressão do bloco original.
# Exemplo: A matriz da IDCT é a mesma do exemplo da DCT, para o N=8
def IDCT(N, bloco):
	# Cria matriz DCT -! Note que isso talvez não seja necessário.
	dctBase = np.zeros((N, N))
	for u in range(N):
			alpha_u = np.sqrt(1.0/N) if u == 0 else np.sqrt(2.0/N) # Calc de alpha
			for y in range(N):
					phiLin = np.pi * u * (2.0 * y + 1.0) / ( 2.0  * N ) # Fórmula
					dctBase[u][y] = alpha_u * np.cos(phiLin)
	# Aplica a fórmula inversa da DCT sobre o bloco quantizado
	outputMatrix = np.round(np.dot(np.dot(dctBase.T, bloco), dctBase)).astype(int)
	
	return outputMatrix
			
#================================
# Main():
#================================
imagem = cv2.imread("clock.tiff", cv2.COLOR_BGR2GRAY)

'''
imagemSplit = np.split(imagem, 32, axis=-1)
print(np.array(imagemSplit))
imagemSplit = np.split(np.array(imagemSplit), 32, axis=-2)
#print(np.array(imagemSplit).shape)
imagemSplit = np.array(imagemSplit).reshape((1024, 8, 8))
#print(imagemSplit)
#pause()
'''

# Split:
n = 8
heightBlocks = imagem.shape[0] // n
widthBlocks = imagem.shape[1] // n

blockSplit = []
for x in range(heightBlocks):
	for y in range(widthBlocks):
		blockSplit.append(imagem[y*n:(y+1)*n, x*n:(x+1)*n])
		
#============================
blockDCT = []
# Aplicação da fórmula da DCT sobre o bloco original:
for i in range(1024):
	blockDCT.append(DCT(8, blockSplit[i]))
	#print(" Aplicação da DCT sobre o bloco original: \n", blockDCT[i])

# Aplicação da quantização para anular coeficientes sobre o bloco da DCT aplicada:
qt = []
for i in range(1024):
	qt.append(Quantization(8, 10, blockDCT[i]))
#print("\n Aplicação de Quantização sobre um bloco com a DCT aplicada: \n", qt)

# Conversão Inversa da DCT para trazer o bloco novamente:
compressedBlock = []
for i in range(1024):
	compressedBlock.append(IDCT(8, qt[i]))
	#print("\n Aplicação da IDCT sobre o bloco Quantizado: \n", compressedBlock[i])

compressedBlock = np.array(compressedBlock)
#print(compressedBlock.shape)
#=============================

#=======================================
# Join blocks:
#=======================================
# transpose is necessary to arrange the axis in order (1,0) refers to Y axis and (2,3) refers to X axis
'''
Transpose:
1,3,0,2 -> Flipped, rotated
1,2,0,3 -> Original image
'''
imagemSplit = compressedBlock.reshape(heightBlocks, widthBlocks, n, n).transpose(1,2,0,3).reshape(heightBlocks*n, widthBlocks*n)


'''
imagemSplit = np.array(np.split(imagemSplit, 32, axis=0))
#print(imagemSplit.shape)
imagemSplit = np.stack(imagemSplit, axis=2)
#imagemSplit = imagemSplit.reshape(32, 8, 256)
print(np.array(imagemSplit).shape)
imagemSplit = imagemSplit.reshape(256, 256).T
'''

#==========================
# Plot()
#==========================
fig, axs = plt.subplots(1, 2)

axs[0].imshow(imagem, cmap='gray', vmin=0, vmax=255)
axs[1].imshow(imagemSplit, cmap='gray', vmin=0, vmax=255)

plt.show()




