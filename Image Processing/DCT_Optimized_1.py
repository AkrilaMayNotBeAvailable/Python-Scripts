import numpy as np
import cv2
import matplotlib.pyplot as plt
from pdb import set_trace as pause

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
''' Expected array for quantization for N = 8 and factor = 10:
[[  1.  11.  21.  31.  41.  51.  61.  71.]
 [ 11.  21.  31.  41.  51.  61.  71.  81.]
	.... (goes in this sequence)
 [ 61.  71.  81.  91. 101. 111. 121. 131.]
 [ 71.  81.  91. 101. 111. 121. 131. 141.]]
 
 Return expected based on DCT example:
[[ 1066 0 0 0 0 0 0 0 ]
	........
	-71 0 0 0 0 0 0 0]]
'''
def Quantization(N, fator, bloco):
	# Base Quantization array:
	qt = np.zeros((N, N))
	for i in range(N):
		for j in range(N):
			qtValue = 1 +  (i + j) * fator
			qt[i][j] = qtValue
			
	# Applies quantization formula (matrix-based) on the array passed as parameter:
	outputMatrix = np.multiply(qt, np.round(np.divide(bloco, qt))).astype(int)
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
#================================
# Main():
#================================
imagem = cv2.imread("clock.tiff", cv2.COLOR_BGR2GRAY)

# Important stuff
#==========================
blockSize = 8 # This is used everywhere, change it for different block slices, DCT size etc.
factor = 10 # This is used in Quantization function as control for image compress/quality
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

# Apply JPEG Algorithm to image:
#===============================
treatmentBlock = [] # Those lists bother me aswell, it would be more optimized to use only one list in this part
# Would be best to use only modifiedImage from above actually.
for i in range(heightBlocks*widthBlocks): # This "for" bothers me
	treatmentBlock.append(DCT(modifiedImage[i], dctBlock))

treatmentBlockTwo = []
for i in range(heightBlocks*widthBlocks): # This "for" bothers me
	treatmentBlockTwo.append(Quantization(blockSize, factor, treatmentBlock[i]))
	
compressedImage = []
for i in range(heightBlocks*widthBlocks): # This "for" bothers me
	compressedImage.append(IDCT(treatmentBlockTwo[i], dctBlock))

# Return image from blocks
#==========================
compressedImage = np.array(compressedImage)
compressedImage = BlocksToImage(heightBlocks, widthBlocks, compressedImage, blockSize)

#==========================
# Plot()
#==========================
fig, axs = plt.subplots(1, 2)

axs[0].imshow(imagem, cmap='gray', vmin=0, vmax=255)
axs[1].imshow(compressedImage, cmap='gray', vmin=0, vmax=255)

plt.show()
