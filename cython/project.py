# -*- coding: utf-8 -*-
"""
RP-PROJECT
"""
import numpy as np
import time
import random
#from fonctions import simple_presentation_cy 
import fonctions

def read(f,p):
    '''input: f le chemin de ficher entree (chaine de caracteres)
              p pourcentage de lignes
       sortie: photos  l'ensemble des photos (liste d'objects)
               photosV l'ensemble des photos verticaux (liste d'objects)
               photosH l'ensemble des photos horizontaux (liste d'ojects)
    '''
    photos = []
    photosV_num = []
    photosH_num = []
    with open(f,'r') as file:
        n = int(file.readline())
        for i in range(int(n*p)):
            line = file.readline()
            line = line.replace("\n", "")
            line = line.split(' ')
            photo = fonctions.Photo(line[0],set(line[2:]),i);
            photos.append(photo)
            if line[0] == 'H':
                photosH_num.append(i)
            else:
                photosV_num.append(i)
    return n,photos, photosH_num, photosV_num
####################################laisser ici pour comparer############
def simple_presentation(photosH_num,photosV_num):
    presentation = []
    for num in photosH_num:
        presentation.append([num])
    for i in range(len(photosV_num)//2):
        presentation.append([photosV_num[2*i],photosV_num[2*i+1]])
    return presentation
############################################################
    

def score_trans(slide1,slide2,photos):
    '''
    compares sets of words
    tag1, tag2 = sets
    '''
    assert slide1 != None, "Dans fonction score_trans, slide1 == None" 
    assert slide2 != None, "Dans fonction score_trans, slide2 == None"
    tag1 = getMots(slide1,photos);
    tag2 = getMots(slide2,photos);
    k1 = len(tag1.intersection(tag2))
    k2 = len(tag1.difference(tag2))
    k3 = len(tag2.difference(tag1))
    return min(k1,k2,k3)

def getMots(slide,photos):
    '''input: slide (liste de numero des photos contenus)
       output: l'ensemble des mots des photos contenus dans la slide'''
    assert slide != None, "fonction getMots prend un slide qui n'est pas None comme argument"
    if len(slide) == 1 :
        return photos[slide[0]].mots;
    else:
        return photos[slide[0]].mots.union(photos[slide[1]].mots);

def evaluate(presentation,photos):
    ''' input:   photos:l'ensemble des photos (liste d'objects)
                 presentation: l'ensemble des slide (liste de slides)
        output:  score de la presentation
    '''
    score = 0
    for i in range(len(presentation)-1):
        score += score_trans( presentation[i], presentation[i+1],photos);
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
        score = score_trans(slide,slideACompleter,photos);
        if  score > scoreMaximum:
            photoChoisie_num = num;
            scoreMaximum = score;
        slideACompleter.remove(num)
    return photoChoisie_num;
                    

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
            if photos[num].orientation == "V"and num in photosV_num:
                photosV_num.remove(num);
            elif num in photosH_num:
                photosH_num.remove(num);
#        print("photos used: ",photosUsed);
        slide = slideMaximisantTransition(photos_num,photosV_num.copy(),presentation[-1]);     # trouver la prochaine vignette qui maximisant la transition
#        print("slide :");
#        slide.afficher();
    return presentation;
 

def gloutonAlea(photos_num,photosV_num,photosH_num,patience,photos):
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
        slide = slideMaximisantTransitionAlea(photos_num,photosV_num.copy(),presentation[-1],patience,photos);     # trouver la prochaine vignette qui maximisant la transition
#        print("slide :");
#        slide.afficher();
    return presentation;

def slideMaximisantTransitionAlea(photos_num,photosV_num,slide,patience,photos):
    slide2 = None;
    photoChoisie_num = choisirPhotoMaximisantTransitionAlea(photos_num,slide,[],patience,photos)
    if photoChoisie_num != None:
        slide2 = [photoChoisie_num];
#        print("slide2 :")
#        slide2.afficher();
        if photos[photoChoisie_num].orientation == "V":
            photosV_num.remove(photoChoisie_num);
            photoChoisie2_num = choisirPhotoMaximisantTransitionAlea(photosV_num,slide,slide2,patience,photos);
            if photoChoisie2_num != None:
                slide2.append(photoChoisie2_num);
    return slide2;       

def choisirPhotoMaximisantTransitionAlea(photos_num,slide,slideACompleter,patience,photos):
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
        score = score_trans(slide,slideACompleter,photos);
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
    x = l[i];
    l[i] = l[j];
    l[j] = x;
#def voisinage_Permuter_deux_vignettes_non_voisins(presentation):
#    voisinage = [];
#    for i in range(len(presentation)):
#        for j in range(i+2,len(presentation)):
#            voisinage.append(presentation);
#    return voisinage;
def Permuter_deux_vignettes(presentation):
    i = np.random.choice(range(len(presentation)-2));
    j = np.random.choice(range(i+2,len(presentation)));
    transposition(presentation,i,j);
    return presentation
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
def recherche_locale_descente_stochastique(presentation,patience,duration,photos):
    '''input:  duration->temps maximum d'execution de la recherche
               patience->nb maximum de recheches consecutives sans amelioration tolerees
       output: la meilleur presentations trouvee
    '''
    k = 0;
    timeStart = time.time();
    score = evaluate(presentation,photos);
    while k<patience and time.time()-timeStart < duration:
        voisin = random.choice([Permuter_deux_vignettes,Permuter_une_des_deux_photos_V_entre_deux_vignettes]);
        presentation2 = voisin(presentation);
        score2 = evaluate(presentation2,photos);
        if score2 > score:
            score = score2;
            presentation = presentation2;
            k = 0;
        else:
            k += 1;
    if k == patience:
        print("patience depassee")
    else:
        print("temps depasse")
    return presentation;








#============================== Main ====================================

'''simple_presentation verifiee avec Checker. correct 100%
'''    
pathIn_4 = './../data/a_example.txt';
pathIn_80000_9M = './../data/b_lovely_landscapes.txt';
pathIn_1000_47K = './../data/c_memorable_moments.txt';
pathIn_90000_4M = './../data/d_pet_pictures.txt';
pathIn_80000_6M = './../data/e_shiny_selfies.txt';
p = 1
##photos, photosH, photosV = read(pathIn_4,p);
#n,photos, photosH_num, photosV_num = fonctions.read(pathIn_80000_9M,p)
#n,photos, photosH_num, photosV_num = read(pathIn_80000_9M,p)
n,photos, photosH_num, photosV_num = read(pathIn_1000_47K,p);
#photos, photosH, photosV = read(pathIn_90000_4M,p);
#photos, photosH, photosV = read(pathIn_80000_6M,p);

photos_num = list(range(n));

################ pour tester presentation simple et cython, corredct #############
#start = time.time();
#presentation = simple_presentation(photosH_num.copy(),photosV_num.copy())
#t1 = time.time()-start;
#presentation = fonctions.simple_presentation_cy(photosH_num.copy(),photosV_num.copy())
#t2 = time.time()-t1;
#print("pour simple_presentation {} fois plus vite".format(t1/t2));
#print(evaluate(presentation,photos))
#write(presentation)
#####################################################################

   
################# pour tester gloutonSimple et  cython ,      correct ###############33#
#n1,photos1, photosH_num1, photosV_num1 = fonctions.read(pathIn_1000_47K,1)
#photos_num1 = list(range(n1));
#start = time.time();
#p1 = gloutonSimple(photos_num1.copy(),photosV_num1.copy(),photosH_num1.copy(),60)
#t1 = time.time()-start;
#p1 = gloutonSimple(photos_num1.copy(),photosV_num1.copy(),photosH_num1.copy(),60)
#t2 = time.time()-t1;
#print("pour gloutonSimple {} fois plus vite".format(t1/t2));
#print("glouton simple evalue(p1) = ",evaluate(p1,photos))
#############################################################



############################  pour tester glouton alea,      correct ###########
#patience = 10;
#duration = 60;#secondes
#
#start = time.time();
#p2 = gloutonAlea(photos_num.copy(),photosV_num.copy(),photosH_num.copy(),patience,photos)
#print("glouton alea alea = {} evalue(p2) = {}".format(patience,evaluate(p2,photos)));   
#t1 = time.time()-start;
#p2 = fonctions.gloutonAlea_cy(photos_num.copy(),photosV_num.copy(),photosH_num.copy(),patience,photos)
#t2 = time.time()-t1;
#print("pour gloutonAlea {} fois plus vite".format(t1/t2));
#print("glouton alea alea = {} evalue(p2) = {}".format(patience,evaluate(p2,photos)));   
###################################################

patience = 10
temps = 60
p2 = gloutonAlea(photos_num.copy(),photosV_num.copy(),photosH_num.copy(),patience,photos)
start = time.time();
p3 = recherche_locale_descente_stochastique(p2,patience,temps,photos);
t1 = time.time() - start
p3 = fonctions.recherche_locale_descente_stochastique_cy(p2,patience,temps,photos);
t2 = time.time() - t1;
print("pour recherche_locale_descente_stochastique {} fois plus vite".format(t1/t2));
print("glouton stochastique(patience = {},dureeMaximum = {}), evalue(p3) = {}".format(patience,temps,evaluate(p3,photos)));   

