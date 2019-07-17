from bs4 import BeautifulSoup
import requests
import csv


def harvest(url, csv_file):
    csv_file = open(csv_file + ".csv", "w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ["question_num", "question", "opt_a", "opt_b", "opt_c", "opt_d", "answer"]
    )
    page_num = 1
    page = requests.get(url + "?page=" + str(page_num))
    source = page.text
    none_count = 0
    stop = False

    while stop == False:
        print("PAGE: " + str(page_num))
        soup = BeautifulSoup(source, "lxml")
        questions = soup.select("article.single-question")
        for question in questions:
            if question.find("div", {"class": "question-number"}) == None:
                none_count += 1
                if none_count >= 5:
                    stop = True
                continue
            none_count = 0

            question_num = (
                question.find("div", {"class": "question-number"})
                .getText()
                .replace(". ", "")
            )
            question_main = question.find("div", {"class": "question-main"}).getText()
            options = question.select("p")
            try:
                opt_a = options[0].getText().replace("\n", "").replace("A. ", "")
                opt_b = options[1].getText().replace("\n", "").replace("B. ", "")
                opt_c = options[2].getText().replace("\n", "").replace("C. ", "")
                opt_d = options[3].getText().replace("\n", "").replace("D. ", "")
            except:
                if "opt_c" not in locals() or opt_c == "":
                    opt_c = "Null(this option is empty)"
                if "opt_d" not in locals() or opt_d == "":
                    opt_d = "Null(this option is empty)"

            answer_container = question.find("div", {"class": "answer_container"})
            answer = (
                answer_container.select("strong")[0]
                .get_text()
                .replace("Option", "")
                .strip()
                .lower()
            )

            csv_writer.writerow(
                [question_num, question_main, opt_a, opt_b, opt_c, opt_d, answer]
            )

            opt_c = ""
            opt_d = ""

        print(page.url)
        page_num += 1
        page = requests.get(url + "?page=" + str(page_num))
        source = page.text

    csv_file.close()


url = input("Enter the url from where you want to harvest or leave blank for default ")

if url == "":
    url = "https://duckduckgo.com"

print(url)

name = input("Enter the file name ")

if name == "":
    name == url

csv_file = "../csvs/file_initials" + name

harvest(url, csv_file)
