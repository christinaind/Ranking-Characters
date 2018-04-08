# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 01:46:42 2018

@author: chris
"""
import FinalNLTKProj as np

books = ['SherlockHolmesTheAdventuresAbbeyRange.txt','TheGreatGatsby.txt','1984.txt','BraveNewWorld.txt',
         'Frankenstein.txt','CrimeAndPunishment.txt','Harry-Potter-7-Deathly-Hollows.txt']

# Import the .txt of the novel and store it
novel_text = np.import_txt(books[0])

# Break up the novel into a list of words
tokenized_novel = np.word_tokenize(novel_text)

# Classify each word based on the 3-class Stanford NER classifier
classified_novel = np.NER_tagger.tag(tokenized_novel)

# Extract the character list
character_list = np.find_characters(classified_novel)

# Use counter to make a count of all the elements in the character_list
character_counts = dict(np.Counter(character_list))

# combine the counts of full names with partial ones
combined_counts = np.flatten(character_counts)

# sort the names by mentions in the movel
sorted_counts = np.sort_counts(combined_counts)

# tag the text in sentences 
novel_sent_tagged = np.sent_tagged(novel_text)

# make edges out of lists
edge_list = np.edge_maker(novel_sent_tagged, combined_counts)
                    
# create a graph
G = np.nx.Graph()
# Add nodes and edges
G.add_nodes_from([i.title() for i in np.char_full_name(np.top_n(combined_counts, 0))])
G.add_edges_from([(i.title(), j.title()) for i,j in np.edge_maker(novel_sent_tagged, np.top_n(combined_counts, 0))])

np.drawGraph(G)