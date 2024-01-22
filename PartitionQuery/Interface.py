#!/usr/bin/python2.7
#
# Assignment2 Interface
#

import psycopg2
import os
import sys
# Donot close the connection inside this file i.e. do not perform openconnection.close()
def RangeQuery(ratingsTableName, ratingMinValue, ratingMaxValue, openconnection):
    cur = openconnection.cursor()

    result_list = []

    cur.execute('SELECT partitionnum FROM RoundRobinRatingsMetadata')
    rr_partitions = cur.fetchone()[0]

    for pnum in range(rr_partitions):
        rr_tableName = 'RoundRobinRatingsPart{0}'.format(pnum)
        cur.execute('SELECT * FROM {0} WHERE Rating BETWEEN {1} AND {2}'.format(rr_tableName, ratingMinValue, ratingMaxValue))
        rr_data_list = cur.fetchall()
        if len(rr_data_list)>0:
            for i in range(len(rr_data_list)):
                result_list.append((rr_tableName,) + rr_data_list[i])

    range_partitions = [(0,)]

    if(ratingMaxValue!=0):
        cur.execute('SELECT partitionnum FROM RangeRatingsMetadata WHERE {0}<=maxrating AND {1}>minrating'.format(ratingMinValue, ratingMaxValue))
        range_partitions = cur.fetchall()

    for rp in range_partitions:
        range_tableName = 'RangeRatingsPart{0}'.format(rp[0])
        cur.execute('SELECT * FROM {0} WHERE Rating BETWEEN {1} AND {2}'.format(range_tableName, ratingMinValue, ratingMaxValue))
        range_data_list = cur.fetchall()
        if len(range_data_list)>0:
            for i in range(len(range_data_list)):
                result_list.append((range_tableName,) + range_data_list[i])

    writeToFile('/app/RangeQuery.txt', result_list)

def PointQuery(ratingsTableName, ratingValue, openconnection):
    cur = openconnection.cursor()

    result_list = []
    
    cur.execute('SELECT partitionnum FROM RoundRobinRatingsMetadata')
    rr_partitions = cur.fetchone()[0]
    
    for pnum in range(rr_partitions):
        rr_tableName = 'RoundRobinRatingsPart{0}'.format(pnum)
        cur.execute('SELECT * FROM {0} WHERE Rating={1}'.format(rr_tableName, ratingValue))
        rr_data_list = cur.fetchall()
        if len(rr_data_list)>0:
            for i in range(len(rr_data_list)):
                result_list.append((rr_tableName,) + rr_data_list[i])

    good_partition = 0

    if(ratingValue!=0):
        cur.execute('SELECT partitionnum FROM RangeRatingsMetadata WHERE {0}>minrating AND {0}<=maxrating'.format(ratingValue))
        good_partition = cur.fetchone()[0]

    range_tableName = 'RangeRatingsPart{0}'.format(good_partition)
    cur.execute('SELECT * FROM {0} WHERE Rating={1}'.format(range_tableName, ratingValue))
    range_data_list = cur.fetchall()
    if len(range_data_list)>0:
        for i in range(len(range_data_list)):
            result_list.append((range_tableName,) + range_data_list[i])
        
    writeToFile('/app/PointQuery.txt', result_list)

def writeToFile(filename, rows):
    f = open(filename, 'w')
    for line in rows:
        f.write(','.join(str(s) for s in line))
        f.write('\n')
    f.close()