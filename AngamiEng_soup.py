from bs4 import BeautifulSoup
import requests
import time

listA=[]
listE=[]

def scrapeChapter(book, chapter_no):
    chapter_urlsA = [f"https://www.bible.com/bible/338/{book}.{i}.ANBRBSI" for i in range(1,chapter_no)]  #Links can be changed according to need
    chapter_urlsE = [f"https://www.bible.com/bible/12/{book}.{i}.ASV" for i in range(1,chapter_no)]

    ####################Scrap the dialect########################
    for idx, page in enumerate(chapter_urlsA):
        page_to_scrape = requests.get(page)
        soup_A = BeautifulSoup(page_to_scrape.text, 'html.parser')
        verses = soup_A.find_all("span", class_ = "ChapterContent_verse__57FIw")

        for verse in verses:
            passage = verse.find_all("span", class_ = "ChapterContent_content__RrUqA")
            var = [verse_line.get_text(strip=True, separator=' ') for verse_line in passage]

            label = verse.find("span", class_ = "ChapterContent_label__R2PLt")
            
            ########################3
            try:
                int(label.get_text())   #The get_text is important since label is just the tag/html element type
                allow = True
            except:
                allow = False
            #######################3

            if verse.find("span", class_ = "ChapterContent_label__R2PLt") and allow == True:
                line =" ".join(var)
                listA.append(line+"\n")
            else:
                line = line+" ".join(var)
                listA.pop()
                listA.append(line+"\n")


    ######################Scrape the english yeah#########################
    for idx, page in enumerate(chapter_urlsE):
        page_to_scrape = requests.get(page)
        soup_A = BeautifulSoup(page_to_scrape.text, 'html.parser')
        verses = soup_A.find_all("span", class_ = "ChapterContent_verse__57FIw")

        for verse in verses:
            passage = verse.find_all("span", class_ = "ChapterContent_content__RrUqA")
            var = [verse_line.get_text(strip=True, separator=' ') for verse_line in passage]

            label = verse.find("span", class_ = "ChapterContent_label__R2PLt")

            ################################
            try:
                int(label.get_text())
                allow = True
            except:
                allow = False
            ###############################

            if verse.find("span", class_ = "ChapterContent_label__R2PLt") and allow == True:
                line =" ".join(var)
                listE.append(line+"\n")
            else:
                line = line+" ".join(var)
                listE.pop()
                listE.append(line+"\n")


########################################################################
books = ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH", "EST", "JOB"] #can add more books
chapters = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29,36, 10, 13, 10, 42] # Make sure this chapter no. matches the book order 


for idx, book in enumerate(books):
    scrapeChapter(book, chapters[idx])
    time.sleep(180)   #3min wait after scraping a book, u can kiss ur ass in the meantime. Who wants to get into trouble right?


with open("Angami.txt", "w") as f:
    f.writelines(listA)
    f.close()

with open("English.txt", "w") as f:
    f.writelines(listE)
    f.close()

print("Done")