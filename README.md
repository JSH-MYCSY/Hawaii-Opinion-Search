<h1>Hawaii Opinion Search Project</h1>
  <div>
    <p>
      This is a project for the <b>Spring 2024 Coding for Lawyers</b> course taught by Professor Stubenberg at the <b>University of Hawaii Richardson School of Law.</b>
    </p>
    <p>
      This project collects case opinion data from the <a href="https://www.courts.state.hi.us/opinions_and_orders/opinions" target="_blank">Judicary's website</a> and stores it into a local database of a csv and txt files in order to be used in a <a href="https://hawaii-opinion-search.streamlit.app/" target="_blank">streamlit app</a> that allows anyone to complete a text search and find cases based on text rather than having to know the month and date as required by the site.
    </p>
    <p>
      This projects demonstrates how even one semester of legal coding could produce work that is beneficial to your resume as well as beneficial to the local community.  This project showcases multiple coding libraries and concepts that were taught in this course, including:
    </p>
    <ul>
      <li>Web Scraping</li>
      <li>CSV Files</li>
      <li>Text Files</li>
      <li>AI</li>
      <li>Streamlit</li>
      <li>Emails</li>
      <li>Functions</li>
      <li>Automation</li>
    </ul>
    <p>
      I will go into a brief overview of how each topic relates to the project, but I encourage you to go to the streamlit app linked above and try it out for yourself.
    </p>
  </div>
<h2>Web Scraping</h2>
  <div>
    <p>
      Outside of coding, the main lesson taught was how to web scrape safely and appropriately.  Always check the websites <a href="https://portal.ehawaii.gov/page/terms-of-use/" target="_blank">Terms of Use</a> and <a href="https://www.courts.state.hi.us/robots.txt" target="_blank">Robots.txt</a> pages to know what is allowed and what is not.  In this project, I had some confusion with the terms of service and the robots.txt file, so I emailed the terms email address and asked for clarification on their policies.  They replied to me that a small educational project should be fine so long as I was not disrupting traffic or overloading their site with requests.  Keeping that in mind, I had a wait time of 2-3 seconds on each request and only scraped between midnight and around 4-5 a.m.  This helped to make sure that the site could keep up with the requests and I was not taking bandwith away from actual people.
    </p>
    <p>
      The actual coding portion of it was fairly simple to implement, it just took a while to complete due to needing to wait between requests.  Below is a snippet of the code used to scrape the site and store information in a txt file.  The code is pretty condensed and easy to grasp, but the important part was the try/except clause in the function.  Since I was scraping multiple urls, I did not want the code to fail and stop randomly if it encountered an unforseen error such as a broken url.  The try/except clause allowed it to just continue with the rest of the urls if it encountered any similar issues.
    </p>
    <pre>
      <code>
    with open("CourtOpinion_Hawaii_New.csv","r",encoding='utf-8') as csvObj:
    reader = csv.reader(csvObj)
    for number, row in enumerate(reader):
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
                print("failed on enumerate number: ", number)
            time.sleep(random.randint(2,3))
      </code>
    </pre>
  </div>
  <h2>CSV Files</h2>
    <div>
      <p>
        In this project, I used CSV files to store data such as the opinion name and date of release.  You can see part of the code used to do this below.
      </p>
      <pre>
        <code>
