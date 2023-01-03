# imports
from selenium import webdriver
import pandas as pd
import time
import requests

# start timer
start = time.time()

# ------------------------------------------------ functions ------------------------------------------------ #
def get_links(button):
    '''List comprehension function for error handling'''
    try:
        return button.get_attribute("href")
    except AttributeError:
        pass

# progress bar function, credits to user Greenstick on StackOverflow
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters/13685020
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} [{bar}] {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# ------------------------------------------------ collect links ------------------------------------------------ #

# open website
# replace executable_path to path of chromedriver on your computer
driver = webdriver.Chrome(executable_path='/Users/visheshnarayan/Documents/Autism Research/data/chromedriver')
driver.get("https://zenodo.org/record/5786860#.Y6VB_ezMKhc")

# collect buttons
buttons = driver.find_elements("link text", "Download")

# update user in terminal
print(f"Links retrieved::{len(list(buttons))}")
print("Storing links in Pandas DataFrame")

# storing in dataframe
# df = pd.DataFrame(data={'links': [get_links(button) for button in buttons]})
# df.to_csv("/Users/visheshnarayan/Documents/Autism Research/data/data_links.csv")
print("Created CSV with all download links")

# ------------------------------------------------ download files ------------------------------------------------ #

# opens links file
df = pd.read_csv("data_links.csv")
links = list(df.links)

# number of links
l = len(links)
print(f"Downloading {l} files")

# for link in links, download file
for i, link in enumerate(links):
    filename = link[link.find("files/")+6:link.find("?")]
    response = requests.get(link)
    try:
        with open(filename, "wb") as f:
            f.write(response.content)
    except:
        print("Couldn't download", filename)

    # print progress
    printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50, fill='=')

print("[----------------------- Done -----------------------]")
print("Execution Time::"+str(time.time()-start)+" seconds")
print("Thank you for using my script!\nFor any questions or suggestions for programs, email me: visheshnarayangupta@gmail.com")