[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/2WrSWYXG)
# Group Project  (AT2024)

## Overall objective

This project is intended to assess your overall knowledge about databases and allow you, as a data science team, to design a database application on a topic/scenario of your choice.

<hr>

## ACTION ITEMS & KEY DATES

1. Read the instructions below carefully and completely.
2. Fill in **[this proposal form](https://docs.google.com/forms/d/e/1FAIpQLSf1ukyZQto-9HJj0xV6FhqPPgJqIE3nJzWfmwvHWn0qN3ZmJg/viewform?usp=sf_link)** with your chosen topic (see Item 2 below) by **11 December 2024, noon**.
3. Send an email to **m.e.barreto@lse.ac.uk** saying your proposal is ready to be assessed. **Add your group number to the email**.
4. Proposed topics will be assessed and approved/rejected/asked to be adjusted by **12 December 2024, 9:00 am**.
5. If your topic is approved, go ahead with your project. If your topic is rejected or need to be adjusted, re-submit the proposal form by **13 December 2024, noon** and **repeat step 3**.
6. Wait for a decision by **13 December 2023, 9:00 pm**.

<hr>

## INSTRUCTIONS

### 1. GROUPS

This is a group project. As such, the group is expected to design a solid solution for a particular application or scenario. Everyone in the group is expected to contribute equally to the project.

### 2. TOPIC 

Choose a topic or scenario for which you want to design a database application. Your choice should be based on real database applications that we find and/or use daily, such as entertainment websites/platforms, medical/financial services, transportation, food/goods delivery etc. **E-commerce-like platforms cannot be proposed, as this was covered in the first assignment**.

The topic/scenario can involve standard (structured, tabular) data and/or non-standard (unstructured, audio, video, streaming, multimodal) data. Remember to identify the *main entities and attributes* (objects from the real world), generalisation and specialisation dependencies (if any), and *relationships*. Remember to also identify interesting use cases and any constraints for the chosen database.

The main point for you is to assess how easy/hard is to design a database application for the chosen topic/scenario given i) your knowledge about the context, ii) the set of queries and other operations you can perform against the database, and iii) available data (see item 3).

### 3. DATA

Make sure to identify a consistent set of **real data** to use in your application. You can also **generate synthetic data** if you don't find real data or as a complement to your real data. You can **use any existing dataset(s)** and **import them into your database** application. Make sure you have a clear understanding of the data and its quality and representativeness.

**There is no need to use huge data**, but **make sure you have a good amount of data for each entity/object that allows for relevant queries and/or update operations**.

Please, reflect on the following questions when choosing your data sources:
* Have you identified publicly available data sources? Are they reliable and representative of a real scenario?
* Will you generate synthetic data (including as a complement to your real datasets)? Have you identified suitable tools for that (for instance, Chat-GPT or other AI tool) and do know how to prompt them to get useful outputs?
* Is there sufficient information that allows you to understand how the data was captured and is structured? Here, you may account for any bias or missing data that can influence and/or restrict the type of queries you can run and/or the results.
* Any restrictions or specific concerns about the chosen data sources?

### 4. DATA MODELLING

Make sure to clearly describe all *entities* and *relationships* from the chosen topic/scenario. Also, any constraints and business rules (*assumptions*) that are relevant to your application. There should be a clear explanation of how entities relate to each other, and a clear link between your model and the data you are using.

You *must* provide a data model for the chosen database. This can be an **Entity-Relationship (ER)** model capturing all entities and relationships, primary and foreign keys, single and multivalued attributes, weak entities, partial and total relationships, and any other important aspect for understanding the context of your database application. If you decide for a **NoSQL database**, you must provide a **conceptual description** of the topic, the entities/objects and corresponding structure/attributes, any relationships among the objects, and any other specific aspects you are considering in your model. This conceptual description can be a diagram, a property graph, or text clearly presenting the required information. You can use any modelling tool.

### 5. DATABASE CREATION/DESIGN 

Make sure to describe how entities are created in the chosen database and how the data is populated. You should demonstrate any commands used for defining entities/objects and their attributes, as well as to load data into those entities/objects. If feasible, you can create any **indexes, triggers and views** as needed by the application rules of your topic/scenario. In case of a **NoSQL database**, specify all the creation and/or data load commands needed for mapping your conceptual model into a set of objects (e.g. documents, graphs etc). This step should cover all the **database definition** tasks. **Make sure to show all results/outputs for each command** (screenshots, textual outputs in your Python code etc).

### 6. DATABASE USAGE

