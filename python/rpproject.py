# -*- coding: utf-8 -*-
"""
RP-PROJECT
"""


import numpy as np
import time
import random

def read(f,p):
    file = open(f,'r')
    n = int(file.readline());
    photos = []
    photosV = []
    photosH = []
    for i in range(int(np.floor(n*p))):
        line = file.readline()
        line = line.replace("\n", "")
        line = line.split(' ')
        photo = [line[0],int(line[1]),set(line[2:]),i]
        photos.append(photo)
        if photo[0] == 'H':
            photosH.append(photo)
        if photo[0] == 'V':
            photosV.append(photo)
            
    file.close()
    return photos, photosH, photosV

p = 0.5

photos, photosH, photosV = read("./../data/b_lovely_landscapes.txt",p)
#photos, photosH, photosV = read('./../data/c_memorable_moments.txt',p)

instance = [photos, photosH, photosV]

def simple_presentation(instance):
    presentation = []
    photosH = instance[1]
    photosV = instance[2]
    for photo in photosH:
        presentation.append([photo[3]])
    for i in range(len(photosV)//2):
        presentation.append([photosV[2*i][3],photosV[2*i+1][3]])
    return presentation

presentation = simple_presentation(instance)


def write(presentation):
    f = open('./../resultat/resultat.txt','w')
    f.writelines([str(len(presentation)),'\n'])
    for photo in presentation:
        if len(photo) == 1:
            f.writelines([str(photo[0]),'\n'])
        if len(photo) == 2:
            f.writelines([str(photo[0]),' ',str(photo[1]),'\n'])
    f.close()
    return

write(presentation)




def score_trans(tag1,tag2):
    '''
    compares sets of words
    tag1, tag2 = sets
    '''
    return min(len(tag1.intersection(tag2)),len(tag1.difference(tag2)),len(tag2.difference(tag1)))


def evaluate(photos,presentation):
    score = 0
    des = []
    for i in range(len(presentation)):
        if len(presentation[i]) == 1 :
            des.append(photos[presentation[i][0]][2])
        if len(presentation[i]) == 2 :
            des.append(set(list(photos[presentation[i][0]][2]) + list(photos[presentation[i][1]][2])))
    for j in range(len(des)-1):
        #score += min(len(des[j].intersection(des[j+1])),len(des[j].difference(des[j+1])),len(des[j+1].difference(des[j])))
        score += score_trans(des[j],des[j+1])
    return score

print(evaluate(photos,presentation))



def glouton_random(instance):
    photos,photosH, photosV = instance[0], instance[1],instance[2]
    presentation = []
    #tag = []
    if random.random() > 0.5:
        slide = random.choice(photosH)
        presentation.append(slide[3])
    else:
        slide = random.sample(photosV,2)
        presentation.append(slide[0][3])
        presentation.append(slide[1][3])
    photo = set(range(len(photos)))    
    photo_libre = list(photo.difference(set(presentation)))
    
    return presentation,photo_libre
    
    
def glouton_iter(instance,presentation,photo_libre,timelimit):
    start = time.time()
    photos = instance[0]
    current_score = 0
    while(((time.time()-start) < timelimit) or photo_libre == []):
        for i in photo_libre:
            if len(presentation[-1])==1:
                score = score_trans(photos[i][2],photos[presentation[-1][0]][2])
            if len(presentation[-1])==2:
                score = score_trans(photos[i][2],set(list(photos[presentation[-1][0]][2]) + list(photos[presentation[-1][1]][2])))
            if score >= current_score:
                current_score = score
                position = i
        photo_libre = list(set(photo_libre) - set(position))

    
    
    
    
    
    