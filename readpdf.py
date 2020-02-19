
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
i=0

for page in f.readlines():
    extracts.append(page.split('CLIENT FACTURE',1))
    if(len(extracts[i])>1):
        del extracts[i][1]
    else:
        del extracts[i]
        i=i-1
    i+=1
    

for page in extracts:
    print(page)
    print('\r\n')

f.close()
  
# closing the pdf file object 
pdfFileObj.close() 
