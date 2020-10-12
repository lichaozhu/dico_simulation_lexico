#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 	créé par Lichao Zhu 
#	lichao.zhu@gmail.com
#	http://zhulichao.fr


import pprint
#import treetaggerwrapper
import nltk
from nltk.corpus import stopwords

from nltk.tag.stanford import StanfordPOSTagger

from nltk.stem.snowball import FrenchStemmer

import stanza

import math

import json
import codecs
import glob
import re
import justext
# import datetime
# import subprocess
from datetime import date
import time
import chardet
import os
import os.path
from os import listdir
from os.path import isfile, join	

global lignes, lines, stop_words, p



u = codecs.open("./def_sem/Defi_democratie.txt", "w+", "utf-8")
#m = codecs.open('./def_sem/DEMOCRATIE_NV2.txt', 'w+', 'utf-8')
q = codecs.open('./def_sem/Axes_XY_democratie_new.txt', "w+", "utf-8")
w = codecs.open('./def_sem/Reseaux_democratie.txt', 'w+', 'utf-8')

bibi = codecs.open("./def_sem/phras_opaq_defi.txt", "w+", "utf-8")

z = codecs.open("DAF.txt", "r", "utf-8")
contenu = z.read()
z.close()



lignes = re.split(r"\n", contenu)




#tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR = "")




root_path="/home/lc/Bureau/dico_tlfi/Etiquettes/StanfordPOSTagger/stanford-postagger-full-2018-10-16/"
pos_tagger = StanfordPOSTagger(root_path+"models/french.tagger", root_path + "stanford-postagger.jar", encoding="utf8")

nlp = stanza.Pipeline(lang='fr', processors="tokenize,pos,lemma")

stop_words = stopwords.words('french')

#print (stop_words)



def pos_tag(mot):
	tokens = nltk.word_tokenize(mot.upper())
	#print (nltk.word_tokenize("C'est un démocrates, et il est antidémocratique."))
	#print("token : "+ str(tokens))
	tags = pos_tagger.tag(tokens)
	return tags
	

def racine(mot): #racinisation 
	stemmer=FrenchStemmer()
	racine = stemmer.stem(mot)
	return racine


def def_entree(mot, segs) :
	list_def=[] 
	for seg in segs : #au niveau de phrase
		new_seg = re.sub(r"^\s+", "", str(seg))
		
		if mot not in new_seg and new_seg.count(' ')>1 and len(new_seg)>8 and new_seg not in list_def and new_seg is not None :
			list_def.append(str(new_seg))
	return list_def



def def_segmenteur(mot, segs, list_def):
	list_ind = []
	for phras in segs : 
		for ele in list_def : 
			if ele in phras : 
				ind = segs.index(phras)
				if ind not in list_ind : 
					list_ind.append(ind)

	list_ind.append((len(segs)))
	return list_ind


def seg_entre_def(list_ind, segs):
	list_new_entre = []

	n=0
	while n < len(list_ind)-1:
		seg = segs[int(list_ind[n]+1):int(list_ind[n+1])]
		seg = ".".join(seg)
		list_new_entre.append(seg)
		n = n+1 

	return list_new_entre	






######################################################################################################





def mot_plein(mot, definition):
	doc = nlp(definition)
	accum = {}
	for sent in doc.sentences:
		for word in sent.words:
			pos = word.pos
			lem_mp = word.lemma
			#space_def = mot + '\t' + lemma #format : entrée <tab> lemme(item définitoire)
			stop_words = stopwords.words('french')
			stop_words += ['ce', 'titre célèbre', 'pratique', 'sport', 'contraire', 'hiver','contraires', 'lequel', "lequels", 'Lequel','qualificatif', 'apposition', 'au', 'adj', 'siècle', 'xxie', 'xixe', 'xxe', 'extension', 'ajectivement', 'plus', "application", "titre", "emporté", "commencé", "affaiblissement", "étendre", "appartenir", "appartient", "résulte", "procéder", "soumet", "métonymie", "assurer", "assure", "introduire", "manière", "afficher", "simple", "subsiste", "fait", "non", "oui", "subsister", "subsistent", "parfaite", "découlent", "découle", "découler", "parfait", "venir", "peut", "ce", "cette", "grande", "grand", 'certains', 'certain', 'certaine', 'certaines', 'connu', 'connue', 'connaître', 'conforme', 'dire', 'tcha', 'doit','être', 'xixe', 'désigner', 'désigne', 'désignant', 'façon', 'adj', 'loc', 'adv', 'deux', 'trois', 'quatre', 'siècle', 'extension', 'adjectivement', 'par', 'analogie', 'plus', 'selon', 'xvi', 'xviiie', 'xvie', 'xve', 'gran', 'xive', 'xviie', 'xive', 'xviii', 'xvii', 'xv', 'xiv', 'xiii', 'xii', 'aux', 'avec', 'ce', 'où', "lequel", 'lesquels', "duquel", 'ces', 'dans', 'de', 'des', 'du', 'elle', 'en', 'et', 'eux', 'il', 'ils', 'je', 'la', 'le', 'les', 'leur', 'lui', 'ma', 'mais', 'me', 'même', 'mes', 'moi', 'mon', 'ne', 'nos', 'notre', 'nous', 'on', 'par', 'pas', 'pour', 'qu', 'que', 'qui', 'sa', 'se', 'ses', 'son', 'sur', 'ta', 'te', 'tes', 'toi', 'ton', 'tu', 'un', 'une', 'vos', 'votre', 'vous', 'leurs']
			if len(mot) < 25 : 
				if "NOUN" in pos and lem_mp not in stop_words and lem_mp in accum and not re.search(r'titre', mot): 
			
					accum[(mot+' '+str(lem_mp))]+=1
				#bibi.write(g4.upper()+'\t'+defi+'\t'+str(accum[(g4.upper(), defi)]))
				#bibi.write('\n')
	
				elif "NOUN" in pos and lem_mp not in stop_words and lem_mp not in accum and not re.search(r'titre', mot): 

					accum[(mot+" : "+str(lem_mp))]=1
	return accum

