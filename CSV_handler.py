# -*- coding: utf-8 -*-
"""
Title: module for csv file reading,writing
"""

from typing import Dict, List

class File():

    def __init__(self, filename: str, delimiter: str = ","):
        """ Import a csv file object as a pythonic list """
        self.__file = filename
        self._delimiter = delimiter
        self.val = []
        with open(filename, "r") as f:
            self.keys = list(i.strip() for i in f.readline().split(self._delimiter))
            for i in f.readlines():
                self.val.append(dict(zip(self.keys, map((lambda val: val.strip() if val != "" else None), i.split(self._delimiter)))))

    def append(self, *updict: List[Dict]):
        """ Add records into the file
        the records to be added must be passed as a dictionary/dictionaries with keys same as that in the csv file """
        with open(self.__file, "a") as f:
            for dic in updict:
                string = tuple(map((lambda key: dic[key] if key in dic.keys() else ""), self.keys))
                f.write(self._delimiter.join(string)+"\n")
                for i in set(self.keys)-set(dic.keys()):
                    dic[i] = None
                self.val.append(dict(dic))

    def get_val(self):
        """ Get the values of the file in form of list of dictionary of records """
        return self.val

    def get_keys(self):
        """ get keys in the corresponding file object """
        return self.keys

    def clear(self):
        """ Delete all the records in the file. Only the keys will remains. """
        with open(self.__file, "w") as f:
            f.write(self._delimiter.join(self.keys)+"\n")
        self.val = []

    def del_rec(self, rec, atr=None):
        """ delete a specified record """
        with open(self.__file, "w") as f:
            if atr:
                f.write(self._delimiter.join(self.keys)+"\n")
                for dic in list(self.val):
                    if rec == dic[atr]:
                        self.val.remove(dic)
                    else:
                        string = list(map((lambda key: dic[key] if key in dic.keys() else ""), self.keys))
                        f.write(self._delimiter.join(string)+"\n")
            else:
                self.val.remove(rec)
                f.write(self._delimiter.join(self.keys)+"\n")
                for dic in self.val:
                    string = list(map((lambda key: dic[key] if key in dic.keys() else ""), self.keys))
                    f.write(self._delimiter.join(string)+"\n")

    def __call__(self):
        return self.val

    def __str__(self):
        return str(self.val)

    def __iter__(self):
        for i in self.val:
            yield i

    def __len__(self):
        return len(self.val)

    def __bool__(self):
        return bool(self.val)

    def __contains__(self, value):
        return any(True for i in self.val if i == value)

    def refresh(self):
        """ Refresh the Values during run time to accomodate for the changes done from other programs """
        self.__init__(self.__file, delimiter=self._delimiter)
