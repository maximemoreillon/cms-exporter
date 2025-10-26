from neo4j import GraphDatabase
from os import getenv
from dotenv import load_dotenv

load_dotenv()

uri = getenv("NEO4J_URI")
username = getenv("NEO4J_USERNAME")
password = getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(username, password))
