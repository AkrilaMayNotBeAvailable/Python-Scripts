from numba import njit
from skimage.metrics import structural_similarity as ssim
from math import log10, sqrt
import numpy as np
import matplotlib.pyplot as plt
import time
import cv2

# Constants:
#=========================================
QT_MATRIX = np.array([
	[16, 11, 10, 16, 24, 40, 51, 61],
	[12, 12, 14, 19, 26, 58, 60, 55],
	[14, 13, 16, 24, 40, 57, 69, 56],
	[14, 17, 22, 29, 51, 84, 80, 62],
	[18, 22, 37, 56, 68, 109, 103, 77],
	[24, 35, 55, 64, 81, 104, 113, 92],
	[49, 64, 78, 87, 103, 121, 120, 101],
	[72, 92, 95, 98, 112, 100, 103, 99]
])

# Uma ListaDeImagens é:
# 1. Vazia ou,
# 2. List[string, ListaDeImagens];

# Uma CV2ImageStructure é:
# 1. Vazia ou,
# 2. List[numpy.ndarray, CV2ImageStructure]

#=========================================
# Functions():
#=========================================
# Discrete Cossine Matrix: Array[N][N] int -> Array[N][N]
# Given a size and a bidimensional array of same size calculates DCT array
# for determined size. *(note: initial array is expected to be zeros)
# Returns DCT array.
# Example:
# N = 8, Print config = (precision=2, suppress=True)
''' Expected bidimensional array when n equals 8:
[[ 0.35  0.35  0.35  0.35  0.35  0.35  0.35  0.35]
 ...
 [ 0.1  -0.28  0.42 -0.49  0.49 -0.42  0.28 -0.1 ]]
'''
''' SUPPORT FOR NUMBA - Numpy operations, nested for loop '''
# Runtime:
# Numba -> 0.02009868621826172 ms
# No Numba -> 0.5078816413879395 ms
def MatrixDCT(block, N):
	for u in range(N):
		alpha_u = np.sqrt(1.0/N) if u == 0 else np.sqrt(2.0/N) # Calc de alpha
		for y in range(N):
			phiRow = np.pi * u * (2.0 * y + 1.0) / ( 2.0  * N ) # Fórmula
			block[u][y] = alpha_u * np.cos(phiRow)
	return block
	
#=========================================
# Discrete Cossine Transform: Array[N][N] Array[N][N] -> Array[N][N] (frequency domain)
# Given DCT Matrix and a bidimensional array of same size,
# Returns a bidimensional array of same size in frequency domain
# Example:
# Should return a high value on the first index and low values overall
''' Something like this:
[[ 1066 -5.04 0.17 -5.18 -5.5 -0.84 2.37 0.86]
	.........
 [-53.65 4.56 8.17 -1.71 7.99 2.22 0.78 3.66]]
'''
''' NO SUPPORT FOR NUMBA - Double dot operation using arrays '''
def DCT(block, dctArray):
	# This applies the DCT (matrix-based) function on a image block:
	outputMatrix = np.dot(np.dot(dctArray, block), dctArray.T)
	# Returns it:
	return outputMatrix

#==================================================================
# Quantization: np.array np.array int -> np.array
# Given a image block array, a quantization table array and a quality factor,
# Returns a array with JPEG proposed quantization applied
''' NUMBA SUPPORT ? - Cannot use it with astype(int) function '''
def Quantization(block, qt, QF):
	# Based on Quality Factor value, applies a formula otherwise, another formula
	if QF < 50:
		S = 5000 / QF
	else:
		S = 200 - (2 * QF)
	# Quantization Matrix:
	Q = np.floor((S * qt + 50) / 100)
			
	# Applies quantization formula (matrix-based) on the array passed as parameter:
	outputMatrix = np.multiply(Q, np.round(np.divide(block, Q))).astype(int)
	return outputMatrix

