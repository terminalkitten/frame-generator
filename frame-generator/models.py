#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Frame Generator
#
# Copyright (C) 2016 Juliette Lonij, Koninklijke Bibliotheek -
# National Library of the Netherlands
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import gensim
import os
import unicodecsv as csv


class TopicList(object):
    '''
    List of generated topics.
    '''

    def __init__(self, doc_reader, num_topics=10, num_words=10,
            mallet_path=None):
        '''
        Set TopicList attributes.
        '''
        self.doc_reader = doc_reader
        self.num_topics = num_topics
        self.num_words = num_words
        self.mallet_path = mallet_path

        if mallet_path:
            print('Generating Mallet LDA model ...')
            lda = gensim.models.wrappers.LdaMallet(mallet_path,
                    num_topics=num_topics, corpus=self.doc_reader.corpus,
                    id2word=self.doc_reader.dictionary, workers=2)
        else:
            print('Generating Gensim LDA model ...')
            lda = gensim.models.LdaModel(corpus=self.doc_reader.corpus,
                    id2word=self.doc_reader.dictionary, num_topics=num_topics,
                    alpha='auto', chunksize=1, eval_every=1)

        topics = [t[1] for t in lda.show_topics(num_words=num_words,
            num_topics=num_topics, formatted=False)]
        self.topics = [[(i[1], i[0]) for i in t] for t in topics]

    def save_topics(self, dir_name):
        '''
        Save generated topics to file.
        '''
        with open(dir_name + os.sep + 'topics' + '.csv', 'wb') as f:
            # Manually encode a BOM, utf-8-sig didn't work with unicodecsv
            f.write(u'\ufeff'.encode('utf8'))
            csv_writer = csv.writer(f, delimiter='\t', encoding='utf-8')
            for topic in self.topics:
                csv_writer.writerow([t[1] for t in topic])
                csv_writer.writerow([str(t[0]) for t in topic])

    def print_topics(self):
        '''
        Print generated topics.
        '''
        print('Topics generated:')
        for i, topic in enumerate(self.topics):
            print('[' + str(i + 1) + '] ' + ', '.join([t[1] for t in topic]))


class TfIdfList(object):
    '''
    List of tf-idf scores.
    '''

    def __init__(self, doc_reader):
        '''
        Set TfIdfList attributes.
        '''
        self.doc_reader = doc_reader

        print('Generating Gensim TF-IDF model ...')
        tfidf = gensim.models.TfidfModel(self.doc_reader.corpus)
        self.scores = tfidf[self.doc_reader.corpus]
