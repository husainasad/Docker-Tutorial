#!/usr/bin/python2.7
#
# Interface for the assignement
#

import psycopg2
import os
import sys

def getOpenConnection(user='postgres', password='1234', dbname='postgres'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='172.17.0.2' password='" + password + "'")

def loadRatings(ratingstablename, ratingsfilepath, openconnection):

    cur = openconnection.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS {0} (userid int, t1 char, movieid int, t2 char, rating float, t3 char, t4 varchar, PRIMARY KEY(userid, movieid), CHECK(rating>=0 AND rating<=5))'.format(ratingstablename))

    # print('Table {} created'.format(ratingstablename))
    
    data_file = open(ratingsfilepath, 'r')
    cur.copy_from(data_file, ratingstablename, sep=':', columns = ('userid', 't1', 'movieid', 't2', 'rating', 't3', 't4'))

    # print('Data inserted into Table {}'.format(ratingstablename))

    cur.execute('ALTER TABLE {} DROP COLUMN t1, DROP COLUMN t2, DROP COLUMN t3, DROP COLUMN t4'.format(ratingstablename))

    cur.execute('CREATE TABLE Metadata (row_count int, range_partitions int, rr_partitions int)')
    cur.execute('INSERT INTO Metadata (SELECT COUNT(*), 0, 0 FROM {0})'.format(ratingstablename))

    # print('Metadata table created')
    
    openconnection.commit()

def rangePartition(ratingstablename, numberofpartitions, openconnection):

    cur = openconnection.cursor()
    interval = 5.0/numberofpartitions
    lowerBound = 0
    upperBound = interval

    cur.execute('CREATE TABLE range_part{0} AS SELECT * FROM {1} WHERE rating>={2} AND rating<={3}'.format(0, ratingstablename, lowerBound, upperBound))
    lowerBound = upperBound
    upperBound +=interval

    for i in range(1, numberofpartitions):
        cur.execute('CREATE TABLE range_part{0} AS SELECT * FROM {1} WHERE rating>{2} AND rating<={3}'.format(i, ratingstablename, lowerBound, upperBound))

        lowerBound = upperBound
        upperBound +=interval        

    # print('Range Partitions created')

    cur.execute('UPDATE Metadata SET range_partitions = {0}'.format(numberofpartitions))
    openconnection.commit()    

def roundRobinPartition(ratingstablename, numberofpartitions, openconnection):
    
    cur = openconnection.cursor()

    for i in range(0, numberofpartitions):
        cur.execute('CREATE TABLE rrobin_part{0} AS WITH T1 AS (SELECT *, row_number() OVER (ORDER BY userid, movieid) AS rownum FROM {1}) SELECT userid, movieid, rating FROM T1 WHERE (rownum-1)%{2} = {0} '.format(i, ratingstablename, numberofpartitions))
    
    # print('Round Robin Partitions created')

    cur.execute('UPDATE Metadata SET rr_partitions = {0}'.format(numberofpartitions))
    openconnection.commit()

def roundrobininsert(ratingstablename, userid, itemid, rating, openconnection):
    
    cur = openconnection.cursor()

    cur.execute('SELECT * FROM Metadata')
    data = cur.fetchall()[0]
    rows = data[0]
    partitions = data[2]

    row_insert = rows+1
    partition_insert = (row_insert-1)%partitions

    cur.execute('INSERT INTO rrobin_part{0} VALUES ({1},{2},{3})'.format(partition_insert, userid, itemid, rating))

    # print('Data inserted into round robin partition')

    cur.execute('UPDATE Metadata SET row_count={0}'.format(row_insert))
    
    openconnection.commit()

def rangeinsert(ratingstablename, userid, itemid, rating, openconnection):

    cur = openconnection.cursor()

    cur.execute('SELECT * FROM Metadata')
    data = cur.fetchall()[0]
    rows = data[0]
    partitions = data[1]

    interval = 5.0/partitions
    partition_insert = int((rating/interval))

    if(rating!=0 and rating==partition_insert*interval):
        partition_insert-=1

    cur.execute('INSERT INTO range_part{0} VALUES ({1},{2},{3})'.format(partition_insert, userid, itemid, rating))

    # print('Data inserted into range partition')

    cur.execute('UPDATE Metadata SET row_count={0}'.format(rows+1))
    
    openconnection.commit()

def createDB(dbname='dds_assignment'):
    """
    We create a DB by connecting to the default user and database of Postgres
    The function first checks if an existing database exists for a given name, else creates it.
    :return:None
    """
    # Connect to the default database
    con = getOpenConnection()
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    # Check if an existing database with the same name exists
    cur.execute('SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname=\'%s\'' % (dbname,))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute('CREATE DATABASE %s' % (dbname,))  # Create the database

    else:
        print ('A database named {0} already exists'.format(dbname))

    # Clean up
    cur.close()
    con.close()

def deletepartitionsandexit(openconnection):
    cur = openconnection.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    l = []
    for row in cur:
        l.append(row[0])
    for tablename in l:
        cur.execute("drop table if exists {0} CASCADE".format(tablename))

    cur.close()

def deleteTables(ratingstablename, openconnection):
    try:
        cursor = openconnection.cursor()
        if ratingstablename.upper() == 'ALL':
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            for table_name in tables:
                cursor.execute('DROP TABLE %s CASCADE' % (table_name[0]))
        else:
            cursor.execute('DROP TABLE %s CASCADE' % (ratingstablename))
        openconnection.commit()
    except psycopg2.DatabaseError, e:
        if openconnection:
            openconnection.rollback()
        print ('Error %s' % e)
    except IOError, e:
        if openconnection:
            openconnection.rollback()
        print ('Error %s' % e)
    finally:
        if cursor:
            cursor.close()