'''
install below libraries
	matplotlib
	fpdf
	numpy
	pandas
	'''
from matplotlib import pyplot as plt
from fpdf import FPDF 
pdf = FPDF()
import numpy as np
import pandas
from collections import Counter
epw = pdf.w - 2*pdf.l_margin
th = 10

col_width = epw/4

import pandas as pd 
data=pd.read_csv('complete.csv')
keys=data.keys()

line=10

def pdf_(text,c=0):

	global line,pdf

	if(c==1):
		pdf.cell(200, 10, txt = text,ln = 1, align = 'C') 
	else:
		pdf.cell(200, 10, txt = text,ln = 1, align = 'L') 

for subject in keys[2::3]:
	pdf.add_page() 

	final_df = data.sort_values(by=[subject], ascending=False)
	count=1;
	last=100
	fail_in_current_subject=0
	top_5=[]
	mark_=[]
	grade_=[]
	cp_=[]
	for ind in final_df.index:
		marks=float(final_df[subject][ind])
		mark_.append(marks)
		grade_.append(final_df[subject.replace("MARKS","GRADES")][ind])
		cp_.append(final_df[subject.replace("MARKS","CP")][ind])
		if(count<6):
			top_5.append([final_df['Seat_number'][ind], final_df['Name of The Student'][ind],final_df[subject][ind]])
		if(marks<last):
			count+=1
			last=marks
		if(final_df[subject.replace("MARKS","")+"GRADES"][ind]=="F"):
			fail_in_current_subject+=1
			
			
	fig,ax = plt.subplots(1,1)
	a = np.array(mark_)
	min_=min(mark_)
	max_=max(mark_)
	bins_=[]
	bins_.append(min_)
	bins_.append(int((((min_+max_)/2)+min_)/2))
	bins_.append(int((min_+max_)/2))
	bins_.append(int((((min_+max_)/2)+max_)/2))
	bins_.append(max_)
	ax.hist(a, bins = bins_,color = 'g')
	ax.set_title("histogram of result for subject"+subject.replace("MARKS",""))
	ax.set_xticks(bins_)
	ax.set_xlabel('marks')
	ax.set_ylabel('no. of students')

	plt.savefig("graphs/"+subject+"marks.png")
	
	fig,ax = plt.subplots(1,1)
	letter_counts = Counter(grade_)


	
	ax.bar(letter_counts.keys(),letter_counts.values(),width = 1.0)
	ax.set_title("bar chart of grades for subject "+subject.replace("MARKS",""))

	ax.set_xlabel('grades')
	ax.set_ylabel('no. of students')

	plt.savefig("graphs/"+subject+"grades.png")


	fig,ax = plt.subplots(1,1)
	a = np.array(cp_)
	min_=min(cp_)
	max_=max(cp_)
	bins_=[]
	bins_.append(min_)
	bins_.append(int((((min_+max_)/2)+min_)/2))
	bins_.append(int((min_+max_)/2))
	bins_.append(int((((min_+max_)/2)+max_)/2))
	bins_.append(max_)
	ax.hist(a, bins = bins_,color = 'b')
	ax.set_title("histogram of CP for "+subject.replace("MARKS",""))
	ax.set_xticks(bins_)
	ax.set_xlabel('CP')
	ax.set_ylabel('no. of students')

	plt.savefig("graphs/"+subject+"cp.png")	
	

	top=top_5[0][-1]
	count=0
	top_1=[]
	for i in top_5:
		if(i[-1]==top):
			top_1.append(i)
	if(len(top_1)>5):
		top_5=top_1
	else:
		while(len(top_5)>5):
			remove=top_5[-1][-1]
			for i in range(len(top_5)):
				if(top_5[-1][-1]==remove):
					top_5.pop();
	pdf.set_font("Arial", size = 30) 
	pdf.set_text_color(220, 50, 50)
	pdf.ln(5)

	pdf_(subject.replace("_MARKS",""),1)
	pdf.set_text_color(0,0,10)
	pdf.ln(10)
	pdf.set_font("Arial", size = 18)
	pdf_("top "+str(len(top_5))+"  students")
	pdf.ln(3)
	pdf.set_font("Arial", size = 13)
	pdf.set_text_color(0,0,0)

	pdf.cell(30, th, "Seat number", border=1)
	pdf.cell(110, th, "Name of The Student", border=1)
	pdf.cell(20, th, "Marks", border=1)
	pdf.ln(10)
	for row in top_5:

		pdf.cell(30, th, row[0], border=1)
		pdf.cell(110, th, row[1], border=1)
		pdf.cell(20, th, str(row[2]), border=1)
		pdf.ln(10)

	pdf.set_text_color(255,0,0)


	pdf_("")
	pdf_("Total Fail = "+str(fail_in_current_subject))


	pdf.set_text_color(0,128,0)
	pdf_("Total PASS = "+str(len(final_df['Seat_number'])-fail_in_current_subject))


	pdf_("Pass Students ="	+str(round((100/len(final_df['Seat_number']))*(len(final_df['Seat_number'])-fail_in_current_subject),2))+" %");
	
	pdf.add_page() 
	pdf.image("graphs/"+subject+"marks.png", x = 0, y = 0, w = 200, h = 100, type = '', link = '')
	pdf.image("graphs/"+subject+"grades.png", x = 0, y = 100, w = 200, h = 100, type = '', link = '')
	pdf.image("graphs/"+subject+"cp.png", x = 0, y = 200, w = 200, h = 98, type = '', link = '')
pdf.output("anylysis.pdf")    