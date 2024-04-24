import csv, requests, io, bs4, time, random
from pypdf import PdfReader

# This should be automatically updated from main.yml

variableTest = []
with open("CourtOpinion_Hawaii_New.csv","r",encoding='utf-8') as csvObj:
    reader = csv.reader(csvObj)
    for row in reader:
        variableTest = row[0]
with open("CourtOpinion_Hawaii_New.csv","a",newline='', encoding='utf-8') as csvObj:
    res = requests.get('https://www.courts.state.hi.us/opinions_and_orders/opinions/')
    courtOpinions = bs4.BeautifulSoup(res.text, 'html.parser')
    courtList = courtOpinions.find('tbody', {'class': 'row-hover'})
    caseName = courtList.find('td', {'class': 'column-4'})
    opinionUrl = courtList.find('td',{'class': 'column-3'})
    opinionDate = courtList.find('td', {'class': 'column-1'})
    courtType = courtList.find('td', {'class': 'column-2'})
    courtAppealed = courtList.find('td', {'class': 'column-5'})
    write = csv.writer(csvObj)
    while_loop_boolean = 0
    tempList = []
    while(while_loop_boolean == 0):
        if(variableTest not in caseName.text):
            case_name = caseName.text
            if('ADA' in str(opinionUrl)):
                opinionUrlText = opinionUrl.find('a', {'title': 'ADA'})['href']
            else:
                opinionUrlText = ""
            tempList.append([case_name,opinionUrlText, opinionDate.text, courtType.text, courtAppealed.text])
            caseName = caseName.find_next('td', {'class': 'column-4'})
            opinionUrl = opinionUrl.find_next('td', {'class': 'column-3'})
            opinionDate = opinionDate.find_next('td', {'class': 'column-1'})
            courtType = courtType.find_next('td', {'class': 'column-2'})
            courtAppealed = courtAppealed.find_next('td', {'class': 'column-5'})
        else:
            while_loop_boolean = 1
    tempList.reverse()
    for row in tempList:
        write.writerow(row)
    for row in tempList:
        if(".pdf" in row[1]):
            try:
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
            time.sleep(random.randint(2,3))