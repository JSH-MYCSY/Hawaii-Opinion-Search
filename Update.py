import csv, requests, io, bs4, time, random
from pypdf import PdfReader
from datetime import datetime

# This should be automatically updated from main.yml

variableTest = [] # creates this variable outside of the for loop so that it is able to be called later.
with open("CourtOpinion_Hawaii_New.csv","r",encoding='utf-8') as csvObj:
    reader = csv.reader(csvObj)
    for row in reader:
        variableTest = row[0]  # This iterates over the csv file and just saves over the variableTest variable until it reaches the end of the list.
with open("CourtOpinion_Hawaii_New.csv","a",newline='', encoding='utf-8') as csvObj:
    res = requests.get('https://www.courts.state.hi.us/opinions_and_orders/opinions/')  # gets the opinions site.
    courtOpinions = bs4.BeautifulSoup(res.text, 'html.parser')  # parses the html on the site.
    courtList = courtOpinions.find('tbody', {'class': 'row-hover'})  # finds the table body that houses all the opinion information.
    caseName = courtList.find('td', {'class': 'column-4'})  # this and the subsequent .find('td) functions get the individual opinion information from the table.
    opinionUrl = courtList.find('td',{'class': 'column-3'})
    opinionDate = courtList.find('td', {'class': 'column-1'})
    courtType = courtList.find('td', {'class': 'column-2'})
    courtAppealed = courtList.find('td', {'class': 'column-5'})
    write = csv.writer(csvObj)
    while_loop_boolean = 0
    tempList = []
    while(while_loop_boolean == 0): # while loop to loop through all the opinions.
        if(variableTest not in caseName.text):  # this checks to see if the last opinion saved in the csv file has the same name as the opinion that is going to be saved, and if it does, it stops the while loop.
            case_name = caseName.text
            if('ADA' in str(opinionUrl)):  # gets specifically the ADA pdf of the opinion because that has the readable text for screen readers.
                opinionUrlText = opinionUrl.find('a', {'title': 'ADA'})['href']
            else:
                opinionUrlText = ""
            tempList.append([case_name,opinionUrlText, datetime.strptime(opinionDate.text, "%B %d, %Y"), courtType.text, courtAppealed.text])  # appends the opinion information into a temporary list to be saved later. Uses the datetime library to save the date string as a sortable datetime variable.
            caseName = caseName.find_next('td', {'class': 'column-4'})  # this and subsequent .find_next('td) continue to go through the opinion table until the 
            opinionUrl = opinionUrl.find_next('td', {'class': 'column-3'})
            opinionDate = opinionDate.find_next('td', {'class': 'column-1'})
            courtType = courtType.find_next('td', {'class': 'column-2'})
            courtAppealed = courtAppealed.find_next('td', {'class': 'column-5'})
        else:
            while_loop_boolean = 1
    tempList.reverse()  # this reverses the opinion list because I want the most recent opinion to be on the bottom of the list to be pulled in the next run of this function.
    for row in tempList:  # writes the list to the csv file.
        write.writerow(row)
    for row in tempList:  # reads the opinion pdf and saves the txt as a txt file in the courtOpinionText folder.
        if(".pdf" in row[1]):
            try:  # catch exception so that the entire program does not fail if there is one bad egg in the list.
                res2 = requests.get(row[1])
                io1 = io.BytesIO(res2.content)
                myReader = PdfReader(io1)
                titleTemp = str(row[1]).split("/")[-1]
                title = titleTemp.split(".")[0]
                with open("courtOpinionText/" + title + ".txt", "w", encoding="utf-8") as f:
                    for page in myReader.pages:
                        f.write(page.extract_text())
            except:
                print("failed")
            time.sleep(random.randint(2,3))  # set time to randomly sleep between 2/3 seconds so as to not overload the page with requests.