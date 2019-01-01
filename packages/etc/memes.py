import csv
import random


def get_meme_msg(result):
    with open('./packages/etc/memes.csv', 'r') as csvfile:
        memescsv = list(csv.reader(csvfile))

    lengthofcsv = len(memescsv)
    position = random.randrange(0, lengthofcsv)
    chosen_meme = memescsv[position]
    return str(chosen_meme[0])