myList = []
courtNext = courtOpinions.find('a', {'class': 'next page-numbers'})
counter = 1
while(courtNext is not None):
    courtList = courtOpinions.find('tbody', {'class': 'row-hover'})
    caseName = courtList.find('td', {'class': 'column-4'})
    opinionUrl = courtList.find('td', {'class': 'column-3'})
    opinionDate = courtList.find('td', {'class': 'column-1'})
    courtType = courtList.find('td', {'class': 'column-2'})
    courtAppealed = courtList.find('td', {'class': 'column-5'})
    while(caseName is not None):
        if("ADA" in str(opinionUrl)):
            opinionUrlText = opinionUrl.find('a', {'title': 'ADA'})['href']
        elif("href" in str(opinionUrl)):
            opinionUrlText = opinionUrl.find('a')['href']
        elif("href" in str(caseName)):
            opinionUrlText = caseName.find('a')
            opinionUrlText = opinionUrlText['href']
        else:
            opinionUrlText = ""
        myList.append([caseName.text, opinionUrlText, opinionDate.text, courtType.text, courtAppealed.text])
        caseName = caseName.find_next('td', {'class': 'column-4'})
        opinionUrl = opinionUrl.find_next('td', {'class': 'column-3'})
        opinionDate = opinionDate.find_next('td', {'class': 'column-1'})
        courtType = courtType.find_next('td', {'class': 'column-2'})
        courtAppealed = courtAppealed.find_next('td', {'class': 'column-5'})
    print("finished page: ", counter)
    time.sleep(1)
    courtNext = courtOpinions.find('a', {'class': 'next page-numbers'})
        </code>
      </pre>
      <p>
        CSV files are really simple to utilize and are supported by most file viewing programs.  This project uses them to store and retrieve data to be used in the streamlit app for searching, as well as for data manipulation such as changing the dates into date time objects to make the search results sortable.
      </p>
    </div>
  <h2>Text Files</h2>
    <div>
      <p>
        While CSV files are great storage tools, they do have some limitations such as each cell (data value separated by the commas) having a character limit.  Granted, that character limit is over 32,000 characters, but some opinions can get pretty long.  For example, <i>State v. Miller</i>, No. 28849, has over 181,000 characters in its opinion.
      </p>
      <p>
        This is why the project uses txt files in a folder to store the case opinion text.  The process for doing so is similar to the process for the CSV file with the hardest part being coming up with a unique name for each text file.  How I did this was just use part of the url as the txt file, specifially the case number.
      </p>
    </div>
  <h2>AI</h2>
    <div>
      <p>
        A very interesting topic this semester was learning how to integrate artificial intelligence into our coding projects.  In the lesson, this was done through picking out a single sentence in a blurb of text.  I took this similar idea and used it in this project to allow for more refined search results.
      </p>
      <pre>
        <code>
    def ChatGPTSubjectSearch(userInput, opinionExcerpt):
    client = OpenAI(api_key = st.secrets['OPENAI_API_KEY'])
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are being passed a keyword and an excerpt from a court opinion. Determine if the keyword is the subject of the sentence it is used in. If the keyword is the subject, return only True. Otherwise, return only False."},
            {"role": "user", "content": "keyword:" + "\n" + userInput + "\n" + "excerpt:" + "\n" + opinionExcerpt}
        ]
    )
    return(completion.choices[0].message.content)
        </code>
      </pre>
      <p>
        Specifically, this project finds a keyword in the text of the opinion, then feeds a blurb of text surrounding the keyword into chatGPT's API and has it determine whether the keyword is the subject of the sentence it is used in.  If it is the subject, then it returns True to let the search function know the keyword is relevant.  This hopefully filters out results that do not actually address or mention the keyword in a relevant way.
      </p>
    </div>
  <h2>Streamlit</h2>
    <div>
      <p>
        Streamlit is the python-based web-hosting library and application that I used to make the search function available to the public.  Streamlit was demonstrated in class on how we could put applications up for public benefit that are easy to access for individuals.  This is also the main hope behind this project, allowing people easier access to the Judiciary's opinions and orders when researching the law on their own.
      </p>
      <p>
        There are a lot of functions to streamlit that I will not go into as they are mostly visual and display elements, but I will list some features used below:
      </p>
      <ul>
        <li>Config.toml</li>
        <li>set_page_config</li>
        <li>pages folder</li>
        <li>html components</li>
      </ul>
      <p>
        Besides hosting the application, there are two main streamlit features that are worth highlighting for this program: session state and caching.
      </p>
      <pre>
        <code>
    def loadData():
    if('OpinionText' not in st.session_state or 'NameList' not in st.session_state):
        loadList = os.listdir("courtOpinionText/")
        OpinionText = []
        NameList = []
        for item in loadList:
            with open("courtOpinionText/" + item, "r", encoding="utf-8") as txtObj:
                OpinionText.append([str(item).split(".")[0], txtObj.read().lower()])
        with open("CourtOpinion_Hawaii_New.csv", "r", encoding="utf-8") as csvObj:
            reader = csv.reader(csvObj)
            for row in reader:
                NameList.append(row)
        st.session_state['OpinionText'] = OpinionText
        st.session_state['NameList'] = NameList
        </code>
        <code>
    @st.cache_data(ttl="1d", max_entries=10) # caches the last ten search results for one day in order to provide faster results upon searching again.
    def nameSearch(userInput):
        name_list = []
        for row in st.session_state['NameList']:
            if userInput.lower() in str(row[0]).lower():
                name_list.append(row)
        return(name_list)
        </code>
      </pre>
      <p>
        The session state feature allows the browser to load something and store it for the entire time the person is accessing the application.  This allows the program to only need to search through the CSV and txt files once before storing them in a local variable usable on all the pages of the web app.
      </p>
      <p>
        Caching is similar, but allows the actual search results to be saved locally in the browser's cache and cookies so that once someone searches for something, the function does not need to run again to pull up the results.
      </p>
      <p>
        Both of these features really help to optimize the search function on the program and are super easy to implement on the site.
      </p>
    </div>
  <h2>Emails</h2>
    <div>
      <p>
        Unfortunately, the email function is not a public use feature, and was only made for my personal use.  I still wanted to explain its implementation because automatic emails were something addressed in the course.
      </p>
      <pre>
        <code>
    def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Done.")
        </code>
      </pre>
      <p>
        Currently, I have the above snippet of code to send an automatic email from joshua.automated.emails@gmail.com to my hawaii.edu address every Friday morning if there was a case mentioning a keyword I setup in my code.  This works in tandom with the automation feature explained below to work on an automatic timeline without any input from a human.  For anyone that wants to do this on their own, you need to make sure Google OAuth2 is on and setup an app password in your settings, then you will need to confirm in an email that you setup the app password in order to verify it.  The app password lets you login with your python application.  I currently have mine hidden in a GitHub Secret that gets called in GitHub Actions.
      </p>
    </div>
  <h2>Functions</h2>
    <div>
      <p>
        Just briefly, functions are organized clusters of code that get run when you call their name in the code body.  I use functions for organizing code that is meant to complete one function, and to contain code I believe may need to be called or run multiple times.
      </p>
    </div>
  <h2>Automation</h2>
    <div>
      <p>
        Automation is done through GitHub Actions and the .yaml files in the workflows folder.  The format of the yaml files are pretty simple to grasp, with the hardest parts making sure that you are calling the correct versions of everything and running the requirements.txt folder, if you need to.  Even the intimidating cron format is simple using tools such as the <a href="https://crontab.guru/" target="_blank">Cron Guru</a>.
      </p>
      <pre>
        <code>
name: run SendEmail.py

on:
  schedule:
    - cron: '23 10 * * 5' # At 00:00 Friday.
  workflow_dispatch:

env:
  EMAIL_PASSCODE: ${{ secrets.EMAIL_PASSCODE }}  # GitHub Actions secret that is my app password for Google.

jobs:
  build:
    runs-on: ubuntu-latest
    steps:

      - name: checkout repo content
        uses: actions/checkout@v4 # checkout the repository content to github runner.

      - name: setup python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12' # install the python version needed.
          
      - name: execute py script # run main.py.
        run: python SendEmail.py

        </code>
      </pre>
    </div>