def extra_def(mot, seg):

	liste_def_1 = []
	
	i_def = re.split(r'\.', seg)
	
	
	if mot not in liste_def_1 and re.search(r'[a-z]', seg):
		seg_v = re.split(r' ',seg)

		for ele in seg_v : 
		
			if "VINF" in pos_tag(mot) or "NPP" in pos_tag(mot) or "ADJ" in pos_tag(mot) or "N" in pos_tag(mot) or "NC" in pos_tag(mot) :
					
				if racine(ele) in racine (mot) :
					
					pass
	
				else :
					liste_def_1.append(ele)
					#print (ele)
			else :
				liste_def_1.append(ele)


	return liste_def_1



def extra_trans_phras(mot, seg) :
	liste_transphras = []
	transphras = re.split(r'\.', seg)
	for ele in transphras : 
		ele = re.sub(r'^\s*', '', ele)
		if mot in ele and "," not in ele :
			liste_transphras.append(ele)
		elif mot in ele and "," in ele and len(re.split(r",", ele)[1]) < 12 : 
			liste_transphras.append(ele)


	return liste_transphras
#
def extra_phras_opaque(mot, segs): #mot = entrée du dico ; segs = phraséologisme opaque et sa définition
	mot = mot.lower()
	liste_phras = {}
	phras_split = re.split(r'\.', segs)	
	for seg in phras_split : 
		if mot in seg and seg.count(' ')>3 and seg.count(',')>0 :

			i_phras_opaque = re.split(r",", seg)[0] #collocations opaques

			def_phras_opaque = re.split(r",", seg)[1] #def collocations opaques
			
			
			#if mot in i_phras_opaque :
			if mot in i_phras_opaque and mot not in def_phras_opaque and i_phras_opaque is not None and len(def_phras_opaque)>12: 

				i_phras_opaque=re.sub(r'^\s?', '', i_phras_opaque)
				dico_phras = mot_plein(i_phras_opaque, def_phras_opaque)
				if dico_phras : 			
					return dico_phras # (phrasélogisme opaque '\t' definition de phraséologisme opaque : fréquence)

######################################""
def noeud(mot, seg):
	liste_noeud = []
	words = re.split(r' ', seg)
	for word in words:
		if word not in stop_words and word != mot:
			liste_noeud.append(word)
	return liste_noeud


def nettoyage(seg):
	tt = re.sub(r"\"", "", str(seg))
	tt = re.sub(r"d\'", "", tt)
	tt = re.sub(r"\'", " ", tt)
	tt = re.sub(r"\.", " ", tt)
						#tt = re.sub(r"c\'", "", tt)
						#tt = re.sub(r"C\'", "", tt)

	tt = re.sub(r" contraire| contraires", " ", tt)
	tt = re.sub(r" .+?ant$| .+?ants$"," ", tt)
	#tt = re.sub(r"l\'", "", tt)
	#tt = re.sub(r"s\'", "", tt)
	tt = re.sub(r"D\'", "", tt)
	tt = re.sub(r"L\'", "", tt)
	tt = re.sub(r"S\'", "", tt)
	#tt = re.sub(r"QU\'", "", tt)
	#tt = re.sub(r"qu\'", "", tt)
	tt = re.sub(r"N\'", "", tt)
	tt = re.sub(r"\-", " ", tt)
	#tt = re.sub(r"n\'", "", tt)
	tt = re.sub(r"\[", "", tt)
	tt = re.sub(r",", "", tt)
	tt = re.sub(r"\]", "", tt)
	tt = re.sub(r"\(", "", tt)
	tt = re.sub(r"\)", "", tt)
	#tt = re.sub(r"\d+", "", tt)

	return tt






