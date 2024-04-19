import sqlite3
from sqlite3 import Error
class Connection :
    """
    Parameters :
        name : str the name of the db connection
    """
    def __init__(self,name : str) :
        self.name = name
        self.connection = None
    
    def open(self) :
        try :
            self.connection = sqlite3.connect(self.name)
        except Error as e :
            print(f"error {e} with database {self.name}")

    def close(self) :
        self.connection.close()
    
    def __enter__(self) :
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb) :
        self.close()

    def add_item(self,name : str, mesh : str, type, front : str="", side : str="", top : str="", persp : str="" ) :
        print("adding to db")
        cursor = self.connection.cursor()
        if len(front) >0 and len(side) > 0 and len(persp) > 0 and len(top) > 0 : # if we have an image
            query  ="""INSERT into Meshes (name,mesh_data,mesh_type,front_image,side_image,top_image,persp_image) VALUES(?,?,?,?,?,?,?)"""
            mesh_blob=self._loadBlob(mesh)
            front_image=self._loadBlob(front)
            side_image=self._loadBlob(side)
            top_image=self._loadBlob(top)
            persp_image=self._loadBlob(persp)
            query_data =(name,mesh_blob,type,front_image,side_image,top_image,persp_image)
            cursor.execute(query,query_data)

        else :
            query = """INSERT into Meshes (name,mesh_data,mesh_type) VALUES(?,?,?)"""
            mesh_blob=self._loadBlob(mesh)
            query_data =(name,mesh_blob,type)
            cursor.execute(query,query_data)

        cursor.connection.commit()
        cursor.connection.close()


    def _loadBlob(self,name : str) :
        with open(name,'rb') as file :
            blob_data = file.read()
        return blob_data




