import mysql.connector
from mysql.connector import Error
from tkinter import ttk, messagebox

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="cognitivereaction.mysql.database.azure.com",
            port=3306,
            user="Ambrose",
            password="NEUyang7034",
            database="cognitive_reaction"
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
        return None
