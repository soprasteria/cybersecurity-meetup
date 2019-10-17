#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Sopra Steria All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

import Orange
from Orange.data import Domain, Table,Instance, DiscreteVariable, ContinuousVariable, StringVariable, TimeVariable
import hashlib
import re
import math
import numpy
import datetime

def url_vector(url):
    #URL to Vector
    url_exploded=url_split(url)
    url_vector=[0]*len(url_exploded)
    for index_v,value in enumerate(url_exploded):
        if value == '':
            url_vector[index_v]=1
        else:
            url_vector[index_v]=pseudo_hash(value)
    return url_vector

def url_split(url):
    #URL Split
    #url_splitter=re.compile(r'^(?:(.*?):\/\/?)?\/?(?:[^\/\.]+\.)*?([^\/\.]+)\.?([^\/]*)(?:([^?]*)?(?:\?(‌​[^#]*))?)?(.*)?')
    #url_explode=url_splitter.split(url)
    #protocol,subdomain,domain,tld,path,parameters,anchros
    url_explode=['']*7

    try:
        url.index('://')
        #proto,rest
        url_remaining=url.split('://',1)
        #protocol
        url_explode[0]=url_remaining.pop(0)
    except (ValueError, IndexError):
        url_remaining=[url]

    try:
        url_remaining[0].index('/')
        #domain,rest
        url_remaining=url_remaining[0].split('/',1)
        #domain
        url_explode[2]=url_remaining.pop(0)
        if(url_explode[2].count('.')>1):
            #subdomain,domain
            url_domain_remaining=url_explode[2].split('.',1)
            #subdomain
            url_explode[1]=url_domain_remaining.pop(0)
            #domain
            url_explode[2]=url_domain_remaining[0]
            #domain,tld
            url_domain_remaining=url_domain_remaining[0].rsplit('.',1)
            url_domain_remaining.pop(0)
            #tld
            url_explode[3]=url_domain_remaining.pop(0)
        elif(url_explode[2].count('.')==1):
            #domain,tld
            url_domain_remaining=url_explode[2].split('.',1)
            #tld
            url_explode[3]=url_domain_remaining.pop(1)
    except (ValueError, IndexError):
        try:
            #domain
            url_explode[2]=url_remaining.pop(0)
        except (ValueError, IndexError):
            pass

    try:
        url_remaining[0].index('?')
        #path,parameters
        url_remaining=url_remaining[0].split('?',1)
        #path
        url_explode[4]=url_remaining.pop(0)
    except (ValueError, IndexError):
        try:
            #path
            url_explode[4]=url_remaining.pop(0)
        except (ValueError, IndexError):
            pass

    try:
        url_remaining[0].index('#')
        #parameters,anchors
        url_remaining=url_remaining[0].split('#',1)
        #parameters
        url_explode[5]=url_remaining.pop(0)
        #anchors
        url_explode[6]=url_remaining.pop(0)
    except (ValueError, IndexError):
        try:
            #parameters
            url_explode[5]=url_remaining.pop(0)
        except (ValueError, IndexError):
            pass
    return url_explode

def pseudo_hash(word):
    #Word to Number
    #simple character convertion
    # 1 invert char order [::-1]
    # 2 convert char to number ord(c)
    # 3 convert number to string str()
    # 4 accolate numbers representating char in a string "".join
    # 5 convert aggregated string to int int()
    #hash=int("".join([str(ord(c)) for c in str(word)[::-1]]))
    hasharray=[ord(c) for c in str(word)]
    hash=float(0)
    maxlen=len(hasharray)
    for index_n,n in enumerate(hasharray):
        coeff=(index_n+1)/maxlen
        #better outlying
        #f(n)=index_n*n**(index_n/len(index))
        hash=hash+(index_n*(n**coeff))
        #worst outlying hash=hash+n**coeff


    #sha256 convertion
    #hasher=hashlib.sha256()
    #hasher.update(str(word).encode('utf-8', 'xmlcharrefreplace'))
    #hash=int(hasher.hexdigest(),base=16)
    return hash

def generateFeatures(in_data):
    new_domain = Domain(['TIMESTAMP','BYTES',TimeVariable('DATETIME'),ContinuousVariable('FEAT_URL_0'), ContinuousVariable('FEAT_URL_1'), ContinuousVariable('FEAT_URL_2'), ContinuousVariable('FEAT_URL_3'), ContinuousVariable('FEAT_URL_4'), ContinuousVariable('FEAT_URL_5'), ContinuousVariable('FEAT_URL_6'),ContinuousVariable('FEAT_USER_1'),ContinuousVariable('FEAT_USER_AGENT_1'),ContinuousVariable('FEAT_CATEGORIES_1')],class_vars=in_data.domain.class_var,metas=in_data.domain.metas,source=in_data.domain)
    new_table=Table(new_domain,in_data)
    #print (("Numbers of rows %s")%(len(in_data)))
    
    for index_d,data in enumerate(new_table):
        for index_v,value in enumerate(url_vector(str(data['URL']))):
            data['FEAT_URL_'+str(index_v)]=value
        data['DATETIME']=datetime.datetime.fromtimestamp(data['TIMESTAMP']).strftime('%Y-%m-%d %H:%M:%S')
        data['DOMAIN']=url_split(str(data['URL']))[2]
        data['FEAT_USER_1']=pseudo_hash(data['USER'])
        data['FEAT_USER_AGENT_1']=pseudo_hash(data['USER_AGENT'])
        data['FEAT_CATEGORIES_1']=pseudo_hash(data['CATEGORIES'])
    return new_table

#MAIN Orange doesn't support magic word __main__
#in_data = Table("file.tab")
#out_data=generateFeatures(in_data)

