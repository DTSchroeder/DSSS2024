# DSSS2024
## Data Science International Summer School 2024: Graph Data Analytics

## Graph Data Analytics with NetworkX and Neo4j

This hands-on tutorial guides you through the exciting world of graph data analytics using the powerful combination of NetworkX (for analysis) and Neo4j (as a graph database). You'll learn how to connect to Neo4j, import and model graph data, analyze graph structures, perform essential calculations, and visualize your findings using the popular Game of Thrones dataset as a case study.

### Prerequisites and Environment Setup

You'll need the following:

- **Python 3.6 or higher:** The backbone of our analysis. Download it from [python.org](https://www.python.org/).
- **Neo4j Desktop 1.5.9:** Our graph database environment. Download it from [neo4j.com](https://neo4j.com/download/). 
- **Database Version:** Neo4j 5.12.0
- **Plugins:** APOC 5.12.0 and Graph Data Science Library 2.6.8. These should be installed in your Neo4j instance. (Instructions for plugin installation will be provided later in the tutorial.)

### Setup Instructions: Let's Get Started!

1. **Create a Virtual Environment (Highly Recommended):**
   - Open your terminal and navigate to the directory where you've cloned this project.
   - Create a virtual environment:
     ```bash
     python3 -m venv myenv
     ```
   - Activate the environment:
     ```bash
     source myenv/bin/activate  # Linux/macOS
     myenv\Scripts\activate      # Windows
     ```

2. **Install Dependencies:**
   - With your virtual environment activated, install the required libraries:
     ```bash
     pip install -r requirements.txt
     ```
     This will install NetworkX, the Neo4j Python driver, Jupyter Notebooks, and any visualization libraries you've specified.

3. **Launch Neo4j Desktop:**
   - Double-click the Neo4j Desktop icon to open the application.

4. **Create a New Project:**
   - In Neo4j Desktop, click on "New Project."
   - Name your project "Data Science Summer School 2024" and click "Create."

5. **Create a New DBMS (Database Management System):**
   - In your new project, click on "New DBMS."
   - Name it "Graph Data Analytics" and select the **Neo4j version 5.12.0**.
   - Click "Create" to set up the DBMS.

6. **Create a Game of Thrones Database:**
   - Under the "Graph Data Analytics" DBMS, click on "New Database."
   - Name it "GoT" and click "Create."
   - Once created, click "Start" to activate the database.
   - In these tutorial we will use the (default) username "neo4j" and the password "your_password".

7. **Open Neo4j Browser:**
   - Click on the "Open" button next to your new "GoT" database. This will launch the Neo4j Browser, where you'll run Cypher queries to import and explore your graph data.

8. **Import the Game of Thrones Dataset:**
   - Copy and paste the following Cypher commands into the Neo4j Browser one by one:

   ```cypher
    CREATE CONSTRAINT FOR (c:Character) REQUIRE c.name IS UNIQUE;  // Ensure unique character names

   LOAD CSV WITH HEADERS FROM '[https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/asoiaf-book1-edges.csv](https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/asoiaf-book1-edges.csv)' AS row
       MERGE (src:Character {name: row.Source})
       MERGE (tgt:Character {name: row.Target})
       MERGE (src)-[r:INTERACTS1]->(tgt)
       ON CREATE SET r.weight = toInteger(row.weight), r.book=1;

   LOAD CSV WITH HEADERS FROM '[https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/asoiaf-book2-edges.csv](https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/asoiaf-book2-edges.csv)' AS row
       MERGE (src:Character {name: row.Source})
       MERGE (tgt:Character {name: row.Target})
       MERGE (src)-[r:INTERACTS2]->(tgt)
       ON CREATE SET r.weight = toInteger(row.weight), r.book=2;

   LOAD CSV WITH HEADERS FROM '[https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/asoiaf-book3-edges.csv](https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/asoiaf-book3-edges.csv)' AS row
       MERGE (src:Character {name: row.Source})
       MERGE (tgt:Character {name: row.Target})
       MERGE (src)-[r:INTERACTS3]->(tgt)
       ON CREATE SET r.weight = toInteger(row.weight), r.book=3;

   LOAD CSV WITH HEADERS FROM '[https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/asoiaf-book45-edges.csv](https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/asoiaf-book45-edges.csv)' AS row
       MERGE (src:Character {name: row.Source})
       MERGE (tgt:Character {name: row.Target})
       MERGE (src)-[r:INTERACTS45]->(tgt)
       ON CREATE SET r.weight = toInteger(row.weight), r.book=45;


9. **Verify Data Import:**
   ```cypher
   MATCH (n)
   RETURN COUNT(n) AS nodeCount; //796