# Group Project: DAM -  Uncovering Football Insights: Advanced match analytics with Cypher

## Installation Guide

### 1. Install Required Dependencies
In terminal, change directory to the main folder, then run the following command:
```bash
pip install -r requirements.txt
```

### 2. Configure Neo4J Instance
Open Jupyter notebook named **‘1. Environment Setup.ipynb’** and change the values within the **‘to_insert’** dictionary to your own Neo4J Instance. Then run the cell below to confirm the environment variables have been set correctly.

### 3. (OPTIONAL) Web Scrape Additional Seasons
Regarding the seasons you would like to insert into the database, if they are not already within the **data/season** directory, do the following:
- Open the Jupyter notebook named **‘2. Webscraper.ipynb’**.
- Find the list named **premier_league_seasons** and specify which seasons you would like to web scrape.
- The seasons should be in the list in a string format **yyyy-yyyy**.
- Then run the cell.

**Note:** This step will take at least **20 minutes per season** due to rate limiting set by FBRef.

### 4. Insert Data into Neo4J
The final step to create and insert the data into a Neo4J instance:
- Open the Jupyter notebook named **‘3. Neo4J Data Insertion.ipynb’**.
- Run the cell.

You should see output from the script with the seasons it has inserted. You can now check via the **Neo4J website**, or other visualizers, that nodes and relations have been inserted properly. There should be around **3.2k nodes** and **50k relationships**.