#==========================================
# Inverse Discrete Cossine Transform: Array[N][N] Array[N][N] -> Array[N][N] (time domain)
# Given a array and a array correspondent to DCT matrix,
# Returns a array in time domain 
# Exemplo: IDCT array is the same as DCT array, but it's treated differently on matrix-based formula
''' NO SUPPORT FOR NUMBA - Double dot operation using arrays '''
def IDCT(block, dctArray):
	# Calculates inverse DCT function applied on a bidimensional array (matrix-based formula)
	outputMatrix = np.round(np.dot(np.dot(dctArray.T, block), dctArray)).astype(int)
	# Returns it:
	return outputMatrix
	
#========================================
# PSNR : Array Array -> Number
# Given two arrays representing a original image on the first and a compressed image as second,
# Returns a floating-point value based on PSNR formula
# Example:
''' Based on clock image with compression factors 1:10
For factor 10: PSNR return value -> 33.312639...
For factor 5: PSNR return value -> 36.170812...
For factor 1: PSNR return value -> 43.555596...
'''
''' NUMBA SUPPORT ? - Cannot use it with float('inf') function '''
def PSNR(original, compressed):
  mse = np.square(np.subtract(original, compressed)).mean()
  if(mse == 0):  # No noise found, both images are equal.
    return float('inf')
  psnr = 20 * log10(255.0 / sqrt(mse))
  return psnr

#==================================================================
# LoadMultipleImages: ListaDeImagens -> CV2ImageStructure
# Given one ListaDeImagens, with the path of each image desired
# Returns a list with each image found.
''' NO SUPPORT FOR NUMBA - CV2 Image Read '''
#==================================================================
def LoadMultipleImages(images):
	imageList = []
	for pathFile in images:
		 imageList.append(cv2.imread(pathFile, cv2.COLOR_BGR2GRAY))
	return imageList

#==================================================================
# QuantizationTableResize: np.array int -> np.array
#	Given a matrix and a integer representing size,
# Returns a matrix resized by BICUBIC interpolation of given size
''' NO SUPPORT FOR NUMBA - CV2 Interpolation '''
#==================================================================
def QtResizeBICUBIC(qtMatrix, size):
	qtMatrix = cv2.resize(qtMatrix.astype(float), dsize=(size, size), interpolation=cv2.INTER_CUBIC)
	return qtMatrix
	
#==================================================================
# MultipleSizeQTMatrixDef: np.array np.array (np.array int -> np.array) -> ListOf(np.array)
# Given a quantization matrix and a list of different sizes,
# Returns a list of each resized matrix.
''' NO SUPPORT FOR NUMBA - CV2 function high-order calls '''
#==================================================================
def MultipleSizeQTMatrixDef(reference, sizeList, resizeMethod):
	qtData = []
	for size in sizeList:
		resizedMatrix = resizeMethod(reference, size)
		qtData.append(resizedMatrix)
	return qtData

#==================================================================
# PlotMultipleImages: CV2ImageStructure -> Matplotlib_GUI_Window
# Given one or more images, 
# Returns a window displaying the image(s).
''' NO SUPPORT FOR NUMBA - MatPlotLib plots '''
#==================================================================
def PlotMultipleImages(images):
	for index, image in enumerate(images):
		plt.figure()
		plt.imshow(image, cmap='gray', vmin=0, vmax=255)
		plt.suptitle(f'Image plot - {index}')
		
	plt.show()

#=========================================
# SplitImage : Number Number Array Number -> Array
# Given a number of rows, columns, block size (n²) and a array to pick values from,
# Returns a 3D array with size rows * columns, blockSize, blockSize.
# Example:
# Too lazy to write about it now, but it splits a image. That is it.
''' NO SUPPORT FOR NUMBA - Numpy split method '''
def SplitImage(rows, columns, imageArray, blockSize):		
	splitBlock = np.split(np.array(imageArray), rows, axis=1) # Divide rows
	splitBlock = np.split(np.array(splitBlock), columns, axis=0) # Divide columns
	splitBlock = np.array(splitBlock).reshape((rows * columns, blockSize, blockSize)) # Gather Axis 0, 1 together
	
	return splitBlock
	
