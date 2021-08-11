import requests
import re
import numpy as np
import imutils
import cv2
from textblob import TextBlob
import pandas as pd
import time
import os

# Title-related functions
def make_en_titles(df: pd.DataFrame) -> list:
    en_titles = []
    for row in range(df.shape[0]):
        if df.iloc[row,:]['alternative_titles']['en'] == '':
            en_titles.append(df.iloc[row,:]['title'])
        else:
            en_titles.append(df.iloc[row,:]['alternative_titles']['en'])
    return en_titles

# Length related anime/manga functions
def get_len_text(text: str) -> int:
    text = re.sub('\W', '', text)
    return len(text)

def get_related_animes(anime_list: list) -> int:
    return len(anime_list)

def get_related_manga(manga_list: list) -> int:
    return len(manga_list)

def get_len_list(manga_list: list) -> int:
    try:
        return len(manga_list)
    except TypeError:
        return np.nan

# Date Functions
def get_start_year(date: str)->int:
    if pd.isnull(date):
        return np.nan
    else:
        return int(date[:4])

def bin_year(year:int) -> str:
    if year < 1980:
        return "< 1980"
    elif year < 1990:
        return "1980-1989"
    elif year < 2000:
        return "1990-1999"
    elif year < 2010:
        return "2000-2009"
    elif year >= 2010:
        return "> 2010"
    else:
        return np.nan

# Functions extracting categorical data from dicts
def get_genre_list(genre_list: list) -> list:
    try: 
        genre_names = []
        for genre in range(len(genre_list)):
            genre_names.append(genre_list[genre]['name'])

        length = len(genre_names)
        if length == 0:
            return np.nan
        else:
            return genre_names
    except TypeError:
        return np.nan

def get_studio_list(studio_list: list) -> list:
    try:
        studio_names = []
        for studio in range(len(studio_list)):
            studio_names.append(studio_list[studio]['name'])

        length = len(studio_names)
        if length == 0:
            return np.nan
        else:
            return studio_names
    except TypeError:
        return np.nan

# Sentiment-gathering functions
def get_polarity(text: str) -> float:
    return TextBlob(text).sentiment.polarity

def get_subjectivity(text: str) -> float:
    return TextBlob(text).sentiment.subjectivity

# Functions for getting picture data
def get_med_pic(pic_dict: dict) -> str:
    if pd.isnull(pic_dict):
        return np.nan
    else:
        return pic_dict['medium']

def get_pic_name(url: str) -> str:
    if pd.isnull(url):
        return np.nan
    else:
        name = re.sub('https://api-cdn.myanimelist.net/images/anime/(\d*/)+', '', url)
        return name

def write_pics(urls: list, directory="datasets/pictures/"):
    for url in urls:
        if pd.isnull(url):
            print("np.NaN error...")
        else:
            name = get_pic_name(url)

            if not os.path.exists(directory + name):
                img_data = requests.get(url).content
                with open(directory + name, 'wb') as f:
                    f.write(img_data)
                    f.close()
                print(f"{name} sucessfully written!")
                time.sleep(1)
            else:
                print(f"{name} exists! Moving to next anime...")

def image_colorfulness(image) -> float:
	# split the image into its respective RGB components
	(B, G, R) = cv2.split(image.astype("float"))

	# compute Red-Green Opponent color space = R - G
	rg = np.absolute(R - G)

	# compute Yellow-Blue Opponent Color Space = 0.5 * (R + G) - B
	yb = np.absolute(0.5 * (R + G) - B)

	# compute the mean and standard deviation of both `rg` and `yb`
	(rbMean, rbStd) = (np.mean(rg), np.std(rg))
	(ybMean, ybStd) = (np.mean(yb), np.std(yb))

	# combine the mean and standard deviations
	stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
	meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))

	# derive the "colorfulness" metric and return it
	return stdRoot + (0.3 * meanRoot)

def get_colorfulness_list(image_list: list, directory="datasets/pictures/") -> list:
    results = []
    # loop over the image paths
    for image_path in image_list:
        if pd.isnull(image_path):
            results.append(np.nan)
            print("np.nan appended...")
        else:
            # load the image, resize it (to speed up computation), and
            # compute the colorfulness metric for the image
            image = cv2.imread(directory + image_path)
            image = imutils.resize(image, width=250)
            C = image_colorfulness(image)

            # add the image and colorfulness metric to the results list
            results.append(C)
            print(f"{image_path} successfully appended!")

    return results

if __name__ == '__main__':
    urls = [
        'https://api-cdn.myanimelist.net/images/anime/13/13738.jpg',
        'https://api-cdn.myanimelist.net/images/anime/1521/94614l.jpg',
        np.nan
    ]
    write_pics(urls, "datasets/pictures/")
    images = list(map(get_pic_name, urls))

    color_scores = get_colorfulness_list(images, "datasets/pictures/")

    print(color_scores)