def word_to_list(mot):

	vide = []

	liste_split= []
	liste_mots = []
	liste_mots_def = []
	liste_mots_exe = []
	liste_mots_phras_trans = []
	liste_mots_phras_opaque = []
	liste_vide = []
	liste_opaque = []
	liste_trans = []
	checklist_phras = []
	liste_def_entree = []
	def_dico = {}
	phras_trans_dico = {}
	whole_semantic_words = {}
	words_freq = []
	whole_words = {}
	mot = mot.lower()
	dic = {}
	liste_trans = []

	stem = racine(mot)
	global stop_words
	#lemma = lemma[:-1]
	
	v = 1
	
	
	
	#tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR = "")

	stop_words = stopwords.words('french')
	
	
	for line in lignes :
		p = 2
		
		g = re.search(r'^(I\. |II\. |III\. |IV\. |V\. |VI\. |VII\. |VIII\. |IX\. |X\. |XI\. |XII\. |XIII\. |XIV\. |XV\. |\*|XVI\.|\'|)([A-ZŒÉÈÔÇÀÙÊÆÏÂËÄÎŸÛÜÖ]+)([a-zœéèôçàùêæïâëäîÿûüö\(,\);\-\'\'«»\s\n\r]+)', line) #DÉMOCR[A-ZÉÀÈÙÔÖÊÂÇÆËÏÎŒ]+

		
		if g : 
			if stem in str(g.group(2).lower()):
				g4 = g.group(2).lower()
				k = open("def_sem/%s.txt"%g4.upper(), "a+")#créer pour chaque entrée un fichier dont le nom est l'entrée en majuscule et dans lequel on met les définiitons et les phraséologismes transparents (optionnels)	
				ind = lignes.index(line)
				tt_cg = re.sub('%s'%g4, '', str(lignes[ind]).lower())
				tt = "".join(lignes[ind+2:ind+35]).lower()
				
				tetris = re.split(r'\.|▪', tt)
				
				liste_definitions = def_entree(g4, tetris)#extraire les définitions

				liste = def_segmenteur(g4, tetris, liste_definitions)
				
				a = seg_entre_def(liste, tetris)

				

				liste_items = {}

				for item in a :

					
			
					#print (item)
					if item not in vide and item != "" : 
						#print ("Définition : " + item)
						vide.append(item)
						#k.write("Définition : " + item)
						#k.write('\n')
						

						print(mot_plein(g4, item)) #monolexical : entrée + item déf
						
						print (extra_phras_opaque(g4, item)) #polylexical : entrée + item déf
						bibi.write(str(extra_phras_opaque))

				#print(accum)
					for trans in extra_trans_phras(g4, item) : 
						if trans not in vide and len(trans) < 40 and trans.count(" ")<4: 

							#print ("Phraséologisme transparent : " + trans)
							vide.append(trans)

						else : 
							pass

						words_trans = nettoyage(noeud(g4, trans))
						spaces_trans = re.split(r' ', words_trans) 
						
						for space_2 in spaces_trans:
							
							if space_2 not in stop_words and g4 not in space_2 and len(space_2)>3 and 'ADV' not in pos_tag(space_2) and 'NPP' not in pos_tag(space_2) and 'DET' not in pos_tag(space_2) and 'ADJ' not in pos_tag(space_2) : 
							
								liste_mots.append(space_2)
								
								
								if space_2 in words_freq :
									dic[space_2] += 1
									k.write("Phraséologisme transparent : "+space_2)
									k.write('\n')
									whole_semantic_words[g4.upper()] = dic
								
								
								else:
									dic[space_2]=1
									whole_semantic_words[g4.upper()] = dic
									#words_freq.append(space_2)
									
									
									
								if space_2 in whole_words :
									whole_words[space_2] += 1
								
								else: 
									whole_words[space_2] = 1
								


						else : 
							pass
							
						
			else:
				pass
	
	
	return liste_mots


			
					
			

						




	
							
#def moulinette(liste):






def list_to_word(liste):
	for i in liste : 
		i = i.upper()
		b = word_to_list(i)

	return b



#a = monolexical("DÉMOCRATIE")
#b = polylexical(a)

# for ele in a.items() :
# 	print (a)
# 	print ('\n')
#print(b)


nv1 = word_to_list('DÉMOCRATIE')
nv2 = list_to_word(nv1)

print (nv2)




