from skimage.metrics import structural_similarity as ssim
from CompressionModule import *
import matplotlib.pyplot as plt

'''
TODO :
	Fix Documentation Examples for PSNR Function
'''
# For better analysis of Matrix data
#np.set_printoptions(precision=2, suppress=True)

#================================
# Main():
#================================
imagem = cv2.imread("7.1.02.tiff", cv2.COLOR_BGR2GRAY)

''' This is a list
5.2.08.tiff --
5.2.09.tiff --
5.2.10.tiff --
7.1.01.tiff --
7.1.02.tiff --
7.1.03.tiff --
'''

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
fig, axs = plt.subplots(1, 2, figsize=(100, 50))
'''
axs[0][0].imshow(imagem, cmap='gray', vmin=0, vmax=255)
axs[0][0].set_title("Original")
'''
'''
axs[0].imshow(imagem, cmap='gray', vmin=0, vmax=255)
axs[0].set_title(f"Compressão Fator {factor}")
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
