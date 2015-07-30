from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import MySQLdb
import BeautifulSoup
#The current settings is for CSE 2nd Sem

db=MySQLdb.connect(host="localhost",user="root",passwd="*****")
cursor=db.cursor()
cursor.execute('CREATE DATABASE Result') #your own database
cursor.execute('use Result')
#add the neccessary subjects you need
cursor.execute("CREATE TABLE Scrape(Rollno VARCHAR(10) ,\
		EP VARCHAR(5) ,\
		Physics VARCHAR(5) ,\
		Maths VARCHAR(5) ,\
		English VARCHAR(5) ,\
		Civil VARCHAR(5) ,\
		NSS VARCHAR(5) ,\
		BranchSpecific VARCHAR(5) ,\
		Mechanical VARCHAR(5) ,\
		Chemistry VARCHAR(5) ,\
		GPA VARCHAR(5))")
browser=webdriver.Firefox()
browser.get('http://www.nitt.edu/prm/nitreg/ShowRes.aspx')
#Give the exact roll no range		
for roll in range(106114001,106114106):
	if(roll==106114052):
		roll=roll+1
	rollno=browser.find_element_by_id("TextBox1")
	rollno.clear()
	rollno.send_keys("%d"%roll)
	browser.find_element_by_name("Button1").click()
	select=Select(browser.find_element_by_name("Dt1"))
	select.select_by_value("115")
	html=browser.page_source

	soup=BeautifulSoup.BeautifulSoup(html)
	table=soup.findAll("table",{"class":"DataGrid"})
	result=table[0].findAll("font")
	gr=[]
	i=6
	#validate loop accordingly(((No of Subjects+1)*6)+1)
	while(i<60):
		gr.append(str(result[i+4].getText()))
		i=i+6
	cgpa=soup.findAll("span",{"id":"LblGPA"})
	cgpa=str(cgpa[0].getText())
	#give your respective fields
	cursor.execute('''INSERT into Scrape (Rollno,EP,Physics,Maths,English,\
			 Civil,NSS,BranchSpecific , Mechanical , Chemistry ,GPA)
			values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
			(roll,gr[0],gr[1],gr[2],gr[3],gr[4],gr[5],gr[6],gr[7],gr[8],cgpa))
	db.commit()

db.close()
browser.close()		