Based on the chosen topic/scenario, specify **five** queries *from an user perspective* (i.e., what would be the main operations that an user would execute over your database?). These queries must be **focused on analytical aspects** of you chosen topic/scenario instead of generic queries (for instance, retrieving basic information from a given entity or object). The overall idea is to explore more dynamic scenarios and use cases on your database, such as patterns, groups/clusters of data, evolution of a given data item over time, aggregation and window functions (when feasible), join and subqueries, database views, temporal and/or spatial data (if pertinent to your topic/scenario). You can also consider any update operations as part of your queries. Think about interesting queries that need some programming effort and allow your group to demonstrate your programming and analytical skills.

You **must** provide a **consistent textual description** of each query in terms of i) what the query or update operation is about, ii) input parameters and conditions for filtering/matching data, and iii) outputs. **Only the SQL/NoSQL code is not sufficient; you must provide a textual description (up to 3 paragraphs) explaining all the database operations along with the outputs/results for each query**. **You must provide 5 (five) interesting queries to your database application**.

### 7. DATABASE TECHNOLOGY

Feel free to play with any database software/tool and/or programming library. Make sure to justify your choice based on the chosen topic/scenario and why do you think this tool is the most adequate for your proposed database. **Make sure to provide all code for your database application, the data itself (CSV files or links to external data sources) along with instructions for reproducibility**. You can also comment on any technical restrictions preventing your database to be fully deployed as initially expected.

<hr>

## DELIVERABLES

Your **solution** `MUST` contain:

* a PDF document (**10 pages maximum, except cover**) with:
i) LSE candidate numbers (LSE student IDs are fine in case you don't have your candidate numbers, but **don't put your names**),
ii) description of the chosen topic/scenario (based on item 2),
iii) description of your data (based on item 3),
iv) description of your model (based on item 4): any ER/EER diagram or conceptual description of your NoSQL model. You can upload any images from your database model and provide a brief explanation about entities/attributes/relationships in the report. **Important:** make sure to comment about any restrictions/constraints assumed in your database, along with relevant business rules from the chosen topic/scenario.
v) textual description of all queries (and updates, if any) with the corresponding outputs for each command.
vi) justification of the database technology/tool (item 7) with necessary instructions for reproducibility (for instance, whether an account is necessary, any software download/installation etc). **Links to appropriate pages are fine**.

* code files designed for your project (i.e., SQL commands or scripts, Python notebooks etc).

* any datasets or synthetic data used in your project.
  
* chat logs used to create any datasets and/or brainstorm any code.

* **make sure to upload all your solution files and data to the provided GitHub repository**. In case of storage/space limitations, please provide links to alternative repositories where the data can be accessed.

<hr>

## IMPORTANT DATES

* Assignment released: 06/12/2024, 5 pm.
* Submission of topic proposal: 11 December 2024, noon.
* Project approval/rejection/adjustment decision: 12 December 2024, 9 am.
* Submission of new proposal (if rejected/adjusted): 13 December 2024, noon
* Project approval/rejection decision (if not accepted previously): 13 December 2024, 9 pm.
* Submission of solution: 17/01/2025, 5 pm (London) **firm deadline**
* Feedback and provisional mark: 28/02/2025, 10 pm (tentative)

<hr>

## GENERATIVE AI TOOLS

