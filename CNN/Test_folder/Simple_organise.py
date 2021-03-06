# Code to extract and organize images for CNN
# Give it a csv of the data and it'll sort stuff into "normal" and "abnormal" based on diagnosis

# Pandas and Numpy are amazing for data organization
import pandas as pd
import numpy as np
# Tarfile and zipfile for extraction of the compressed files
import tarfile
import zipfile
# Some OS stuff for handling files and folders
import os
import shutil
import ntpath
import subprocess
import random

print "Beginning extraction and organisation process of data"

# Declaring variables
csv_file = "Data_Entry_2017.csv"						# CSV file for how to organise the image data (which categories they belong to)
zipped_files = "archives"								# Where the raw image data is located
category_list = []											# Initializing a list of categories. Will be filled later
subfolder = "images"									# If the images are stored within a subfolder, write name in quotes. Otherwise use None

# This stuff you just have to know
image_name_column = "Image Index"						# Name of column in which "image name" is placed
category_column = "Finding Labels"						# Name of column in which "diagnosis" is placed

# How to organise data
train = 0.8
validation = 0.1

subdirs = ['data', 'data/train', 'data/train/normal', 'data/train/abnormal',
				   'data/validation', 'data/validation/normal', 'data/validation/abnormal',
				   'data/test', 'data/test/normal', 'data/test/abnormal', 'tmp']
# Make data folders
shutil.rmtree('data', ignore_errors=True)
shutil.rmtree('tmp', ignore_errors=True)
for folder in subdirs:
	os.mkdir(folder)

# Load the CSV file into variable "dataframe" so we can organise
dataframe = pd.read_csv(csv_file)

# There are labels that have multiple "diagnoses". Remove all but the first label. 
############# This runs super slow, optimize later
for index, row in dataframe.iterrows():
	if "|" in row[category_column]:
		dataframe.loc[index, category_column] = row[category_column].split('|')[0]






# After extraction, organise data into 
def organise():
	for image in os.listdir('tmp/images'):
		random_num = random.random()

		image_name = str(image)
		row = dataframe.loc[dataframe[image_name_column] == image_name]
		category = str(row.iloc[0][category_column])

		if random_num < train:
			if category == 'No Finding':
				subprocess.call(["mv", "tmp/images/" + image_name, "data/train/normal"])
			else:
				subprocess.call(["mv", "tmp/images/" + image_name, "data/train/abnormal"])
			print "train"

		elif random_num > train and random_num < (train+validation):
			if category == 'No Finding':
				subprocess.call(["mv", "tmp/images/" + image_name, "data/validation/normal"])

			else:
				subprocess.call(["mv", "tmp/images/" + image_name, "data/validation/abnormal"])
			print "validation"

		else:
			if category == 'No Finding':
				subprocess.call(["mv", "tmp/images/" + image_name, "data/test/normal"])

			else:
				subprocess.call(["mv", "tmp/images/" + image_name, "data/test/abnormal"])
			print "test"


# Iterate through all files in your "tar_files" folder 
# Filename is the zipped file, and is extracted to 'tmp' in a folder with its own name
# Works for .tar, .tar.gz, .tgz, .tar.bz2, .tbz files.
def extract():
	for filename in os.listdir(zipped_files):
		print "Extracting " + str(filename)
		# Firstly, load the zipped file into a temporary file... called file.
		if filename.endswith('.tar') or filename.endswith('.tar.gz') or filename.endswith('.tgz') or filename.endswith('.tar.bz2') or filename.endswith('.tbz'):
			tar = tarfile.open(zipped_files + '/' + filename)
			tar.extractall('tmp')
			tar.close()

# Main function run
print "\n========================"
print "Beginning extraction"
extract()
print "\n========================"
print "Beginning organisation"
organise()
print "\n========================"
print "Finished organising, process complete."