#=========================================
# BlocksToImage : Number Number Array Number -> Array
# Given a number of rows, columns, block size (n²) and a array to pick values from,
# Returns a bidimensional array, transposed based on SplitImage().
# Example:
# Also too lazy to write about it. But it merges what you did with SplitImage(). Consider this a inverse of SplitImage
''' NO SUPPORT FOR NUMBA - Numpy not contiguous array '''
def BlocksToImage(rows, columns, blockArray, blockSize):
	# This concatenates all blocks back to a image format, transpose is needed to fix block locations.
	block = blockArray.reshape(rows, columns, blockSize, blockSize).transpose(1,2,0,3).reshape(rows*blockSize, columns*blockSize)
	''' Transpose:
	1,3,0,2 -> Flipped and mirrored image
	1,2,0,3 -> Original image
	'''
	return block

#===================================
# Main()
#===================================
# Execution time test
startPoint = time.time()

pathFiles = ["5.2.08.tiff", "5.2.09.tiff", "5.2.10.tiff", "7.1.01.tiff", "7.1.02.tiff", "7.1.03.tiff", "7.1.05.tiff", "7.1.06.tiff", "7.1.07.tiff", "7.1.08.tiff"]

blockSize = [4, 8, 16, 32]
imageList = LoadMultipleImages(pathFiles)
quantizationMatrixList = MultipleSizeQTMatrixDef(QT_MATRIX, blockSize, QtResizeBICUBIC)

compressedImages = []

factorList = [10, 50, 90]

# Data Verification lists:
ssimValues = [[[] for _ in blockSize] for _ in pathFiles]
psnrValues = [[[] for _ in blockSize] for _ in pathFiles]
bppValues = [[[] for _ in blockSize] for _ in pathFiles]
compressFactors = [[[] for _ in blockSize] for _ in pathFiles]
#======================================
for image_index, image in enumerate(imageList): # (Nested loop count = 1)
	for index, size in enumerate(blockSize): # (Nested loop count = 2)
		# Initialize DCT array:
		dctBlock = np.zeros((size, size), dtype=float)
		dctBlock = MatrixDCT(dctBlock, size)
		
		# Check image split blocks amount:
		rows = image.shape[0] // size 
		columns = image.shape[1] // size
		
		# Breaks Image into blocks
		splitImage = SplitImage(rows, columns, image, size)
		splitImage = np.array(splitImage)
		
		# Runs through each compression on factorList (Nested loop count = 3)
		#==========================================================================
		for factor in factorList:
			# Applies DCT
			treatmentBlock = []
			for i in range(rows*columns): 
				treatmentBlock.append(DCT(splitImage[i], dctBlock))
				
			# Applies Quantization
			treatmentBlockTwo = []
			notZeros = 0
			for i in range(rows*columns):
				treatmentBlockTwo.append(Quantization(treatmentBlock[i], quantizationMatrixList[index], factor))
				valuesZero = np.isclose(treatmentBlockTwo[i], 0)
				notZeros += (size * size - np.sum(valuesZero))
				
			# Applies Inverse DCT
			compressedImage = []
			for i in range(rows*columns):
				compressedImage.append(IDCT(treatmentBlockTwo[i], dctBlock))
			
			# Return Image from blocks
			compressedImage = np.array(compressedImage)
			compressedImage = BlocksToImage(rows, columns, compressedImage, size)
			
			# PSNR Values and Etcetera
			#==========================
			PSNRValue = PSNR(image, compressedImage)
			SSIMValue = ssim(image, compressedImage, data_range=image.max() - compressedImage.min())
			bppValue = (notZeros / (image.shape[0] * image.shape[1])) * 8
			
			# This updates each value as one image
			ssimValues[image_index][index].append(SSIMValue)
			psnrValues[image_index][index].append(PSNRValue)
			bppValues[image_index][index].append(bppValue)
			compressFactors[image_index][index].append(factor)
			print(f"For blockSize: {size} For compression factor {factor}: \n\tPSNR Value: {PSNRValue}\n\tSSIM Value: {SSIMValue}")
			print(f"\t BPP Value: {bppValue}")
	# 3*4 Imagens em compressão 90
	compressedImages.append(compressedImage)

