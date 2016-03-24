#Data management - database setup and data entry
#Two functions - one inits a database, one writes a new entry to it
#Writing this as either a module that can be imported or a main method to run
import sqlite3 as sql
import os, sys
from graph_tool.all import *
import pickle

#Initialize - run iff database doesn't exist already!
def initDatabase(filename):
    conn = sql.connect(filename)
    db = conn.cursor()

    queryTable1 = """CREATE TABLE graphData (
        GraphID INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
        SampleID TEXT NOT NULL,
        LeafID TEXT NOT NULL,
        ImageFile TEXT,
        Points BLOB,
        Scale REAL,
        Graph BLOB
        ) """

    queryTable2 = """CREATE TABLE leafData (
        LeafID TEXT PRIMARY KEY NOT NULL,
        PlantID TEXT NOT NULL,

        )"""

    queryTable3 = """CREATE TABLE plantData(
        PlantID TEXT PRIMARY KEY NOT NULL,
        Genus TEXT,
        Species TEXT,
        Source TEXT,
        )"""

    queryTableMeta = """CREATE TABLE metadata (
        Field TEXT,
        Units TEXT,
        Description TEXT
        )"""

    db.execute(queryTable1)
    db.execute(queryTable2)

    db.execute(queryTableMeta)

    conn.commit()
    conn.close()

def getID(imageFile,filename="ThesisData.db"):
    conn = sql.connect(filename)
    db = conn.cursor()
    db.execute("SELECT GraphID FROM graphData WHERE ImageFile = ?",imageFile)
    value = db.fetchall()
    conn.commit()
    conn.close()

def savePoints(graphID,points,filename="ThesisData.db"):
    pointBin = pickle.dumps(points)
    conn = sql.connect(filename)
    db = conn.cursor()
    db.execute("UPDATE graphData SET Points = ? WHERE GraphID = ?",(pointBin,graphID))
    conn.commit()
    conn.close()

def saveGraph(graphID,graph):
    graphBin = pickle.dumps(graph)
    conn = sql.connect(filename)
    db = conn.cursor()
    db.execute("UPDATE graphData SET Graph = ? WHERE GraphID = ?",(graphBin,graphID))
    conn.commit()
    conn.close()

#Main - actually initialize - run me once!
if __name__ == "__main__":
    wd = "/home/jen/Documents/School/GradSchool/Thesis/Code/"
    os.setwd(wd)
    filename = "ThesisData.db"
    if filename not in os.listdir():
        initDatabase(filename)
