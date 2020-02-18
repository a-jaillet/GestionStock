
# importing required modules 
import PyPDF2 

f = open('./Hello.txt','w')
# creating a pdf file object 
pdfFileObj = open('unpdf.pdf', 'rb') 
  
# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
  
# printing number of pages in pdf file 
# creating a page object 
for i in range(0,pdfReader.numPages) : 
    pageObj = pdfReader.getPage(i) 
    f.write(pageObj.extractText())
    f.write('\r\n')
f.close()

f = open('./Hello.txt','r')

extracts = []

for page in f.readlines():
    extracts.append(page.split('CLIENT FACTURE',5))

print(extracts)

f.close()
  
# closing the pdf file object 
pdfFileObj.close() 