# Execution time test:
endPoint = time.time()
print("Tempo de execução: ", (endPoint - startPoint), "ms")


# Calcula a média de valores de PSNR para cada bloco
#============================================================
mediaPSNR = [[] for _ in blockSize]
mediaSSIM = [[] for _ in blockSize]
mediaBPP = [[] for _ in blockSize]

for idx, size in enumerate(blockSize):
	for quality, _ in enumerate(factorList):
		psnrCatcher = []
		ssimCatcher = []
		bppCatcher = []
		
		for imageindex, _ in enumerate(imageList):
			PSNRval = psnrValues[image_index][idx][quality]
			SSIMval = ssimValues[image_index][idx][quality]
			BPPval = bppValues[image_index][idx][quality]
			
			psnrCatcher.append(PSNRval)
			ssimCatcher.append(SSIMval)
			bppCatcher.append(BPPval)

		mediaPSNR[idx].append(np.mean(psnrCatcher, axis=0))
		mediaSSIM[idx].append(np.mean(ssimCatcher, axis=0))
		mediaBPP[idx].append(np.mean(bppCatcher, axis=0))
#============================================================
print(mediaPSNR)
print(psnrValues)


for imageindex, image in enumerate(imageList):
	plt.figure(figsize=(12, 6))
	plt.suptitle(f'SSIM and PSNR - {pathFiles[imageindex]}')
	for idx, size in enumerate(blockSize):
		# SSIM vs BPP
		plt.subplot(1, 2, 1)
		plt.plot(bppValues[imageindex][idx], ssimValues[imageindex][idx], label=f'Block Size {size}', marker='o')
		plt.xlabel('BPP Value')
		plt.ylabel('SSIM')
		plt.title('SSIM vs. BPP')
		plt.legend()
		
		# PSNR vs BPP
		plt.subplot(1, 2, 2)
		plt.plot(bppValues[imageindex][idx], psnrValues[imageindex][idx], label=f'Block Size {size}', marker='o')
		plt.xlabel('BPP Value')
		plt.ylabel('PSNR')
		plt.title('PSNR vs BPP')
		plt.legend()
					
plt.figure(figsize=(12, 6))
for idx, size in enumerate(blockSize):
	plt.subplot(1, 2, 1)
	plt.plot(mediaBPP[idx], mediaSSIM[idx], label=f'Average SSIM Block: {size}', marker='o')
	plt.xlabel('Avg. BPP Value')
	plt.ylabel('Avg. SSIM')
	plt.title(f'Average SSIM for {len(imageList)} Images')
	plt.legend()
	
	plt.subplot(1, 2, 2)
	plt.plot(mediaBPP[idx], mediaPSNR[idx], label=f'Average PSNR Block: {size}', marker='o')
	plt.xlabel('Avg. BPP Value')
	plt.ylabel('Avg. PSNR')
	plt.title(f'Average PSNR for {len(imageList)} Images')
	plt.legend()
	
plt.show()

'''
for blockidx, block in enumerate(quantizationMatrixList):
	plt.figure(figsize=(12, 6))
	plt.suptitle(f'Quantization Block size {blockSize[blockidx]}')
	
	plt.subplot(1, 2, 1)
	plt.imshow(block, cmap='gray', vmin=0, vmax=255)
	plt.title('(Grayscale) Block Plot')
	
	plt.subplot(1, 2, 2)
	plt.plot(block)
	plt.xlabel('Array Position')
	plt.ylabel('Pixel Color freq.')
	plt.title('Block Color Frequency x Position on array')
	

plt.show()
'''

#PlotMultipleImages(quantizationMatrixList)
