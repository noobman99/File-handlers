# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 19:13:33 2021
Title: module for csv text reading,writing
@author: hp
"""


class File():
    def __init__(self, filename):
        self.__file = filename
        self.val = []
        with open(filename, "r") as f:
            self.keys = list(i.strip() for i in f.readline().split(","))
            for i in f.readlines():
                self.val.append(dict(zip(self.keys, map((lambda _: _.strip() if _ != "" else None), i.split(",")))))

    def append(self, *updict):
        with open(self.__file, "a") as f:
            for dic in updict:
                string = tuple(map((lambda key: dic[key] if key in dic.keys() else ""), self.keys))
                f.write(",".join(string)+"\n")
                for i in set(self.keys)-set(dic.keys()):
                    dic[i] = None
                self.val.append(dict(dic))

    def get_val(self):
        return self.val

    def clear(self):
        with open(self.__file, "w") as f:
            f.write(",".join(self.keys)+"\n")
        self.val = []

    def del_rec(self, rec, atr=None):
        with open(self.__file, "w") as f:
            if atr:
                f.write(",".join(self.keys)+"\n")
                for dic in list(self.val):
                    if rec == dic[atr]:
                        self.val.remove(dic)
                    else:
                        string = list(map((lambda key: dic[key] if key in dic.keys() else ""), self.keys))
                        f.write(",".join(string)+"\n")
            else:
                self.val.remove(rec)
                f.write(",".join(self.keys)+"\n")
                for dic in self.val:
                    string = list(map((lambda key: dic[key] if key in dic.keys() else ""), self.keys))
                    f.write(",".join(string)+"\n")
