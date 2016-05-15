#!/usr/bin/python
#-*- coding: utf-8 -*-

from multiprocessing import Pool
from jianshuFrontPage import get_front_page
from jianshupassages import get_passages
from jianshuAuthor import get_author
if __name__ == '__main__':
    pool = Pool()
    results = pool.map(get_passages,range(20000,26991))
