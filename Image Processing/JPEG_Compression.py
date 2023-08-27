from math import log10, sqrt
from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from pdb import set_trace as pause

'''
TODO :
	Fix Documentation for Quantization Function
	Fix Documentation Examples for PSNR Function
	Python file modulations?
'''
# For better analysis of Matrix data
#np.set_printoptions(precision=2, suppress=True)

#=========================================
# Functions():
#=========================================
# Discrete Cossine Matrix: Number Array[N][N] -> Array[N][N]
# Given a size and a bidimensional array of same size calculates DCT array
# for determined size. *(note: initial array is expected to be zeros)
# Returns DCT array.
# Example:
# N = 8, Print config = (precision=2, suppress=True)
''' Expected bidimensional array when n equals 8:
[[ 0.35  0.35  0.35  0.35  0.35  0.35  0.35  0.35]
 [ 0.49  0.42  0.28  0.1  -0.1  -0.28 -0.42 -0.49]
 [ 0.46  0.19 -0.19 -0.46 -0.46 -0.19  0.19  0.46]
 [ 0.42 -0.1  -0.49 -0.28  0.28  0.49  0.1  -0.42]
 [ 0.35 -0.35 -0.35  0.35  0.35 -0.35 -0.35  0.35]
 [ 0.28 -0.49  0.1   0.42 -0.42 -0.1   0.49 -0.28]
 [ 0.19 -0.46  0.46 -0.19 -0.19  0.46 -0.46  0.19]
 [ 0.1  -0.28  0.42 -0.49  0.49 -0.42  0.28 -0.1 ]]
'''
def MatrixDCT(N, block):
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
def DCT(block, dctArray):
	# This applies the DCT (matrix-based) function on a image block:
	outputMatrix = np.dot(np.dot(dctArray, block), dctArray.T)
	# Returns it:
	return outputMatrix
#==========================================
# Inverse Discrete Cossine Transform: Array[N][N] Array[N][N] -> Array[N][N] (time domain)
# Given a array and a array correspondent to DCT matrix,
# Returns a array in time domain 
# Exemplo: IDCT array is the same as DCT array, but it's treated differently on matrix-based formula
def IDCT(block, dctArray):
	# Calculates inverse DCT function applied on a bidimensional array (matrix-based formula)
	outputMatrix = np.round(np.dot(np.dot(dctArray.T, block), dctArray)).astype(int)
	# Returns it:
	return outputMatrix
#=========================================
# Quantization: Number Number Array[N][N] -> Array[N][N]
# Given a size, a quantization factor and a bidimensional array
# Returns a bidimensional array with anulated coefficients suggested by JPEG standard
# N -> Integer value, refers to Array size
# factor -> Interger value, refers to how much the coefficients will be reduced
# Array -> Expected a bidimensional array with DCT function applied beforehand.
# Examples:
''' 
...
'''
def Quantization(QF, bloco, size):
	# Hardcoded Quantization Table:
	qtTable = np.array([
		[16, 11, 10, 16, 24, 40, 51, 61],
		[12, 12, 14, 19, 26, 58, 60, 55],
		[14, 13, 16, 24, 40, 57, 69, 56],
		[14, 17, 22, 29, 51, 84, 80, 62],
		[18, 22, 37, 56, 68, 109, 103, 77],
		[24, 35, 55, 64, 81, 104, 113, 92],
		[49, 64, 78, 87, 103, 121, 120, 101],
		[72, 92, 95, 98, 112, 100, 103, 99]
	])

	qtTable = cv2.resize(qtTable.astype(float), dsize=(size, size), interpolation=cv2.INTER_CUBIC)
	
	#print(qtTable)
	
	# Based on Quality Factor value, applies a formula otherwise, another formula
	if QF < 50:
		S = 5000 / QF
	else:
		S = 200 - (2 * QF)
	# Quantization Matrix:
	Q = np.floor((S * qtTable + 50) / 100)
			
	# Applies quantization formula (matrix-based) on the array passed as parameter:
	outputMatrix = np.multiply(Q, np.round(np.divide(bloco, Q))).astype(int)
	return outputMatrix
#=========================================
# SplitImage : Number Number Array Number -> Array
# Given a number of rows, columns, block size (n²) and a array to pick values from,
# Returns a 3D array with size rows * columns, blockSize, blockSize.
# Example:
# Too lazy to write about it now, but it splits a image. That is it.
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
def BlocksToImage(rows, columns, blockArray, blockSize):
	# This concatenates all blocks back to a image format, transpose is needed to fix block locations.
	block = blockArray.reshape(rows, columns, blockSize, blockSize).transpose(1,2,0,3).reshape(rows*blockSize, columns*blockSize)
	''' Transpose:
	1,3,0,2 -> Flipped and mirrored image
	1,2,0,3 -> Original image
	'''
	return block

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
def PSNR(original, compressed):
  mse = np.square(np.subtract(original, compressed)).mean()
  if(mse == 0):  # No noise found, both images are equal.
    return float('inf')
  psnr = 20 * log10(255.0 / sqrt(mse))
  return psnr
