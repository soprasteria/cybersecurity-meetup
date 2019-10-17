# !/usr/bin/python3
# -*- coding: utf-8 -*-

import Orange
from Orange.data import Domain, Table,Instance, DiscreteVariable, ContinuousVariable, StringVariable

class DataSet:

    self.datatable=None

    def __init__(self):
        self.datatable=Table()

    def __init__(self,table):
        self.datatable=table
        self.processFeatures()

    @classmethod
    def from_numpy_array(cls,columns_titles,classes,np_array_features,np_array_classes):
        tmpdom = Orange.data.Domain(columns_titles + classes, False)
        features = np_array_features # N x M array of attributes
        classes = np_array_classes # N x L array of values for each class
        data = Orange.data.Table(tmpdom, np.concatenate((features, classes), axis=1))
        domain = Orange.data.Domain(columns_titles, False, class_vars=classes)
        return cls(Table(domain, data))

    @classmethod
    def from_tab_file(cls,file_path):
        return cls(Table(file_path))

    def processFeatures():
        pass
