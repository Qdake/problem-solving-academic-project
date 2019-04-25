#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 18:37:08 2019

@author: wei
"""
#from libcpp.string cimport string

#from libcpp.set cimport set
import time;
import random;
import numpy as np
cpdef read_cy(str f, float p):
    '''input: f le chemin de ficher entree (chaine de caracteres)
              p pourcentage de lignes
       sortie: photos  l'ensemble des photos (liste d'objects)
               photosV l'ensemble des photos verticaux (liste d'objects)
               photosH l'ensemble des photos horizontaux (liste d'ojects)
    '''
    cdef int i
    cdef n
    cdef list photos = []
    cdef photosV_num = []
    cdef photosH_num = []
    with open(f,'r') as file:
        n = int(file.readline())
        for i in range(int(n*p)):
            line = file.readline()
            line = line.replace("\n", "")
            line = line.split(' ')
            photo = Photo(line[0],set(line[2:]),i);
            photos.append(photo)
            if line[0] == 'H':
                photosH_num.append(i)
            else:
                photosV_num.append(i)
    return n,photos, photosH_num, photosV_num

cpdef void write(list presentation):
    cdef list slide_num;
    with open('./../resultat/resultat.txt','w') as f:
        f.writelines([str(len(presentation)),'\n'])
        for slide_num in presentation:
            if len(slide_num) == 1:
                f.writelines([str(slide_num[0]),'\n'])
            if len(slide_num) == 2:
                f.writelines([str(slide_num[0]),' ',str(slide_num[1]),'\n'])

cdef class Photo:
    cdef public int num
    cdef public str orientation
    cdef public set mots
    #cdef char orientation
    def __init__(self,str orientation,set mots,int num):
        self.orientation = orientation;
        self.mots = mots; 
        self.num = num;
        
cpdef list simple_presentation_cy(list photosH_num,list photosV_num):
    cdef list presentation = [];
    for num in photosH_num:
        presentation.append([num]);
    cdef int i;
    for i in range(len(photosV_num)//2):
        presentation.append([photosV_num[2*i],photosV_num[2*i+1]])
    return presentation




cpdef int score_trans_cy(list slide1,list slide2,list photos):
    '''
    compares sets of words
    tag1, tag2 = sets
    '''
    cdef list tag1,tag2
    cdef int k1,k2,k3
#    assert slide1 != None, "Dans fonction score_trans, slide1 == None" 
#    assert slide2 != None, "Dans fonction score_trans, slide2 == None"
    tag1 = getMots_cy(slide1,photos);
    tag2 = getMots_cy(slide2,photos);
    k1 = len(set(tag1).intersection(set(tag2)))
    k2 = len(set(tag1).difference(set(tag2)))
    k3 = len(set(tag2).difference(set(tag1)))
    return min(k1,k2,k3)
    
cpdef list getMots_cy(list slide,list photos):
    '''input: slide (liste de numero des photos contenus)
       output: l'ensemble des mots des photos contenus dans la slide'''
#    assert slide != None, "fonction getMots prend un slide qui n'est pas None comme argument"
    cdef list r = [];
    cdef char mot 
    if len(slide)==1:
        return list(photos[slide[0]].mots)
    else:
        return list((photos[slide[0]].mots).union(photos[slide[1]].mots));

cpdef int evaluate_cy(list presentation,list photos):
    ''' input:   photos:l'ensemble des photos (liste d'objects)
                 presentation: l'ensemble des slide (liste de slides)
        output:  score de la presentation
    '''
    cdef int score = 0
    cdef int i
    for i in range(len(presentation)-1):
        score += score_trans_cy( presentation[i], presentation[i+1],photos);
    return score

cpdef list slideMaximisantTransition_cy(list photos_num,list photosV_num,list slide,list photos):
    cdef list slide2 = None;
    cdef int photoChoisie_num = choisirPhotoMaximisantTransition_cy(photos_num,slide,[],photos)
    if photoChoisie_num != None:
        slide2 = [photoChoisie_num];
#        print("slide2 :")
#        slide2.afficher();
        if photos[photoChoisie_num].orientation == "V":
            photosV_num.remove(photoChoisie_num);
            photoChoisie2_num = choisirPhotoMaximisantTransition_cy(photosV_num,slide,slide2,photos);
            if photoChoisie2_num != None:
                slide2.append(photoChoisie2_num);
    return slide2;            

cpdef choisirPhotoMaximisantTransition_cy(list photos_num,list slide,list slideACompleter,list photos):
    '''input: photos_num  l'ensemble de numero des photos 
               slide       
               slideACompleter
       output: num du photo qui maximise le score de la transition etre slide et slideACompleter''' 
    cdef int scoreMaximum = -1;
    cdef int photoChoisie_num = -1;
    cdef int num,score
    for num in photos_num: 
        slideACompleter.append(num);
        score = score_trans_cy(slide,slideACompleter,photos);
        if  score > scoreMaximum:
            photoChoisie_num = num;
            scoreMaximum = score;
        slideACompleter.remove(num)
    if photoChoisie_num==-1:
        return None
    else:
        return photoChoisie_num


######################      ALEA ######################################
        
    
cpdef list slideMaximisantTransitionAlea_cy(list photos_num,list photosV_num,list slide,int patience, list photos):
    cdef list slide2 = None;
    photoChoisie_num = choisirPhotoMaximisantTransitionAlea_cy(photos_num,slide,[],patience,photos)
    if photoChoisie_num != None:
        slide2 = [photoChoisie_num];
#        print("slide2 :")
#        slide2.afficher();
        if photos[photoChoisie_num].orientation == "V":
            photosV_num.remove(photoChoisie_num);
            photoChoisie2_num = choisirPhotoMaximisantTransitionAlea_cy(photosV_num,slide,slide2,patience,photos);
            if photoChoisie2_num != None:
                slide2.append(photoChoisie2_num);
    return slide2;       

cpdef choisirPhotoMaximisantTransitionAlea_cy(list photos_num,list slide,list slideACompleter,int patience,list photos):
    '''input: photos_num  l'ensemble de numero des photos 
               slide       
               slideACompleter
       output: num du photo qui maximise le score de la transition etre slide et slideACompleter''' 
    cdef int scoreMaximum = -1;
    cdef int photoChoisie_num = -1;
    cdef int k = 0;
    cdef int num,score
    while k<=patience and len(photos_num)!=0 : 
        num = random.choice(photos_num);
        slideACompleter.append(num);
        score = score_trans_cy(slide,slideACompleter,photos);
        if  score > scoreMaximum:
            photoChoisie_num = num;
            scoreMaximum = score;
            k = 0;
        else:
            k += 1;
        slideACompleter.remove(num)
    if photoChoisie_num==-1:
        return None
    else:
        return photoChoisie_num

cpdef list gloutonAlea_cy(list photos_num,list photosV_num,list photosH_num,int patience,list photos):
    # 1) initialization
    cdef int photoChoisie2_num,num
    cdef list slide;
    cdef list presentation = [];                    
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
        slide = slideMaximisantTransitionAlea_cy(photos_num,photosV_num.copy(),presentation[-1],patience,photos);     # trouver la prochaine vignette qui maximisant la transition
#        print("slide :");
#        slide.afficher();
    return presentation;
##################################################################################


############### to cythonize#############################33
cpdef void transposition_cy(list l,int i,int j):
    x = l[i];
    l[i] = l[j];
    l[j] = x;
cpdef changer_une_photo_cy(list slide1,list slide2):
    cdef int a,b,c,d
    cdef list slide3,slide4
    a,b = random.choice([[0,1],[1,0]]);
    c,d = random.choice([[0,1],[1,0]]);
    slide3 = [slide1[a],slide2[c]];
    slide4 = [slide1[b],slide2[d]];
    return slide3,slide4
cpdef list Permuter_une_des_deux_photos_V_entre_deux_vignettes_cy(list presentation):
    cdef int num,i,j
    cdef list slide1,slide2
    cdef list slides_2_photos_num = [num for num in range(len(presentation)) if len(presentation[num])==2]; # to do ameliorer
    i,j = np.random.choice(slides_2_photos_num,2,replace = False);
    slide1,slide2 = changer_une_photo_cy(presentation[i],presentation[j]);
    presentation[i] = slide1;
    presentation[j] = slide2;
    return presentation;   # pas besoin de retour
cpdef list Permuter_deux_vignettes_cy(list presentation):
    cdef int i,j
    i = np.random.choice(range(len(presentation)-2));
    j = np.random.choice(range(i+2,len(presentation)));
    transposition_cy(presentation,i,j);
    return presentation;
cpdef list recherche_locale_descente_stochastique_cy(list presentation,int patience,int duration,list photos):
    '''input:  duration->temps maximum d'execution de la recherche 
               patience->nb maximum de recheches consecutives sans amelioration tolerees
       output: la  meilleur presentations trouvee
    '''
    cdef list presentation2
    cdef int k = 0;
    cdef int timeStart = time.time();
    cdef int score2,score = evaluate_cy(presentation,photos);
    while k<patience and time.time()-timeStart < duration:
        voisin = random.choice([Permuter_deux_vignettes_cy,Permuter_une_des_deux_photos_V_entre_deux_vignettes_cy]);
        presentation2 = voisin(presentation);
        score2 = evaluate_cy(presentation2,photos);
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
