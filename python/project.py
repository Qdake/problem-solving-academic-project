# -*- coding: utf-8 -*-
"""
RP-PROJECT
"""

import itertools
import numpy as np
import time
import random
import copy
class Photo:
    def __init__(self,orientation,mots,num):
        self.orientation = orientation;
        self.mots = mots; 
        self.num = num;
def read(f,p):
    '''input: f le chemin de ficher entree (chaine de caracteres)
              p pourcentage de lignes
       sortie: photos  l'ensemble des photos (liste d'objects)
               photosV l'ensemble des photos verticaux (liste d'objects)
               photosH l'ensemble des photos horizontaux (liste d'ojects)
    '''
    file = open(f,'r')
    n = int(file.readline());
    photos = []
    photosV = []
    photosH = []
    for i in range(int(np.floor(n*p))):
        line = file.readline()
        line = line.replace("\n", "")
        line = line.split(' ')
        photo = Photo(line[0],set(line[2:]),i);
        photos.append(photo)
        if photo.orientation == 'H':
            photosH.append(photo)
        if photo.orientation == 'V':
            photosV.append(photo)
            
    file.close()
    return photos, photosH, photosV

def simple_presentation(photos,photosH,photosV):
    presentation = []
    for photo in photosH:
        presentation.append([photo.num])
    for i in range(len(photosV)//2):
        presentation.append([photosV[2*i].num,photosV[2*i+1].num])
    return presentation

def write(presentation):
    f = open('resultat.txt','w')
    f.writelines([str(len(presentation)),'\n'])
    for photo in presentation:
        if len(photo) == 1:
            f.writelines([str(photo[0]),'\n'])
        if len(photo) == 2:
            f.writelines([str(photo[0]),' ',str(photo[1]),'\n'])
    f.close()
    return




def score_trans(slide1,slide2):
    '''
    compares sets of words
    tag1, tag2 = sets
    '''
    assert slide1 != None, "Dans fonction score_trans, slide1 == None" 
    assert slide2 != None, "Dans fonction score_trans, slide2 == None"
    tag1 = getMots(slide1);
    tag2 = getMots(slide2);
    k1 = len(tag1.intersection(tag2))
    k2 = len(tag1.difference(tag2))
    k3 = len(tag2.difference(tag1))
    return min(k1,k2,k3)

def getMots(slide):
    '''input: slide (liste de numero des photos contenus)
       output: l'ensemble des mots des photos contenus dans la slide'''
    assert slide != None, "fonction getMots prend un slide qui n'est pas None comme argument"
    if len(slide) == 1 :
        return photos[slide[0]].mots;
    else:
        return photos[slide[0]].mots.union(photos[slide[1]].mots);

def evaluate(presentation):
    ''' input:   photos:l'ensemble des photos (liste d'objects)
                 presentation: l'ensemble des slide (liste de slides)
        output:  score de la presentation
    '''
    score = 0
    for i in range(len(presentation)-1):
        score += score_trans( presentation[i], presentation[i+1]);
    return score

def durationExecution(t):
    return time.time()-t;

def slideMaximisantTransition(photos_num,photosV_num,slide):
    slide2 = None;
    photoChoisie_num = choisirPhotoMaximisantTransition(photos_num,slide,[])
    if photoChoisie_num != None:
        slide2 = [photoChoisie_num];
#        print("slide2 :")
#        slide2.afficher();
        if photos[photoChoisie_num].orientation == "V":
            photosV_num.remove(photoChoisie_num);
            photoChoisie2_num = choisirPhotoMaximisantTransition(photosV_num,slide,slide2);
            if photoChoisie2_num != None:
                slide2.append(photoChoisie2_num);
    return slide2;            

def choisirPhotoMaximisantTransition(photos_num,slide,slideACompleter):
    '''input: photos_num  l'ensemble de numero des photos 
               slide       
               slideACompleter
       output: num du photo qui maximise le score de la transition etre slide et slideACompleter''' 
    scoreMaximum = -1;
    photoChoisie_num = None;
    for num in photos_num: 
        slideACompleter.append(num);
        score = score_trans(slide,slideACompleter);
        if  score > scoreMaximum:
            photoChoisie_num = num;
            scoreMaximum = score;
        slideACompleter.remove(num)
    return photoChoisie_num;
                    

############### Exercice 3  methode gloutonne ##############
def gloutonSimple(photos_num,photosV_num,photosH_num,T=60):
    # 1) initialization
    startTime = time.time();      # temps du debut de l'execution
    presentation = [];                    
    # 2) generer la premiere vignette
    photoChoisie_num = random.choice(photos_num);     # choix par hasard d'une photo
    if photos[photoChoisie_num].orientation == "V":      # si la premiere photo choisie est d'orientation V,
        photoChoisie2_num = random.choice(photosV_num);
        while photoChoisie2_num == photoChoisie_num:
            photoChoisie2_num = random.choice(photosV_num);
        slide = [photoChoisie_num,photoChoisie2_num]
    else:
        slide = [photoChoisie_num]

    # 3) tant que le temps de l'execution ne depasse pas T et que l'on peut trouver une
    # vignette de de transition non nulle, faire
    while slide != None and durationExecution(startTime) < T:
        presentation.append(slide);                        #ajouter la vignette a la fin de presentation
#        print("presentation: ");
#        presentation.afficher();
        for num in slide:
            photos_num.remove(num);
            if photos[num].orientation == "V":
                assert num in photosV_num, "photo {} is not in photosV_num".format(num)
                photosV_num.remove(num);
            else:
                photosH_num.remove(num);
#        print("photos used: ",photosUsed);
        slide = slideMaximisantTransition(photos_num,photosV_num.copy(),presentation[-1]);     # trouver la prochaine vignette qui maximisant la transition
#        print("slide :");
#        slide.afficher();
    return presentation;
 

def gloutonAlea(photos_num,photosV_num,photosH_num,patience):
    # 1) initialization
    presentation = [];                    
    # 2) generer la premiere vignette
    photoChoisie_num = random.choice(photos_num);     # choix par hasard d'une photo
    if photos[photoChoisie_num].orientation == "V":      # si la premiere photo choisie est d'orientation V,
        photoChoisie2_num = random.choice(photosV_num);
        while photoChoisie2_num == photoChoisie_num:
            photoChoisie2_num = random.choice(photosV_num);
        slide = [photoChoisie_num,photoChoisie2_num]
    else:
        slide = [photoChoisie_num]

    # 3) tant que le temps de l'execution ne depasse pas T et que l'on peut trouver une
    # vignette de de transition non nulle, faire
    while slide != None:
        presentation.append(slide);                        #ajouter la vignette a la fin de presentation
#        print("presentation: ");
#        presentation.afficher();
        for num in slide:
            photos_num.remove(num);
            if photos[num].orientation == "V":
                assert num in photosV_num, "photo {} is not in photosV_num".format(num)
                photosV_num.remove(num);
            else:
                photosH_num.remove(num);
#        print("photos used: ",photosUsed);
        slide = slideMaximisantTransitionAlea(photos_num,photosV_num.copy(),presentation[-1],patience);     # trouver la prochaine vignette qui maximisant la transition
#        print("slide :");
#        slide.afficher();
    return presentation;

def slideMaximisantTransitionAlea(photos_num,photosV_num,slide,patience):
    slide2 = None;
    photoChoisie_num = choisirPhotoMaximisantTransitionAlea(photos_num,slide,[],patience)
    if photoChoisie_num != None:
        slide2 = [photoChoisie_num];
#        print("slide2 :")
#        slide2.afficher();
        if photos[photoChoisie_num].orientation == "V":
            photosV_num.remove(photoChoisie_num);
            photoChoisie2_num = choisirPhotoMaximisantTransitionAlea(photosV_num,slide,slide2,patience);
            if photoChoisie2_num != None:
                slide2.append(photoChoisie2_num);
    return slide2;       

def choisirPhotoMaximisantTransitionAlea(photos_num,slide,slideACompleter,patience):
    '''input: photos_num  l'ensemble de numero des photos 
               slide       
               slideACompleter
       output: num du photo qui maximise le score de la transition etre slide et slideACompleter''' 
    scoreMaximum = -1;
    photoChoisie_num = None;
    k = 0;
    while k<=patience and len(photos_num)!=0 : 
        num = random.choice(photos_num);
        slideACompleter.append(num);
        score = score_trans(slide,slideACompleter);
        if  score > scoreMaximum:
            photoChoisie_num = num;
            scoreMaximum = score;
            k = 0;
        else:
            k += 1;
        slideACompleter.remove(num)
    return photoChoisie_num;

######################  exercice 4 #######################################
def transposition(l,i,j):
    l2 = l.copy();
    l2[i] = l[j];
    l2[j] = l[i];
    return l2;
#def voisinage_Permuter_deux_vignettes_non_voisins(presentation):
#    voisinage = [];
#    for i in range(len(presentation)):
#        for j in range(i+2,len(presentation)):
#            voisinage.append(presentation);
#    return voisinage;
def Permuter_deux_vignettes(presentation):
    i = np.random.choice(range(len(presentation)-2));
    j = np.random.choice(range(i+2,len(presentation)));
    presentation2 = transposition(presentation,i,j);
    return presentation2;
def changer_une_photo(slide1,slide2):
    assert len(slide1)==2
    assert len(slide2)==2
    a,b = random.choice([[0,1],[1,0]]);
    c,d = random.choice([[0,1],[1,0]]);
    slide3 = [slide1[a],slide2[c]];
    slide4 = [slide1[b],slide2[d]];
    return slide3,slide4
def Permuter_une_des_deux_photos_V_entre_deux_vignettes(presentation):
    slides_2_photos_num = [num for num in range(len(presentation)) if len(presentation[num])==2];
    i,j = np.random.choice(slides_2_photos_num,2,replace = False);
    slide1,slide2 = changer_une_photo(presentation[i],presentation[j]);
    presentation2 = presentation.copy();
    presentation2[i] = slide1;
    presentation2[j] = slide2;
    return presentation2
def recherche_locale_descente_stochastique(presentation,patience,duration):
    '''input:  duration->temps maximum d'execution de la recherche
               patience->nb maximum de recheches consecutives sans amelioration tolerees
       output: la meilleur presentations trouvee
    '''
    k = 0;
    timeStart = time.time();
    score = evaluate(presentation);
    while k<patience and time.time()-timeStart < duration:
        voisin = random.choice([Permuter_deux_vignettes,Permuter_une_des_deux_photos_V_entre_deux_vignettes]);
        presentation2 = voisin(presentation);
        score2 = evaluate(presentation2);
        if score2 > score:
            socre = score2;
            presentation = presentation2;
            k = 0;
        else:
            k += 1;
    if k == patience:
        print("patience depassee")
    else:
        print("temps depasse")
    return presentation;

pathIn_4 = './../data/a_example.txt';
pathIn_1000_47K = './../data/c_memorable_moments.txt';
pathIn_90000_4M = './../data/d_pet_pictures.txt';
pathIn_80000_6M = './../data/e_shiny_selfies.txt';
pathIn_80000_9M = './../data/b_lovely_landscapes.txt';
p = 1
#photos, photosH, photosV = read("b_lovely_landscapes.txt",p)
photos, photosH, photosV = read(pathIn_1000_47K,p);
#photos, photosH, photosV = read(pathIn_80000_9M,p);
photos_num = [photo.num for photo in photos];
photosV_num = [photo.num for photo in photosV];
photosH_num = [photo.num for photo in photosH];

p1 = simple_presentation(photos,photosH,photosV)
write(p1);
print(evaluate(p1))
write(presentation)
p1 = gloutonSimple(photos_num,photosV_num,photosH_num,60)
print("glouton simple evalue(p1) = ",evaluate(p1))   
patience = 10;
duration = 60;#secondes
photos_num = [photo.num for photo in photos];
photosV_num = [photo.num for photo in photosV];
photosH_num = [photo.num for photo in photosH];
s = time.time();
p2 = gloutonAlea(photos_num,photosV_num,photosH_num,patience)
print("glouton alea alea = {} evalue(p2) = {}, temp = {}".format(patience,evaluate(p2),time.time()-s));   

patience = 100
temps = 60
s = time.time();
p3 = recherche_locale_descente_stochastique(p1,patience,temps);
print("glouton stochastique(patience = {},dureeMaximum = {}), evalue(p3) = {}, temps ={} ".format(patience,temps,evaluate(p3),time.time()-s));   

#=======
print("glouton alea alea = {} evalue(p2) = {} ".format(patience,evaluate(p2)));   

