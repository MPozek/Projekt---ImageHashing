from PIL import Image
import imagehash
import sys
import os
from os.path import basename


def print_results(TP, FP, FN, lista, lista_hash_fileova, ostali, broj_usporedenih):
	print("NUMBER OF COMPARES:%d\n" % broj_usporedenih)	
	print("NUMBER OF ORGINALS:%d\tNUMBER OF FAKES:%d\n" % (len(lista_hash_fileova), len(lista)))
	print("A-HASH:\tTP=%d\tFP=%d\tFN=%d" % (TP[0], FP[0], FN[0]))
	print("precision=%f\nrecall=%f\n" % ((TP[0]/(TP[0] + FP[0])),(TP[0]/(TP[0] + FN[0]))))
	print("P-HASH:\tTP=%d\tFP=%d\tFN=%d" % (TP[1], FP[1], FN[1]))
	print("precision=%f\nrecall=%f\n" % ((TP[1]/(TP[1] + FP[1])),(TP[1]/(TP[1] + FN[1]))))
	print("D-HASH:\tTP=%d\tFP=%d\tFN=%d" % (TP[2], FP[2], FN[2]))
	print("precision=%f\nrecall=%f\n" % ((TP[2]/(TP[2] + FP[2])),(TP[2]/(TP[2] + FN[2]))))
	print("W-HASH:\tTP=%d\tFP=%d\tFN=%d" % (TP[3], FP[3], FN[3]))
	print("precision=%f\nrecall=%f\n" % ((TP[3]/(TP[3] + FP[3])),(TP[3]/(TP[3] + FN[3]))))
	print("")	
	print("Others => A-HASH:%d P-HASH:%d D-HASH:%d W-HASH:%d\n" % (ostali[0], ostali[1], ostali[2], ostali[3]))

def check_picture(reader, hash_from_file, picture, string, TP, FP, FN, index, N, ostali):
	read_hash = imagehash.hex_to_hash(reader.readline().strip())
	if((read_hash-hash_from_file) <= N):
		if(string == picture.split("_")[0]):
			TP[index] += 1
		if(string != picture.split("_")[0]):
			FP[index] += 1
	elif((read_hash-hash_from_file) > N and string == picture.split("_")[0]):
		FN[index] += 1
	else:
		ostali[index] += 1

def folder_and_hash_file(help_folder, input_dir):
	if not os.path.exists(help_folder):
   		os.makedirs(help_folder)

	list = 	os.listdir(help_folder)
	for file in list:
		os.remove(help_folder+file)
	
	list = os.listdir(input_dir)

	for picture in list:
		tekst_file = help_folder+os.path.splitext(picture)[0]+"_hash.txt"
		try:
			os.mknod(tekst_file)
		except Exception:
			print("", end="")
		writer = open(tekst_file, "w")
		image = Image.open(input_dir+picture)

		hash = imagehash.average_hash(image)
		writer.write(str(hash)+"\n")

		hash = imagehash.phash(image)
		writer.write(str(hash)+"\n")

		hash = imagehash.dhash(image)
		writer.write(str(hash)+"\n")

		hash = imagehash.whash(image)
		writer.write(str(hash)+"\n")

		writer.close()

def evaluate_hashing_algoritms(input_dir, output_dir, N):
	help_folder = "help_folder/"
	folder_and_hash_file(help_folder, input_dir)
	
	# true positive apdw
	TP = [0,0,0,0]
	# false positive apdw
	FP = [0,0,0,0]
	# false negative apdw
	FN = [0,0,0,0]
	# other comparings
	ostali = [0,0,0,0]
	list = os.listdir(output_dir)
	hash_files = os.listdir(help_folder)	

	broj_usporedenih = 0

	for picture in list:
		image = Image.open(output_dir+picture)	
		ahash = imagehash.average_hash(image)
		phash = imagehash.phash(image)
		dhash = imagehash.dhash(image)
		try:
			whash = imagehash.whash(image)
		except Exception:
			continue

		broj_usporedenih += 1
		for hash_file in hash_files:
			reader = open(help_folder+hash_file, "r+")
			string = str(os.path.splitext(hash_file)[0]).split("_")[0]
			check_picture(reader, ahash, picture, string, TP, FP, FN, 0, N, ostali)
			check_picture(reader, phash, picture, string, TP, FP, FN, 1, N, ostali)
			check_picture(reader, dhash, picture, string, TP, FP, FN, 2, N, ostali)
			check_picture(reader, whash, picture, string, TP, FP, FN, 3, N, ostali)
			reader.close()

	print_results(TP, FP, FN, list, hash_files, ostali, broj_usporedenih)
	
if(len(sys.argv) != 4):
	print("Example: python3 program.py <folder_with_orginals> <folder_with_fakes> <tracehold>")
	exit(0)

folder_original = sys.argv[1] + "/"
folder_kopije = sys.argv[2] + "/"
tracehold = sys.argv[3]
evaluate_hashing_algoritms(folder_original, folder_kopije, int(tracehold))