As per School and course-specific policy, you may acknowledge the use of any generative AI tool in any part of your summative work. You may note that marks can be deducted if no acknowledgement is made and/or a substantial part of your work (especially coding) is done by these tools. See [Moodle](https://moodle.lse.ac.uk/course/view.php?id=11282) for guidance.

You may use these tools literally as a “co-pilot” to help you prototype your database models, generate synthetic data, and/or structure your SQL queries, but the final results must be your own, validated work.

<hr>

## MARKING CRITERIA

* This assignment is worth 60% of the final grade.
* **IMPORTANT**: according to the School policy, you **must** submit an answer to this assignment; otherwise, you will be graded 0 (zero).

| Problem breakdown  | Max marks |
| ------------- | ------------: |
| (2) Topic/scenario - relevance and complexity of the topic/scenario in terms of entities/objects, attributes, generalisation and specialisation dependencies, relationships, constraints and assumptions. Clear description of the topic/scenario.  | 15 |
| (3) Data - Usage of real data and any criteria for subsampling. Generation of synthetic data and how it mimics a real scenario. Good description of the data. Aspects of data consistency and quality. Adherence of data sources to the proposed topic/scenario. Amount of data used versus database usage operations (SQL queries).  | 10 |
| (4) Database modelling - model clarity and consistency (how close to the real scenario the model is). Complete and clear description of all entities/objects, generalisation/specialisation, relationships, keys and constraints. Representative set of use cases and the extent they were explored/implemented by your SQL queries | 20 |
| (5) Database creation - Complete and correct set of commands for materialising the database model into a set of objects (relational tables, documents, nodes etc) and associated relationships. Use of indexes, views, and triggers according to the application rules (chosen topic/scenario). | 10 |
| (6) Database usage - relevant and consistent set of queries and/or update operations. Rationale behind each database operation and to what extent the provided query/update commands have explored the available data and matches the identified use cases. Usage of aggregations, subqueries, join and other complex query/update structures. If available in the database, good exploration of indexes, views, and triggers. Clear documentation of all queries. Submission of all outputs. | 35  |
| (7) Database technology - justification, adherence, and technical complexity involved in its use. Clear instructions for reproducibility purposes. | 5 |
| Documentation - quality of the PDF report, code organisation and documentation. | 5 |
| TOTAL  | 100  |

<hr>

## EXTENSION REQUESTS

You have the right to ask for an extension under some circumstances, as per LSE Extension Policy. Check [here](https://info.lse.ac.uk/current-students/services/assessment-and-results/exceptional-circumstances/extension-policy) for guidance and the necessary documents. **Please note that any extensions must be requested and approved before the deadline, so do not leave this to the last minute as it may incur late penalties being applied to your work**. You should submit your requests to Dr. Christine Yuen (BSc Data Science programme director) and Steve Ellis (Undergraduate Programmes Manager) for analysis. See here for contact details, under Academic Faculty and Professional Service Staff, respectively. If you have adjustments in place and need an extension, follow the same procedure and contact your teachers for advice.

<hr>

## FEEDBACK AND PROVISIONAL MARKS

Feedback and provisional marks will be provided in a markdown (.md) file in your “assignment1” repository by the expected date. Please, note that we do our best to provide you with relevant and meaningful feedback by the intended deadline, but **we reserve the right to delay any feedback while any extension requests are in place. You may also note that all marks are provisional and subject to changes to comply with School and departmental policies on mark distributions and as a result of external examiners and sub-board revisions**.

<hr>

## REVISION OF FEEDBACK AND PROVISIONAL MARKS

We advise you to read carefully your feedback file and get in touch with the teaching staff to discuss any points. We are available to revise any specific parts of your feedback when **there is a justifiable reason for that**. Please, **raise any points regarding your feedback and provisional marks up to two weeks after receiving them**. We may refrain from revising any parts of your feedback and provisional marks later in the academic year due to the internal flow/processing of marks across department and school sub-boards and external examiners.

<hr>

## REFERENCES

- Wikipedia: [Database application](https://en.wikipedia.org/wiki/Database_application) - some example databases.
- [10 Database Examples in Real Life](https://www.liquidweb.com/blog/ten-ways-databases-run-your-life/)
- [Database Applications Types and Examples](https://www.mongodb.com/basics/database-application)
- [15 Database Software Examples 2022](https://rigorousthemes.com/blog/database-software-examples/)
- Medium: [10 Best Database Design Practices](https://medium.com/quick-code/10-best-database-design-practices-1f10f3441730)
- Learn Computer Science: [How to design a database?](https://www.learncomputerscienceonline.com/how-to-design-database/)
- The Digital Skye: [8 Practical Guidelines for Designing Databases That Don’t Land You in Hot Water](https://thedigitalskye.com/2020/12/19/8-practical-guidelines-for-designing-databases-that-dont-land-you-in-hot-water/)

#### Multimedia databases

* https://en.wikipedia.org/wiki/Multimedia_database
* https://www.sciencedirect.com/topics/computer-science/multimedia-databases

#### Spatial Databases

* https://en.wikipedia.org/wiki/Spatial_database
* Kinetica - https://www.kinetica.com/features/geospatial-analytics/
* https://www.safe.com/blog/2021/11/7-spatial-databases-enterprise/
* Oracle - https://www.oracle.com/uk/database/spatial/
* https://gisgeography.com/spatial-databases/

#### Streaming databases

* https://www.theseattledataguy.com/7-real-time-data-streaming-databases-which-one-is-right-for-you/#page-content
* HStreamDB - https://hstream.io/
* Amazon AWS - https://aws.amazon.com/streaming-data/
* ksqlDB - https://ksqldb.io/

#### NoSQL databases

* https://en.wikipedia.org/wiki/NoSQL
* DataStax - https://www.datastax.com/lp/nosql-database
* IBM Cloud - https://www.ibm.com/uk-en/cloud/free/databases
* MongoDB NoSQL - https://www.mongodb.com/nosql-explained
* https://www.g2.com/categories/graph-databases
* https://en.wikipedia.org/wiki/Graph_database
* Neo4j - https://neo4j.com/developer/graph-database/

### Additional references

- Microsoft: [Database design basics](https://support.microsoft.com/en-us/office/database-design-basics-eb2159cf-1e30-401a-8084-bd4f9c9ca1f5)
- Xplenty: [Complete Guide to Database Schema Design](https://www.xplenty.com/blog/complete-guide-to-database-schema-design-guide/)
