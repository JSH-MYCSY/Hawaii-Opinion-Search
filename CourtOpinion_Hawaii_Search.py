import webbrowser, requests, bs4, io, csv, time, random, os
from pypdf import PdfReader
from datetime import datetime

# this is the setup for the functions below. I have commented out pretty much everything because I do not want to accidentally run any of it again.
# res = requests.get('https://www.courts.state.hi.us/opinions_and_orders/opinions')
# courtOpinions = bs4.BeautifulSoup(res.text, 'html.parser')

# This function below was used to make the initial list of all court opinions and save it to a csv.

# myList = []
# courtNext = courtOpinions.find('a', {'class': 'next page-numbers'})
# counter = 1
# while(courtNext is not None):
#     courtList = courtOpinions.find('tbody', {'class': 'row-hover'})
#     caseName = courtList.find('td', {'class': 'column-4'})
#     opinionUrl = courtList.find('td', {'class': 'column-3'})
#     opinionDate = courtList.find('td', {'class': 'column-1'})
#     courtType = courtList.find('td', {'class': 'column-2'})
#     courtAppealed = courtList.find('td', {'class': 'column-5'})
#     while(caseName is not None):
#         if("ADA" in str(opinionUrl)):
#             opinionUrlText = opinionUrl.find('a', {'title': 'ADA'})['href']
#         elif("href" in str(opinionUrl)):
#             opinionUrlText = opinionUrl.find('a')['href']
#         elif("href" in str(caseName)):
#             opinionUrlText = caseName.find('a')
#             opinionUrlText = opinionUrlText['href']
#         else:
#             opinionUrlText = ""
#         myList.append([caseName.text, opinionUrlText, opinionDate.text, courtType.text, courtAppealed.text])
#         caseName = caseName.find_next('td', {'class': 'column-4'})
#         opinionUrl = opinionUrl.find_next('td', {'class': 'column-3'})
#         opinionDate = opinionDate.find_next('td', {'class': 'column-1'})
#         courtType = courtType.find_next('td', {'class': 'column-2'})
#         courtAppealed = courtAppealed.find_next('td', {'class': 'column-5'})
#     print("finished page: ", counter)
#     time.sleep(1)
#     courtNext = courtOpinions.find('a', {'class': 'next page-numbers'})
#     try:
#         res = requests.get(courtNext['href'])
#         courtOpinions = bs4.BeautifulSoup(res.text, 'html.parser')
#     except:
#         break
#     counter+=1

# myList.reverse()
# with open("CourtOpinion_Hawaii_New.csv", "w", encoding="utf-8", newline="") as csvObj:
#     writer = csv.writer(csvObj)
#     for row in myList:
#         writer.writerow(row)



# The below code should be able to add the opinion text to a txt file.

# with open("CourtOpinion_Hawaii_New.csv","r",encoding='utf-8') as csvObj:
#     reader = csv.reader(csvObj)
#     for number, row in enumerate(reader):
#         if(".pdf" in row[1]):
#             try:
#                 res2 = requests.get(row[1])
#                 io1 = io.BytesIO(res2.content)
#                 myReader = PdfReader(io1)
#                 titleTemp = str(row[1]).split("/")[-1]
#                 title = titleTemp.split(".")[0]
#                 with open("courtOpinionText/" + title + ".txt", "w", encoding="utf-8") as f:
#                     for page in myReader.pages:
#                         f.write(page.extract_text())
#             except:
#                 print("failed on enumerate number: ", number)
#             time.sleep(random.randint(2,3))

#The error list below holds the rows that have links that do not work or I do not have permission to access. These cases are still searchable using the name search, but they won't be searchable using the text search.
#errorList = [726, 1013, 1547, 2081, 2265, 2519, 2809,  2919, 2954, 2957, 2958, 2965, 2972, 3063, 3194, 5997, 6147, 6261, 6265, 6590, 6763, 7220]

# I had created a test csv file with the datetime component, and used the below function to add the datetime information to searchable csv file.

# myList = []
# with open("DateTimeTest.csv", "r", encoding="utf-8") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         myList.append(row)
# f.close()

# with open("CourtOpinion_Hawaii_New.csv", "w", encoding="utf-8", newline="") as file:
#     writer = csv.writer(file)
#     for row in myList:
#         writer.writerow(row)
# file.close()

# this lets me know when the program has completely finished.
print("done.")

# The code below are some of the test versions that I used when first developing this project.


# The below code searches through every link in the site and if it is a valid link, it opens it and reads it, and searches through it to find the keyword. If it finds the keyword, it prints the link out.
# This code takes a long time to run since it goes through every link and every page in those links until the end of the page. I used to have it open the links using webbrowser, but I accidentally inputted a common word and it opened every link in my browser over the course of around five minutes.