#================================
# Main():
#================================
imagem = cv2.imread("clock.tiff", cv2.COLOR_BGR2GRAY)

# Important stuff
#==========================
# 4, 8, 16, 32
blockTypes = [4, 8, 16, 32]
MINFACTOR = 1
MAXFACTOR = 90

# Lists for Graph Plot
#==========================
ssimValues = [[] for _ in blockTypes]
psnrValues = [[] for _ in blockTypes]
bppValues = [[] for _ in blockTypes]
compressFactors = [[] for _ in blockTypes]

# idx will be a index value between 0 and len(blockTypes)
# while blockSize will be a value inside blockTypes list
#================================================
for idx, blockSize in enumerate(blockTypes):
	heightBlocks = imagem.shape[0] // blockSize # Finds how many blocks there's based on blockSize
	widthBlocks = imagem.shape[1] // blockSize # Same as above but with width

	# Initializates DCT standard block: 
	#===================================
	dctBlock = np.zeros((blockSize, blockSize), dtype=float)
	dctBlock = np.array(MatrixDCT(blockSize, dctBlock))

	# Split image in blocks
	#==========================
	modifiedImage = SplitImage(heightBlocks, widthBlocks, imagem, blockSize)
	modifiedImage = np.array(modifiedImage) # Conversion to Array

	# Apply JPEG Algorithm to image: Values between 1 and 90
	#=========================================================
	for factor in range(MINFACTOR, MAXFACTOR+1):
		# Applies DCT
		treatmentBlock = []
		for i in range(heightBlocks*widthBlocks): 
			treatmentBlock.append(DCT(modifiedImage[i], dctBlock))
		
		# Applies Quantization
		treatmentBlockTwo = []
		notZeros = 0
		for i in range(heightBlocks*widthBlocks):
			treatmentBlockTwo.append(Quantization(factor, treatmentBlock[i], blockSize))
			valuesZero = np.isclose(treatmentBlockTwo[i], 0)
			notZeros += (blockSize * blockSize - np.sum(valuesZero)) 
		
		# Applies Inverse DCT
		compressedImage = []
		for i in range(heightBlocks*widthBlocks):
			compressedImage.append(IDCT(treatmentBlockTwo[i], dctBlock))

		# Return image from blocks
		#==========================
		compressedImage = np.array(compressedImage)
		compressedImage = BlocksToImage(heightBlocks, widthBlocks, compressedImage, blockSize)

		# PSNR Values and Etcetera
		#==========================
		PSNRValue = PSNR(imagem, compressedImage)
		SSIMValue = ssim(imagem, compressedImage, data_range=imagem.max() - compressedImage.min())
		bppValue = (notZeros / (imagem.shape[0] * imagem.shape[1])) * 8
		
		# Lista de Verificações:
		#==========================
		if(factor % 10 == 0):
			ssimValues[idx].append(SSIMValue)
			psnrValues[idx].append(PSNRValue)
			bppValues[idx].append(bppValue)
			compressFactors[idx].append(factor)
		

		print(f"For blockSize: {blockSize} For compression factor {factor}: \n\tPSNR Value: {PSNRValue}\n\tSSIM Value: {SSIMValue}")
		print(f"\t BPP Value: {bppValue}")

#==========================
# Save Image()
#==========================
#cv2.imwrite("CompressedClock.jpg", compressedImage)

#==========================
# Plot()
#==========================
fig, axs = plt.subplots(1, 3, figsize=(100, 50))
'''
axs[0][0].imshow(imagem, cmap='gray', vmin=0, vmax=255)
axs[0][0].set_title("Original")
axs[0][1].imshow(compressedImage, cmap='gray', vmin=0, vmax=255)
axs[0][1].set_title(f"Compressão Fator {factor}")
'''
#================================
# Graph Plots()
#================================
for idx, blockSize in enumerate(blockTypes):
	# SSIM vs BPP
	axs[0].plot(bppValues[idx], ssimValues[idx], label=f'Block Size {blockSize}', marker='o')
	axs[0].set_xlabel('BPP Value')
	axs[0].set_ylabel('SSIM')
	axs[0].set_title('SSIM vs BPP')
	axs[0].legend()

	# PSNR vs BPP
	axs[1].plot(bppValues[idx], psnrValues[idx], label=f'Block Size {blockSize}', marker='o')
	axs[1].set_xlabel('BPP Value')
	axs[1].set_ylabel('PSNR')
	axs[1].set_title('PSNR vs BPP')
	axs[1].legend()
	'''
	# BPP vs Quality Factor
	axs[2].plot(compressFactors[idx], bppValues[idx], label=f'Block Size {blockSize}', marker='o')
	axs[2].set_xlabel('Quality Factor')
	axs[2].set_ylabel('BPP')
	axs[2].set_title('BPP vs Quality Factor')
	axs[2].legend()
	'''
plt.show()
