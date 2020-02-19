
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

#On trie que les pages qui nous semblent intéressantes
for page in f.readlines():
    extracts.append(page.split('CLIENT FACTURE',1))
    if(len(extracts[i])>1):
        del extracts[i][1]
    else:
        del extracts[i]
        i=i-1

    extracts[i][0]=extracts[i][0].replace('_', '')
    extracts[i][0]=extracts[i][0].replace('|', '')
    i+=1

# Ici, la liste extract contient beaucoup d'éléments,
# Je vais créer une autre liste pour gérer seulement les article

listArticle = extracts
listAsuppr = []
for page in listArticle:
    parser = page[0].split(' ')
    if parser[0] in ['Montant','Commande','chèque','Solde','3TVA']:
        if page not in listAsuppr:
            listAsuppr.append(listArticle.index(page))
    elif 'livraison' in page[0]:
        if page not in listAsuppr:
            listAsuppr.append(listArticle.index(page))
    elif 'RECLAMATION' in page[0]:
        if page not in listAsuppr:
            listAsuppr.append(listArticle.index(page))        

for index in range(0,len(listAsuppr)):
    del listArticle[listAsuppr[index]]
    for index2 in range(0,len(listAsuppr)):
        listAsuppr[index2] = listAsuppr[index2]-1

print(len(listArticle))
for page in listArticle:
    print(page)
    print('\r\n')

f.close()
  
# closing the pdf file object 
pdfFileObj.close() 