# courtA = courtOpinions.find('a', href=True)
# stopgab = 0
# userInput = input("Enter a search term.")
# while(stopgab == 0):
#     if courtA is None:
#         stopgab = 1
#     elif "pdf" in courtA['href'] and "www" in courtA['href']:
#         noDuplicate = 0
#         res2 = requests.get(courtA['href'])
#         io1 = io.BytesIO(res2.content)
#         myReader = PyPDF2.PdfReader(io1)
#         for page in range(len(myReader.pages)):
#             if userInput in str(myReader.pages[page].extract_text()).lower():
#                 print(courtA['href'])
#                 break
#         courtA = courtA.find_next('a', href=True)
#     else:
#         courtA = courtA.find_next('a', href=True)


# the below code was used to initially create the opinion csv file.

# my_list = []
# courtNext = courtOpinions.find('a','next page-numbers')
# with open("CourtOpinion_Hawaii.csv","w",newline='', encoding='utf-8') as csvObj:
#     csvWrite = csv.writer(csvObj)
#     while(courtNext is not None):
#         courtB = courtOpinions.find('tbody', 'row-hover')
#         courtC = courtB.find('td', 'column-4')
#         courtD = courtB.find('td','column-3')
#         courtE = courtD.find('a', attrs={'title': 'ADA'})
#         case_name2 = ""
#         case_url2 = ""
#         while(courtC is not None):
#             str_courtC = str(courtC)
#             case_name1 = str_courtC.split(">")[2]
#             case_name2 = case_name1.split("</p>")[0]
#             if('href' in str(courtE)):
#                 str_courtE = str(courtE)
#                 case_url1 = str_courtE.split('href="')[1]
#                 case_url2 = case_url1.split('" title=')[0]
#             else:
#                 case_url2 = ""
#             my_list.append([case_name2,case_url2])
#             courtC = courtC.find_next('td','column-4')
#             courtD = courtD.find_next('td','column-3')
#             if(courtD is not None):
#                 courtE = courtD.find('a', attrs={'title': 'ADA'})
#         time.sleep(1)
#         courtNext = str(courtNext)
#         urlNext1 = courtNext.split('href="')[1]
#         urlNext2 = urlNext1.split('">')[0]
#         res = requests.get(urlNext2)
#         courtOpinions = bs4.BeautifulSoup(res.text, 'html.parser')
#         courtNext = courtOpinions.find('a','next page-numbers')
#     for row in my_list:
#         csvWrite.writerow(row)

# with open("CourtOpinion_Hawaii.csv","a",newline='', encoding='utf-8') as csvObj:
#     res = requests.get('https://www.courts.state.hi.us/opinions_and_orders/opinions/page/249')
#     courtOpinions = bs4.BeautifulSoup(res.text, 'html.parser')
#     courtB = courtOpinions.find('tbody', 'row-hover')
#     courtC = courtB.find('td', 'column-4')
#     courtD = courtB.find('td','column-3')
#     courtE = courtD.find('a', attrs={'title': 'ADA'})
#     write = csv.writer(csvObj)
#     case_name2 = ""
#     case_url2 = ""
#     while(courtC is not None):
#         str_courtC = str(courtC)
#         case_name1 = str_courtC.split(">")[2]
#         case_name2 = case_name1.split("</p>")[0]
#         if('href' in str(courtE)):
#             str_courtE = str(courtE)
#             case_url1 = str_courtE.split('href="')[1]
#             case_url2 = case_url1.split('" title=')[0]
#         else:
#             case_url2 = ""
#         write.writerow([case_name2,case_url2])
#         courtC = courtC.find_next('td','column-4')
#         courtD = courtD.find_next('td','column-3')
#         if(courtD is not None):
#             courtE = courtD.find('a', attrs={'title': 'ADA'})

# I had a major problem with duplicates that I emailed you about previously, the error at that time was due to the fact that I accidentally had the write to csv function within a while loop.
# This below code was meant to eliminate duplicates from the csv file, but eventually I just remade the csv file.
# no_duplicate_list = []
# with open("CourtOpinion_Hawaii_Update.csv","r",encoding='utf-8') as csvObj:
#     reader = csv.reader(csvObj)
#     for row in reader:
#         if row not in no_duplicate_list:
#             no_duplicate_list.append(row)

# with open("CourtOpinion_Hawaii_fixed.csv","w",encoding='utf-8',newline='') as csvObj:
#     writer = csv.writer(csvObj)
#     for row in no_duplicate_list:
#         writer.writerow(row)

