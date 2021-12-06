# import the necessary packages
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import glob
import os

def load_house_characteristics(inputPath):
    cols = ["bedrooms", "bathrooms", "area", "zipcode", "price"]
    df = pd.read_csv(inputPath, sep=" ", header=0, names=cols)

        #delete
    zipcodes = df["zipcode"].value_counts().keys().tolist()
    counts = df["zipcode"].value_counts().tolist()
	# loop over each of the unique zip codes and their corresponding
	# count
    for (zipcode, count) in zip(zipcodes, counts):
		# the zip code counts for our housing dataset is *extremely*
		# unbalanced (some only having 1 or 2 houses per zip code)
		# so let's sanitize our data by removing any houses with less
		# than 25 houses per zip code
          if count < 25:
              idxs = df[df["zipcode"] == zipcode].index
              df.drop(idxs, inplace=True)

    return df

def load_house_images(df, inputpath):
  #initializes images array
  images = []

  for i in df.index.values:
     basePath = os.path.sep.join([inputPath, "{}_*".format(i + 1)])
     housePaths = sorted(list(glob.glob(basePath)))

  inputImages =[]
  outputImage = np.zeros((


def process_house(df,train, test):
  #initializes the colum names
  attributes = ["bedrooms", "bathrooms", "area"]
  
  #performs min-max scaling to each feature in the range of [0,1]
  cs = MinMaxScaler()
  trainAttributes = cs.fit_transform(train[attributes])
  testAttributes = cs.transform(test[attributes])

  #One hot encode any categorical data ## delete
  zipBinarizer = LabelBinarizer().fit(df["zipcode"])
  trainCategorical = zipBinarizer.transform(train["zipcode"])
  testCategorical = zipBinarizer.transform(test["zipcode"])

  trainX = np.hstack([trainCategorical, trainAttributes])
  testX = np.hstack([testCategorical, testAttributes])

  #return training and testing data 
  return (trainX, testX)
