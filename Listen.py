#coding:utf-8
import requests
import time
import re
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


##########
__author__ = 'p0desta'
nples = 'http://192.168.100.117/npels/'
##########
def find(name):
	A = []
	B = []
	C = []
	D = []
	ss = open(name+"-A.txt",'r').read()
	section_one = ss.split("Section C")[0]
	section_two = ss.split("Section C")[1]
	answer = re.findall(r'----> ([A-D])',section_one)
	print answer
	T = re.findall(r'----> (.+)',section_two)

	answer_A = re.findall(r'A\).+?\.',section_one)
	answer_B = re.findall(r'B\).+?\.',section_one)
	answer_C = re.findall(r'C\).+?\.',section_one)
	answer_D = re.findall(r'D\).+?\.',section_one)
	for a in answer_A:
		if "B)" not in a:
			A.append(a)

	for b in answer_B:
		if "C)" not in b:
			B.append(b)

	for c in answer_C:
		if "D)" not in c:
			C.append(c)

	for d in answer_D:
		if "and decide which is the best answer" not in d:
			D.append(d)
	End_answer = []
	for i in range(20):
		if answer[i] == "A":
			End_answer.append(A[i][3:])
		elif answer[i] == "B":
			End_answer.append(B[i][3:])
		elif answer[i] == "C":
			End_answer.append(C[i][3:])
		elif answer[i] == "D":
			End_answer.append(D[i][3:])
	return End_answer,T
def find_units(driver):

	IDS = []
	#匹配是否是听说
	tbody = driver.find_elements("css selector","tbody")[1]
	units = []

	trs = tbody.find_elements("css selector","tr")
	for tr in trs[1:-1]:
		ll = len(tr.text)
		if ll<50:
			score = 0
		else:
			score =  int(tr.text.split(" ")[-2])

		if u"听说" in tr.text and (score < 60):
			units.append(tr.text)
			td = tr.find_elements("css selector","td")[4]
			ID = td.find_elements("css selector","span")[0].get_attribute("id")
			IDS.append(ID)
	#ctl00_ContentPlaceHolder1_CourseTestTask1_dgTestTask_ctl19_PAGER > div > ul > li:nth-child(14) > a
	return units,IDS
def reply(driver_new,IDS,units):
	flag = 0
	for ID in IDS:
		driver = driver_new
		#ctl00_ContentPlaceHolder1_CourseTestTask1_dgTestTask_ctl05_Action > span > input[type="button"]
		path = "#"+ID + " > span > input[type=\"button\"]"
		print path
		name = units[flag].split(" ")[0][7:]
		print name
		X = find(name)
		flag += 1
		End_answer = X[0]
		T = X[1]
		print T
		
		above = driver.find_element_by_css_selector(path)
		ActionChains(driver).move_to_element(above).perform()
		driver.find_element_by_css_selector(path).click()
		time.sleep(2)

		qustions = driver.find_elements_by_class_name("test_s_1")
		tmp = 0
		f = 0
		#选择正确选项
		for qustion in qustions:
			if tmp < 20:
				answers =  qustion.find_elements_by_class_name("test_list")
				for answer in answers:
					tmp += 1
					time.sleep(1.5)
					aa =  answer.find_elements("css selector","li")
					for s in aa:
						print s.text[2:]
						if s.text[2:].strip() in End_answer:
							
							id = s.find_elements("css selector","input")[0].get_attribute("id")
							print id
							driver.find_element_by_id(id).click()
			else:
				answers =  qustion.find_elements_by_class_name("test_list_2")[0]
				answer = answers.find_elements("css selector","li")[0]
				Input = answer.find_elements("css selector","input")
				for ID in Input:
					id = ID.get_attribute("id")
					print id
					driver.find_element_by_id(id).send_keys(T[f])
					f +=1
					time.sleep(1)
		time.sleep(4)
		driver.find_element_by_id('btnBottomSubmit').click()
		time.sleep(5)
		driver.switch_to_alert().accept()
		time.sleep(10)	
def listening():

	url = "http://192.168.100.117/NPELS"
	username = raw_input("Please input your username:")
	pwd = raw_input("Please input your password:")
	driver = webdriver.Chrome()
	driver.get(url)

	driver = driver

	time.sleep(2)        
	driver.find_element_by_id("tbName").send_keys(username)
	driver.find_element_by_id("tbPwd").send_keys(pwd)
	driver.find_element_by_id('btnLogin').click()

	time.sleep(2)
	driver.switch_to.frame('mainFrame')

	driver.find_element_by_css_selector("#aspnetForm > div.content > div.main_right > div:nth-child(3) > div > div.class_container > div > ul:nth-child(1) > a > li.class_mag_3_1").click()
	
	time.sleep(2)
	driver.find_element_by_css_selector("#ctl00_liTT > a").click()
	driver_new = driver
	XX = find_units(driver)
	units = XX[0]
	IDS = XX[1]
	reply(driver,IDS,units)
	time.sleep(2)

	#切换到第二页
	driver_new.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CourseTestTask1_dgTestTask_ctl19_PAGER > div > ul > li.gototxt > input[type=\"text\"]").send_keys("2")
	driver_new.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CourseTestTask1_dgTestTask_ctl19_PAGER > div > ul > li.gotobtn > input[type=\"submit\"]").click()
	time.sleep(5)
	YY = find_units(driver_new)
	units = YY[0]
	IDS = YY[1]
	reply(driver_new,IDS,units)
	#ctl00_ContentPlaceHolder1_CourseTestTask1_dgTestTask_ctl03_Action > span > input[type="button"]
	
def main():
	listening()
if __name__ == '__main__':
	main()