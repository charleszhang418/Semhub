import mysql.connector

class Connector:
    instance: mysql.connector.MySQLConnection = None

    def __init__(self):
        pass

    def getConnectorInstance():
        if Connector.instance:
            return Connector.instance
        
        Connector.instance = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="semhub"
        )

        return Connector.instance

