#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Christina Indudhara/ UID: 204745788
Ignat Kulinka/ UID: 304845754
PIC 16
Professor Ji
Final Project
    Part 1: character name extraction
    Part 2: network building
    Part 3: pretty graph
"""

from collections import Counter
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize, sent_tokenize
import matplotlib.pyplot as plt
import networkx as nx
import operator
import math
import pygraphviz as pgv

NER_tagger = StanfordNERTagger('C:\Users\chris\Desktop\iCloudDrive\UCLA Classes\PIC 16\stanford-ner-2018-02-27\classifiers\english.all.3class.distsim.crf.ser.gz',
                       'C:\Users\chris\Desktop\iCloudDrive\UCLA Classes\PIC 16\stanford-ner-2018-02-27\stanford-ner.jar',
                       encoding="utf-8")


def import_txt(myfile):
    '''
    This function lets us import .txt novels into python
    '''
    with open(myfile, 'r') as N:
        novel = N.read()
        novel = unicode(novel, errors='replace')
    N.close()
    
    return novel


def find_characters(classified_novel):
    '''
    This function lets us combine partial names to find full names of characters
    '''    
    character_list = []
    i = 0
    while i < len(classified_novel):
        if classified_novel[i][1] == 'PERSON':
            if classified_novel[i+1][1] == 'PERSON':
                if classified_novel[i+2][1] == 'PERSON':
                    character_list.append(classified_novel[i][0].lower() +
                                    " " + classified_novel[i+1][0].lower() +
                                    " " + classified_novel[i+2][0].lower())
                    i+=1
                else:
                    character_list.append(classified_novel[i][0].lower() +
                                    " " + classified_novel[i+1][0].lower())
                i+=1 
            else:
                character_list.append(classified_novel[i][0].lower())
        i+=1 
    return character_list

def flatten(counts):
    """
    This functions lets us combine the counts of characters and list them
    under partial names
    """
    
    single_names = {}
    long_names = {}
    for i in range(len(counts.items())):
        if(len(counts.items()[i][0].split(" ")) <= 1):
            single_names[str(counts.items()[i][0])] = counts.items()[i][1]
        else:
            long_names[str(counts.items()[i][0])] = counts.items()[i][1]
    
    starter_list = [[[x[0]],x[1]] for x in long_names.items()]
    for i in range(len(single_names.items())):
        matched = False
        for j in range(len(starter_list)):
            if(single_names.items()[i][0] in starter_list[j][0][0].split(" ")):
                starter_list[j][0].append(single_names.items()[i][0])
                starter_list[j][1] += single_names.items()[i][1]
                matched = True
                break
                
        if(matched == False):
           starter_list.append([[single_names.items()[i][0]], single_names.items()[i][1]]) 
    
 
    return starter_list
    
def sort_counts(combined_counts):
    """
    This function sorts the counts of characters by least to greatest
    """
    sorted_counts = sorted(combined_counts, key=operator.itemgetter(1))
    return (sorted_counts)
    

def sent_tagged(novel_text):
    """
    This function takes in the text of the novel and outputs the 
    novel but split into sentences within a list, and words tagged 
    with stanford NER 3-class.
    """
    novel = []
    novel_tagged = NER_tagger.tag(word_tokenize(novel_text))
    novel_sent_tokenized = sent_tokenize(novel_text)
    novel_tokenized = [word_tokenize(novel_sent_tokenized[i]) for i in range(len(novel_sent_tokenized))]
    sent_length = [len(novel_tokenized[i]) for i in range(len(novel_sent_tokenized))]
    
    a = 0
    b = 0
    for i in sent_length:
        b += i
        novel.append(novel_tagged[a:b])
        a = b
    
    return(novel)
    
def combine_persons(sent_tagged):
    """
    This function returns a list of characters in a sentence. This function
    takes the novel as a list of sentences where each sentence is word_tokenized
    """
    persons = []
    i = 0
    while i < len(sent_tagged) - 3:
        if sent_tagged[i][1] == 'PERSON':
            if sent_tagged[i+1][1] == 'PERSON':
                if sent_tagged[i+2][1] == 'PERSON':
                    persons.append(sent_tagged[i][0].lower() + 
                                   " " + sent_tagged[i+1][0].lower() + 
                                   " " + sent_tagged[i+2][0].lower())
                    i+=1
                else:
                    persons.append(sent_tagged[i][0].lower() + 
                                   " " + sent_tagged[i+1][0].lower())
                i+=1 
            else:
                persons.append(sent_tagged[i][0].lower())
        i+=1 
    return(persons)


def connect_persons(persons, character_list):
    """
    This function creates connections between people in persons
    """
    edge_list = []
    persons_fixed = []
    for i in range(len(persons)):
        for j in range(len(character_list)):
            if(persons[i] in character_list[j][0]):
                persons_fixed.append(sorted(character_list[j][0], key=len)[-1])
    
    for i in range(1, len(persons_fixed)):
        edge_list.append((persons_fixed[0], persons_fixed[1]))
    
    return(edge_list)
                

def edge_maker(novel_sent_tagged, combined_counts):
    """
    This function combines a list of persons in a sentence and makes them
    into connections tuples!
    """
    edge_list = []
    
    for i in range(len(novel_sent_tagged)):
        persons = combine_persons(novel_sent_tagged[i])
        edge_list.extend(connect_persons(persons, combined_counts))
        
    return(edge_list)
       
def char_full_name(combined_counts):
    full_names = []
    for i in range(len(combined_counts)):
        full_names.append(sorted(combined_counts[i][0], key=len)[-1])
    
    return(full_names)
        

def top_n(combined_counts, n):
    sorted_counts = sort_counts(combined_counts)
    if n == 0:
        n = len(combined_counts)
    
    return(sorted_counts[len(combined_counts) - n:])
    
def drawGraph(G):
    """ This function draws the graph in a visually pleasing way 
    """
    # Drawing with network x
    page_rank = nx.pagerank(G)
        
    pos = nx.nx_pydot.graphviz_layout(G)
    plt.figure(figsize=(15,10))
        
    label_pos = {}
    for i in pos:
        label_pos[i] = (pos[i][0] , pos[i][1] - (math.exp(page_rank[i]) * 12))
        
    labels = nx.draw_networkx_labels(G, label_pos, font_weight = 'bold', font_size = 9)
    nodes = nx.draw_networkx_nodes(G, pos, 
                                   node_size = [2000 * page_rank[i] for i in list(nx.nodes(G))],
                                   node_color = range(len(nx.pagerank(G))),
                                   cmap = plt.cm.Spectral)
        
    nodes.set_edgecolor('black')
        
    nx.draw_networkx_edges(G, pos, edge_color = 'grey', alpha = .70)
    plt.axis('off')

    plt.show()


