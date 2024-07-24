from neo4j import GraphDatabase
import networkx as nx
import os


class Neo4jConnection:
    """
    A singleton class representing a connection to a Neo4j database.

    This class provides methods to establish a connection, run Cypher queries,
    and verify the connection status.

    Usage:
        connection = Neo4jConnection.get_instance()
        connection.run_query("MATCH (n) RETURN n")
        connection.close()
    """

    __instance = None  # Private class variable to store the single instance

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Neo4jConnection.__instance is None:
            Neo4jConnection()  # Create the instance if it doesn't exist
        return Neo4jConnection.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Neo4jConnection.__instance is not None:
            raise Exception(
                "This class is a singleton! Use get_instance() instead.")
        else:
            Neo4jConnection.__instance = self

            # Connection details (Replace with your actual credentials)
            self.uri = "bolt://localhost:7687"
            self.username = "neo4j"
            self.password = os.environ.get("NEO4J_PASSWORD", "password")

            # Establish the connection
            self.driver = GraphDatabase.driver(
                self.uri, auth=(self.username, self.password))

    def close(self):
        """ Close the database connection. """
        if self.driver:
            self.driver.close()
            Neo4jConnection.__instance = None  # Reset the instance when closing

    def run_query(self, query, parameters=None):
        """ Run a Cypher query with optional parameters. """
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return result.data()  # Return query results as a list of dictionaries

    def verify_connection(self):
        """ Verify that the connection is active. """
        try:
            query = "MATCH (n) RETURN count(n) AS count"
            result = self.run_query(query)
            return result[0]["count"] == 796  # Check if 796 nodes are present
        except Exception as e:
            print(f"Connection verification failed: {e}")
            return False

    def count_movie_characters(self):
        """ Return the count of movie characters. """
        query = "MATCH (c:Character) RETURN count(c) AS count"
        result = self.run_query(query)
        return result[0]["count"] if result else 0

    def count_interactions_by_book(self):
        """ Return the count of interactions by book. """
        query = "MATCH ()-[r]->() RETURN r.book as book, count(r) as interaction_count ORDER BY book"
        return self.run_query(query)

    def count_interactions(self):
        """ Return the count of interactions. """
        query = "MATCH ()-[r]->() RETURN count(r) as count"
        result = self.run_query(query)
        return result[0]["count"] if result else 0

    def calculate_network_summary_statistics(self):
        """ Calculate network summary statistics. """
        query = "MATCH (c:Character)-->() WITH c, count(*) AS num " \
                "RETURN min(num) AS min, max(num) AS max, avg(num) AS avg_characters, stdev(num) AS stdev"
        result = self.run_query(query)
        return result[0] if result else None

    def calculate_network_summary_statistics_by_book(self):
        """ Calculate network summary statistics by Book. """
        query = "MATCH (c:Character)-[r]->() " \
                "WITH r.book as book, c, count(*) AS num " \
                "RETURN book, min(num) AS min, max(num) AS max, avg(num) AS avg_characters, stdev(num) AS stdev " \
                "ORDER BY book"
        return self.run_query(query)

    def load_data_into_networkx(self):
        """ Load data from Neo4j into a NetworkX graph. """
        # Query to retrieve all nodes and relationships
        query = """
        MATCH (n)
        WITH collect(n) AS nodes
        MATCH ()-[r]->()
        RETURN nodes, collect(r) AS relationships
        """

        with self.driver.session() as session:
            result = session.run(query)

            # Create a new NetworkX graph
            graph = nx.Graph()

            # Add nodes to the graph
            for record in result:
                for node in record["nodes"]:
                    graph.add_node(node["name"])

                # Add relationships to the graph
                for rel in record["relationships"]:
                    graph.add_edge(
                        rel.start_node["name"], rel.end_node["name"], weight=rel["weight"])

            return graph

    def print_community_sizes(self, communities):
        """ Print the sizes of the communities. """
        # Calculate the sizes of the detected communities and create a list of (community_index, size) tuples
        community_sizes = [(idx, len(community))
                           for idx, community in enumerate(communities)]

        # Sort the list of community sizes by size in descending order
        sorted_community_sizes = sorted(
            community_sizes, key=lambda x: x[1], reverse=True)

        print(f"Number of communities: {len(communities)}")
        for idx, size in sorted_community_sizes:
            print(f"Community {idx + 1}: {size} nodes")

    def subgraph_largest_community(self):
        """ Return the subgraph of the largest community. """
        # Load the data into a NetworkX graph
        graph = self.load_data_into_networkx()

        # Detect communities using the Louvain method
        communities = list(nx.algorithms.community.louvain_communities(graph))

        # Find the largest community
        largest_community = max(communities, key=len)

        # Create a subgraph of the largest community
        subgraph = graph.subgraph(largest_community)

        return subgraph

    # TODO ADD SUBGRAPHS
