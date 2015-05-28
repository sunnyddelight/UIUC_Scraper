#!/usr/bin/python
import cookielib
import mechanize
import getpass
import re
import time
import smtplib
def getWebPage(subj,crse,user,password):
    #initialize mechanize
    br=mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Chrome')]

    #go to login page
    br.open('https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1')
    br.select_form(nr=0)
    br.form['inputEnterpriseId']=user
    br.form['password']=password
    br.submit()

    #go to course search page
    br.open('https://ui2web1.apps.uillinois.edu/BANPROD1/bwskfcls.p_sel_crse_search')
    br.select_form(nr=1)

    #select term
    #need to update this so we can choose terms
    #first digit is always 1, then the year, then the term
    #1 - Spring, 5- Summer, 8-Fall,
    # e.g 120135 is Summer 2013
    br.form['p_term']=['120158']
    br.open(br.form.click()).read()

    #select subject
    forms=br.forms()
    forms.next()
    focus=forms.next()
    focus.set_value([subj], nr=13)
    br.open(focus.click(name='SUB_BTN'))

    #retrieve the html from the "View Sections" Page
    page=''
    for f in br.forms():
        if f.get_value(nr=0)=='120158' and f.get_value(name='SEL_CRSE')==str(crse):
            page=br.open(f.click()).read()
    return page

def parsePage(page):
    #split the table into rows
    section_strings=page.split('<TR>')

    #for every row, match the expression and if there is a match store into sections
    sections=[[elem1[22:-5] for elem1 in re.findall('<TD CLASS=\"dddefault\">(?!<A HREF).*</TD>',elem)] for elem in section_strings]
    #remove any empty lists
    sections=[elem for elem in sections if elem!=[]]
    return sections
def calculateSpots(sections):
    section_dict={}
    for section in sections:
        #check if section is marked closed
        if '<ABBR' not in section[0]:
            if section[2][1] in section_dict:
                section_dict[section[2][1]]+=int(section[10])
            else:
                section_dict[section[2][1]]=int(section[10])
        else:
            #report 0 spots
            if section[3][1] not in section_dict:
                section_dict[section[3][1]]=0
    min_spots=999999
    for key in section_dict:
        if section_dict[key]<min_spots:
            min_spots=section_dict[key]
    return min_spots
# No longer using twilio, using email instead
# def notify(number, course_string):
# # put your own credentials here
#     ACCOUNT_SID = "ACdff1eefaa26353a1fd2bce5c444b5f7b"
#     AUTH_TOKEN = "e38afcca8f3b9a761b8eebee50782827"
#
#     client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
#
#     client.messages.create(
#         to=number,
#         from_="+13312155994",
#         body=course_string,
#     )
def notify(email, course_string):
    #set up email server and send email to user
    smtpObj = smtplib.SMTP_SSL('smtp.gmail.com',465)
    smtpObj.login('uiucscraper@gmail.com','scraperuiuc')
    message = """From: UIUC Scraper
To:
Subject: Class Opening

{0}
""".format(course_string)
    smtpObj.sendmail('uiucscraper@gmail.com', email, message)
    print "Successfully sent email"






#more debugging stuff so we don't have to enter in our user/pass
#output=open('output.txt','w')
#page=getWebPage('CS','173','USERNAME',r'PASSWORD')

#used for testing our scraper so we dont always need to query the page
#output.write(page)
#temp=open('output.txt')
#page=temp.read()
if __name__ == "__main__":
    #get User Inputs
    username=raw_input('Username: ')
    password=getpass.getpass('Password: ')
    course_name=raw_input('Course Subject (Subj): ')
    course_number=raw_input('Course Number (Crse): ')
    email=raw_input('Your Email: ')
    time_interval=raw_input('Time Interval (sec): ')

    #while no spots have opened loop
    while True:
        #retrieve the sections page
        page=getWebPage(course_name,course_number,username,password)

        #parse sections
        sections=parsePage(page)

        #calculate number of open spots
        spots=calculateSpots(sections)
        if spots>0:
            notify(email,'Your course({0} {1}) has an open spot!'.format(course_name,course_number))
            break
        print 'Spots: {0}'.format(spots)
        time.sleep(int(time_interval))
