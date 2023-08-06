import feedparser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler

def findPackages():
    print("starting up ........")
    d = feedparser.parse("https://pypi.org/rss/packages.xml")
    #
    # with open("newProjects.txt") as myfile:
    #     # myfile.write(projectName + "\n")
    #     for project in myfile:
    #         with open("analysisDone.txt") as donefile:
    #             content = donefile.read()
    #             if project in content:
    #                 print("yep")
    #             else:
    #                 print("needs analysis")


    for entry in d.entries:
        # dPub = entry.published
        title = entry.title
        date = entry.published
        projectName = title.split("added")[0]
        with open("newProjects.txt") as myfile:
            # myfile.write(projectName + "\n")
            content=myfile.read()
            if projectName in content:
                pass
            else:
                with open("newProjects.txt", "a") as myfile:
                    myfile.write(projectName + ", "+ date + "\n")
                print("new addition")
            myfile.close()

    options=Options()
    options.headless=True
    driver = webdriver.Chrome(options=options)
    with open("newProjects.txt") as myfile:
        # myfile.write(projectName + "\n")
        for project in myfile:
            project = project.split(",")[0]
            with open("analysisDone.txt") as donefile:
                content = donefile.read()

                if project in content:
                    #project already analyzed
                    print("already looked at, exiting to next one")
                    continue
                else:
                    linkTest = "https://inspector.pypi.io/project/" + str(project)
                    driver.get("https://inspector.pypi.io/project/" + str(project))
                    print("Starting analysis of " + linkTest)
                    try:
                        link = driver.find_element(By.XPATH,"/html/body/ul/li/a")
                        print("here")
                    except Exception as e:
                        with open("analysisDone.txt", "a") as projectDone:
                            projectDone.write("Error with project: " + project + str(e.args) + "\n")
                        projectDone.close()
                        continue
                    href =link.get_attribute("href")
                    driver.get(href)
                    try:
                        link2 = driver.find_element(By.PARTIAL_LINK_TEXT,"tar.gz")
                        print("getting tar")
                    except Exception as e:
                        try:
                            link2 = driver.find_element(By.PARTIAL_LINK_TEXT,".whl")
                            print("trying wheel instead")
                        except Exception as e:
                            with open("analysisDone.txt", "a") as projectDone:
                                print("still error")
                                projectDone.write("Error with project: " + project + "\n")
                            projectDone.close()
                        with open("analysisDone.txt", "a") as projectDone:
                            print("other error")
                            projectDone.write("Error with project: " + project + "\n")
                        projectDone.close()
                        continue
                    print("now to py")
                    href2 = link2.get_attribute("href")
                    driver.get(href2)
                    if len(driver.find_elements(By.PARTIAL_LINK_TEXT,".py")) > 35:
                        print("too many python files")
                        continue
                    else:
                        print("multiple pythons to look at")
                        link3 = driver.find_elements(By.PARTIAL_LINK_TEXT,".py")
                    list = []
                    for stuff in link3:
                        href3=stuff.get_attribute("href")
                        list.append(href3)
                    print("checking for malware...")
                    malwareKeywords = ["powershell","add.MemoryAccess","billythegoat356/Hyperion","b64decode(","discord.com/api/webhooks","stealer","malware","''.exe'", "Invoke-WebRequest"
                    "import executable","pastebin","paste.","api.apify.org","transfer.sh", "b64encode(","pyarmor", "w.exe",".xyz", "WEBHOOK_URL", "proc.kill()"]
                    for link in list:
                        driver.get(link)
                        try:
                            code = driver.find_element(By.CLASS_NAME,"language-python")
                        except Exception as e:
                            continue
                        if any(x in code.text for x in malwareKeywords):
                            print("True!" + project+ "link:" + link + " has malware")
                            project=project.strip('\n')
                            dir = "//uSERS/ttataryn/Documents/PyPiNetworkTest/src/pypinetworktest_ttataryn26/Malicious/" + str(project) + ".txt"
                            print(dir)
                            try:
                                f = open(dir, "x")
                            except FileExistsError as e:
                                with open(dir, "a") as f:
                                    f.write("Project Name: " + project + "\n" + "Link: " + link + "\n")
                                    f.write(code.text)
                                    continue
                            f.write("Project Name: " + project + "\n" + "Link: " + link + "\n")
                            f.write(code.text)
                            f.close()
                            with open("potentiallyMalicious.txt","a") as malfile:
                                malfile.write(project + "is potentially malicious. Link: " + link +"\n")
                            malfile.close()
                    print("exiting " + project)
                    with open("analysisDone.txt", "a") as projectDone:
                        projectDone.write(project + "\n")
                    projectDone.close()
        # driver.close()
    # driver.get(href3)
    # source = driver.page_source
    # searh_text = "github"
    # print("github" in source)

scheduler= BlockingScheduler()
scheduler.add_job(findPackages,"interval",minutes=10)
print("Press _ to exit")
try:
    scheduler.start()
except (KeyboardInterrupt,SystemExit):
    pass
