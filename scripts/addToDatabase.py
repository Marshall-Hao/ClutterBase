#!/usr/bin/env python

import argparse
from ClutterBase import Connection

def add_mesh(database : str, name : str , mesh_data : str, mesh_type : str, front : str, side : str,top : str,persp : str) :
    print("add to db")
    with Connection.Connection(database) as connection :
        connection.add_item(name,mesh_data,mesh_type,front,side,top,persp)

if __name__ == "__main__" :
    parser=argparse.ArgumentParser(description="add mesh to database")
    parser.add_argument("--mesh","-m",help="mesh file to add", required=True)
    parser.add_argument("--name","-n",help="name to add", required=True)
    parser.add_argument("--type","-t",help="mesh type loaded",required=True)
    parser.add_argument("--database","-db",help="which Db to add to",required=True)
    parser.add_argument("--top","-T",help="top image",default="")
    parser.add_argument("--side","-S",help="side image",default="")
    parser.add_argument("--front","-F",help="front image",default="")
    parser.add_argument("--persp","-P",help="persp image",default="")
    
    args=parser.parse_args()
    
    add_mesh(args.database,args.name,args.mesh,args.type,args.front,args.side,args.top,args.persp)