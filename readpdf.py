
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
    extracts.append(page)

#On crée 2 listes pour séparer les factures des avoirs
i=0
j=0
listfactures = []
for page in extracts:
    if 'FACTURECOMMUNAUTE' in page:
        listfactures.append(page)

listavoir = []
for page in extracts:
    if 'AVOIRCOMMUNAUTE' in page:
        listavoir.append(page)


#travail sur les factures :

asupprimer = []
#suppression des factures vides
for i in range (0,len(listfactures)):
    pageparser = listfactures[i].split(" ")
    if pageparser[0] == 'Commande':
        asupprimer.append(i)

for i in range(len(asupprimer)-1,-1,-1):
    del listfactures[asupprimer[i]]

#ici on parse le document pour enlever les parties qui ne nous intéressent pas
asupprimer = []
listfactures2 = []
for page in listfactures:
    listfactures2.append(page.split('CLIENT FACTURE',1)[0])
for i in range(0,len(listfactures)):
    listfactures[i] = listfactures2[i]
listfactures2 = []
for page in listfactures:
    listfactures2.append(page.split('Total Déconsigne',1)[0])
for i in range(0,len(listfactures)):
    listfactures[i] = listfactures2[i]
listfactures2 = []
for page in listfactures:
    if page[0]!='_':
        listfactures2.append([listfactures.index(page),page.split('_',1)[0]])
for i in range(0,len(listfactures2)):
    listfactures[listfactures2[i][0]] = listfactures2[i][1]

#On va encore décomposer pour se faciliter la tache :
#On sépare les articles des consignes

listarticle = []
listconsigne = []


for page in listfactures:
    if page[0]=='_':
        listconsigne.append(page)
    else:
        listarticle.append(page)

listarticleparse = []
for i in range(0,len(listarticle)):
    parse=listarticle[i].split(' ')
    #Pour parser joliment
    while '' in parse:
        del parse[parse.index('')]

    #On enleve les elements à virgules qui servent un peut a rien (aussi ceux des °)
    asupprimer = []
    asup = []
    for j in range (0,len(parse)):
        if ',' in parse[j]:
            asupprimer.append(j)
        if '°' in parse[j]:
            asupprimer.append(j)

    for j in range(0,len(asupprimer)-1):  #On remet la grolsch
        if '19,5L' == parse[asupprimer[j]]:
            asup.append(j)
    for j in range(len(asup)-1,-1,-1):
        del asupprimer[asup[j]]

    for j in range(len(asupprimer)-1,-1,-1):
        del parse[asupprimer[j]]
    del parse[0]
    parse = (' '.join(parse)).split('net')
    if len(parse) >1:
        listarticleparse.append(parse)
#print(listarticleparse)

#On remet en place le nombre de colis et cols
for i in range (0,len(listarticleparse)):
    for j in range(0,len(listarticleparse[i])):
        parse = listarticleparse[i][j].split()
        if len(parse)>0:
            parseder = list(parse[len(parse)-1])
            if(len(parseder)<5):
                der = parseder[0]+' '+''.join(parseder[1:len(parseder)])
            else:
                der = ''.join(parseder[0:2])+' '+''.join(parseder[2:len(parseder)])
            parse[len(parse)-1]=der
        listarticleparse[i][j]=' '.join(parse)

#On enleve toutes les infos inutiles pour avoir ce qu'on veut traiter
listarticle = []
for i in range (0,len(listarticleparse)):
    for j in range(0,len(listarticleparse[i])):
        articleparse = listarticleparse[i][j].split()
        if len(articleparse) > 3:
            del articleparse[len(articleparse)-1]
            del articleparse[len(articleparse)-2]
        article = ' '.join(articleparse)
        if ' FUT ' in article:
            article = article.split(' FUT ',1)
        elif ' VC ' in article:
            article = article.split(' VC ',1)
        elif ' VP ' in article:
            article = article.split(' VP ',1)

        listarticle.append(article)


# for i in range (0,len(listarticle)-1):
#     article= []
#     if len(listarticle[i])>2:
#         articleparse = listarticle[i].split
#         article.append(' '.join(articleparse[0:len(articleparse)-1]))
#         article.append(articleparse[len(articleparse)-1])
#         listarticle[i] = article


# print(listarticleparse[0])
        
# closing the pdf file object 
pdfFileObj.close() 
