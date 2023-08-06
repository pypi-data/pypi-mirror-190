# -*- coding: utf-8 -*-
"""
Created on: 2018/12/21 14:29

@author: yd
@file: mysql_connector.py 
"""


import pymysql
import traceback
import threading
import numpy as np


class mysql_db():
    def __init__(self):
        self.host = ''
        self.port = ''
        self.user = ''
        self.passwd = ''
        self.db = ''
        self.charset = ''
        self.reconnect_count = 0
        self.lock = threading.Lock()
        # decode numpy.float64
        pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
        pymysql.converters.conversions = pymysql.converters.encoders.copy()
        pymysql.converters.conversions.update(pymysql.converters.decoders)
        self.connect = self.getConnect()

    def reset_count(self):
        with self.lock:
            self.reconnect_count = 0

    def add_count(self):
        with self.lock:
            self.reconnect_count += 1

    def get_count(self):
        with self.lock:
            count = self.reconnect_count
        return count
    
    def getConnect(self):
        self.host = "123.60.31.90"
        self.port = 3307
        self.user = "basisreader"
        self.passwd = "gtja@123"
        self.db = "qhadmin"
        self.charset = 'utf8'
        connect = pymysql.Connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            charset=self.charset
        )
        connect.autocommit(1)
        return connect

    def query(self, sqlstr):
        try:
            dbc = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
            dbc.execute(sqlstr)
            msg = dbc.fetchall()
            dbc.close()
            self.reset_count()
            return msg
        except Exception as e:
            traceback.print_exc()
            self.connect.close()
            self.connect = self.getConnect()
            if self.get_count() >= 3:
                raise e
            self.add_count()
            return self.query(sqlstr)

    def query_1b1(self, sqlstr, func):
        dbc = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
        num = dbc.execute(sqlstr)
        for _ in range(num):
            func(dbc.fetchone())
        dbc.close()

    def exec(self, query):
        try:
            dbc = self.connect.cursor()
            msg = dbc.execute(query)
            dbc.close()
            self.reset_count()
            return msg
        except Exception as e:
            traceback.print_exc()
            self.connect.close()
            self.connect = self.getConnect()
            if self.get_count() < 3:
                self.add_count()
                return self.exec(query)
            else:
                raise e

    def execmany(self, query, value_ls):
        try:
            dbc = self.connect.cursor()
            msg = dbc.executemany(query, value_ls)
            dbc.close()
            self.reset_count()
            return msg
        except Exception as e:
            traceback.print_exc()
            self.connect.close()
            self.connect = self.getConnect()
            if self.get_count() < 3:
                self.add_count()
                return self.execmany(query, value_ls)
            else:
                raise e

    def close(self):
        try:
            self.connect.close()
        except Exception:
            pass





