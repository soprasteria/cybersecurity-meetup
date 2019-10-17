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

#######################################################
### Partie features SGC:
#######################################################
import pandas as pd
### Create dict from Pandas.dataframe where key is tuple ('USER','DOMAIN') and values the list of 'TIMESTAMPS':
### Generic
def pandas_dataframe_to_dict(df, field):
    usrdom_dict = {}
    field_index = list(df.keys()).index(field)
    for row in df.iterrows():
        l_aux = []
        user = row[1][0]
        domain = row[1][1]
        field = int(row[1][field_index])
        key = (user,domain)
        if key in usrdom_dict:
            l_aux = usrdom_dict[key]
        l_aux.append(field)
        usrdom_dict[key] = l_aux
    return usrdom_dict

def temp_byte_features(in_data):
    ### From Table into list convertible into Pandas
    user_list = []
    domain_list = []
    timestamp_list = []
    bytes_list = []
    #method_list = []
    #action_list = []
    #result_code_list = []
    #categories_list = []
    for index_d,data in enumerate(in_data):
        domain = url_split(str(data['URL']))[2]
        #data['DOMAIN'] = domain
        domain_list.append(domain)
        user_list.append(str(data['USER']))
        timestamp_list.append(data['TIMESTAMP'])
        bytes_list.append(data['BYTES'])
        #method_list.append(data['METHOD'])
        #action_list.append(data['ACTION'])
        #result_code_list.append(int(data['RESULT_CODE'])/100)
        #categories_list.append(data['CATEGORIES'])

    ### Conversion into Pandas for future display and eventual conversion into Table
    df = pd.DataFrame()
    df['USER'] = user_list
    df['DOMAIN'] = domain_list
    df['TIMESTAMP'] = timestamp_list
    df['BYTES'] = bytes_list
    #df['METHOD'] = method_list
    #df['ACTION'] = action_list
    #df['RESULT_CODE'] = result_code_list
    #df['CATEGORIES'] = categories_list
    sorted_df = df.sort_values(by=['TIMESTAMP'])

    ################################ MAIN #####################################
    d_usrdom_timestamp = {}
    d_usrdom_timestamp = pandas_dataframe_to_dict(df,'TIMESTAMP')
    d_usrdom_bytes = {}
    d_usrdom_bytes = pandas_dataframe_to_dict(df,'BYTES')
    #d_usrdom_method = {}
    #d_usrdom_method = pandas_dataframe_to_dict(df,'METHOD')
    #d_usrdom_action = {}
    #d_usrdom_action = pandas_dataframe_to_dict(df,'ACTION')
    #d_usrdom_resultcode = {}
    #d_usrdom_resultcode = pandas_dataframe_to_dict(df,'RESULT_CODE')

    ### TIMESTAMP RELATED ATTRIBUTES
    ### Attribute 1: dict of number of occurrences of couple 'USER'/'DOMAIN'
    ### Attributes 2-5: dict min, max, mean, median, std of delta distances between occurrences of couple 'USER'/'DOMAIN'
    ATTR_time_bytes = {}
    i = 0
    for usrdom in d_usrdom_timestamp.keys():
        l_deltas = []
        for i in range(len(d_usrdom_timestamp[usrdom])):
            try:
                delta = d_usrdom_timestamp[usrdom][i+1] - d_usrdom_timestamp[usrdom][i]
            except:
                delta = 0
            l_deltas.append(delta)
        ATTR_time_bytes[usrdom] = [pseudo_hash(user_list[i]),pseudo_hash(domain_list[i]),len(d_usrdom_timestamp[usrdom]),numpy.min(l_deltas), numpy.max(l_deltas), numpy.mean(l_deltas), numpy.median(l_deltas), numpy.std(l_deltas),numpy.min(d_usrdom_bytes[usrdom]), numpy.max(d_usrdom_bytes[usrdom]), numpy.mean(d_usrdom_bytes[usrdom]), numpy.median(d_usrdom_bytes[usrdom]), numpy.std(d_usrdom_bytes[usrdom])]
        i += 1


    ### From dict to numpy array
    arr_time_bytes = numpy.empty((0,13), float)
    for key in ATTR_time_bytes.keys():
        arr_time_bytes = numpy.vstack((arr_time_bytes,numpy.array(ATTR_time_bytes[key])))

    new_domain = Domain([DiscreteVariable('USER'),DiscreteVariable('DOMAIN'),ContinuousVariable('OCCURRENCES'),ContinuousVariable('MIN_DELTA'),ContinuousVariable('MAX_DELTA'),ContinuousVariable('MEAN_DELTA'),ContinuousVariable('MEDIAN_DELTA'),ContinuousVariable('STD_DELTA'),ContinuousVariable('MIN_BYTES'),ContinuousVariable('MAX_BYTES'),ContinuousVariable('MEAN_BYTES'),ContinuousVariable('MEDIAN_BYTES'),ContinuousVariable('STD_BYTES')])
    #print (("Numbers of rows %s")%(len(in_data)))
    new_table=Table(new_domain,arr_time_bytes.tolist())
          
    return new_table

#arr_time_bytes = temp_byte_features(in_data)
#print (arr_time_bytes)


### DICRETE 'METHOD', 'ACTION', 'RESULT_CODE' RELATED ATTRIBUTES
### Kind of dummify values with nb occurrences: standard function
### TO DO

#MAIN Orange doesn't support magic word __main__
#out_data=generateFeatures(in_data)
#print(url_vector('http://www.example.co.uk:80/search?q=term&lang=en#results'))
