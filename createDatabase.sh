#!/usr/bin/env bash

echo "Genereating test clutterbase"

sql="DROP TABLE IF EXISTS Meshes;
Create table Meshes (
        id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL,
        mesh_data BLOB NOT NULL,
        mesh_type TEXT CHECK(mesh_type IN('obj','usd','fbx')),
        front_image BLOB,
        side_image BLOB,
        top_image BLOB,
        persp_image BLOB
);"

echo $sql | sqlite3 ClutterTest.db

./scripts/addToDatabase.py -m assets/Cube.obj -n "TestCube" -t "obj" -db ClutterTest.db
./scripts/addToDatabase.py -m assets/Cube.usd -n "TestCubeUSD" -t "usd" -db ClutterTest.db
./scripts/addToDatabase.py -m assets/Cube.fbx -n "TestCubeFBA" -t "fbx" -db ClutterTest.db
./scripts/addToDatabase.py -m assets/gear.obj -n "gear" -t "obj" -db ClutterTest.db -F assets/gearFront.png -S assets/gearSide.png -T assets/gearTop.png -P assets/gearPersp.png