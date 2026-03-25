from neo4j import GraphDatabase

class Neo4jConnection:
    """Simple wrapper for local Neo4j connection"""
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="Badal123"):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            print("✅ Connected to Neo4j (local)")
        except Exception as e:
            print("❌ Cannot connect to Neo4j:", e)
            self.driver = None

    def run_query(self, query, params=None):
        if not self.driver:
            return None
        with self.driver.session() as session:
            return session.run(query, params or {})