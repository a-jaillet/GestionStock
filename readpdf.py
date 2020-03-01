
# importing required modules 
import PyPDF2 
from tkinter import * 
from tkinter.messagebox import *
from tkinter.filedialog import *

def calculPdf(n):
    f = open('./Hello.txt','w')
    for i in range(0,n):
        #On ouvre les pdfs que l'on veut en interface graphique
        pdf = askopenfilename(title="Ouvrir votre document",filetypes=[('all files','.*')])
        pdfFileObj = open(pdf, 'rb') 
        
        # creating a pdf reader object 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

        # printing number of pages in pdf file 
        # creating a page object 
        for i in range(0,pdfReader.numPages) : 
            pageObj = pdfReader.getPage(i) 
            f.write(pageObj.extractText())
            f.write('\r\n')
        pdfFileObj.close() 
    f.close()

    f = open('./Hello.txt','r')

    extracts = []
    i=0

    for page in f.readlines():
        extracts.append(page)
    f.close()
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

    for i in range(0,len(listarticle)):
        listarticle[i] = listarticle[i].replace('19,5L','20L')

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

        for j in range(len(asupprimer)-1,-1,-1):
            del parse[asupprimer[j]]
        del parse[0]
        parse = (' '.join(parse)).split('net')
        if len(parse) >1:
            listarticleparse.append(parse)

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

    #On vire les palettes et les administratif
    asupprimer = []
    article = []
    for i in range (0,len(listarticle)):
        if len(listarticle[i])==0:
            asupprimer.append(i)
        if len(listarticle[i])>2:
            parse = listarticle[i].split()
            if parse[0]=='PALETTE':
                asupprimer.append(i)
            if parse[0]=='ad':
                asupprimer.append(i)
            if parse[0]=='administratifs':
                asupprimer.append(i)
            if parse[0]=='REPRISE':
                asupprimer.append(i)
            if parse[0]=='CAFE':
                asupprimer.append(i)
            if parse[0]=='CHOCOLAT':
                asupprimer.append(i)
            #dead la mise en forme
            article.append(' '.join(parse[0:len(parse)-1]))
            article.append(parse[len(parse)-1])
            listarticle[i]=article
            article = []

    for i in range(len(asupprimer)-1,-1,-1):
        del listarticle[asupprimer[i]]


    #On veut voir les remisé séparément mais ils seront toujours pris en compte dans le calcul total
    # !!!! On ne gere pas les remises à plus de 10 fûts !!!!
    listarticleremise = []
    for article in listarticle:
        if len(article[1])>3:
            parse = article[1].split()
            listarticleremise.append(article)
            article[1] = parse[1][0]

    listarticlesomme = []
    nomarticle = []
    for article in listarticle:
        parse = []
        parse.append(article[0])
        parse.append(int(article[1]))
        if parse[0] in nomarticle:
            for article2 in listarticlesomme:
                if article2[0]==parse[0]:
                    article2[1]=article2[1]+parse[1]
        else:
            nomarticle.append(parse[0])
            listarticlesomme.append(parse)
    return listarticlesomme



#Gérer plusieurs pdfs
fenetre = Tk()
label = Label(fenetre, text="Bienvenue sur l'outil d'aide à la gestion de stock.\n Cet outil te servira à rentrer tes factures beaucoup plus rapidement sur ton tableur. \n Merci de rentrer le nombre de facture à traiter ci-dessous")
label.pack()

print('Indiquez le nombre de pdf à parser')
n=input()

listarticles = calculPdf(int(n))
for i in listarticles:
    print(i)