# Data Warehouses

## Why are Datawarehouses needed?
For simpler and small use cases a database can be used. Nevertheless, at some point, a database reaches its boundaries in terms of:
- Scale
- Complexity
- Performance

## Operational vs Analytical Processes
Storage engines fall into two broad categories: those optimized for transaction processing (OLTP), and those optimized for analytics (OLAP).
There are big differences between the access patterns in those use cases:

### Operational Processes (OLTP: Online Transactional Processing)
- Primarly used by end user/customer, via web application i.e. huge number of requests
- Main read pattern: Small number or records per query, fetched by key. Bottleneck is disk seek time.
- Main write pattern: Random-access, low-latency writes from user input
- Data represents its latest state (current point in time)
- Dataset size: Gigabytes to terabytes
- Storage Engine: Log-structured (SSTables, LSM-Trees,..) and update-in-place or page-oriented (B-Trees)

### Analytical Processes (OLAP: Online Analytical Processing)
- Primarly used by internal analyst, for decision support.
- Main read pattern: Aggregate over large number of records. Bottleneck is disk bandwidth
- Main write pattern: Bulk import (ETL) or event stream.
- Data represents a history of events that happened over time
- Dataset size: Terabytes to petabytes
- Storage Engine: Column-oriented

Data Warehouses enable us to support analytical processes. Here we extract the data from the source systems used for operations, transform it, and load it into a dimensional model that can be used by business-user-facing applications.


## Dimensional Modelling: 3NF to Star Schema
The 3rd Normalized Form (3NF) is a database schema design approach which uses normalizing principles to reduce the duplication of data.

By using a Star Schema we make the data easier to understand and fast for analytical queries. In the Star Schema we can distinguish between Fact and Dimension Tables:

Fact tables:
- Record events, like an order, a phone call or a book review.
- Fact tables columns can be used to calculate quantifiable metrics like quantity of an item, duration of a call or a book rating.

Dimension tables:
- Record the context of the business events, e.g. who, what, where, why, etc.
- Dimension tables columns contain attributes like the store at which an item is purchased or the customer who made the call, etc.

Following the Kimball data warehouse design, a common scenario in Data Warehouses is to have an ETL process to transform 3NF Data (as it is found in the source systems) to a Star Schema make it easier to consume for analytical purposes.

## DWH Architectures: Kimball's and Inmon's Design

There are two main data warehouse design methodologies: Kimball and Inmon.

In the Kimball Methodology the primary data sources are then evaluated, and an Extract, Transform and Load (ETL) tool is used to fetch data from several sources and load it into a staging area of the relational database server. Once data is uploaded in the  data warehouse staging area, the next phase includes loading data into a dimensional data warehouse model that’s denormalized by nature. This model partitions data into the fact table, which is numeric transactional data or dimension table, which is the reference information that supports facts. Star schema is the fundamental element of the dimensional data warehouse model.

![Kimball](/media/Project3_DataWarehouse-Kimball.drawio.png)

The Bill Inmon design approach uses the normalized form for building entity structure, avoiding data redundancy as much as possible. Data loading becomes less complex due to the normalized structure of the model. However, using this arrangement for querying is challenging as it includes numerous tables and links.

This Inmon data warehouse methodology proposes constructing data marts separately for each division, such as finance, marketing sales, etc. All the data entering the data warehouse is integrated. The data warehouse acts as a single data source for various data marts to ensure integrity and consistency across the enterprise.

![Inmon](/media/Project3_DataWarehouse-Inmon.drawio.png)

## OLAP Cubes

Once we have a star schema, we can create OLAP cubes, which are an aggregation of a number of dimensions like e.g. Movie, Branch, Month.

It is basically pre-aggregating some metrics, so that they can be queried faster.

Some operations can be done on the OLAP Cubes like
- roll-ups (reducing the columns in one dimension)
- drill-downs (more columns in one dimension)
- slices (reducing one dimension to a single value)
- dices (mantaining the dimensions, but computing a sub-cube, by restricting one dimension to some values)

## Implementing OLAP Cubes
OLAP Cubes can be basically calculated following two approaches:
- Pre-aggregated OLAP Cubes and saving them on a special purpose non-relational database (MOLAP)
- Computing the OLAP Cubes on the fly from the existing relational database where the dimensional model resides (ROLAP)

# Amazon Redshift

Redshift is an AWS-managed service which provides SQL-Columnar-Database with the capacity to perform massive parallel processing. Internally it's a modified PostgreSQL.

## Redshift - A technical perspective
Massively Parallel Processing (MPP) databases parallelize the execution of one query on multiple CPUs/machines.

Most relational databases are able to execute multiple queries in parallel, but usually they are executed in a single CPU. In MPP Databases, tables are partitioned so that the queries can be executed by multiple CPUs in parallel.

Other examples of MPP Databases: Teradata, Aster, Oracle ExaData, Azure SQL,...

In Redshift we have:
- Leader nodes: Coordinates compute nodes, handles external communication, optimizes query execution.
- Compute Nodes: Each with own CPU, memory, and disk (determined by the node type).
- Node Slices: Each compute node is logically divided into a number of slices. A cluster with n slices can process n partitions of tables simultaneously

## Redshift - Design considerations

Node Types:
- Compute Optimized Nodes: Start with these for lower costs and a capacity of 5 terabytes.
- Storage Optimized Nodes: Higher costs, not as fast, but higher capacity

### SQL to SQL ETL (To do!)

### Parallel ETL

### Table Design (Distribution Style and sort Key)

Distribution Style
- EVEN distribution: Round-robin over all slices to achieve load-balancing. Good if a table won’t be joined
- ALL distribution. Small tables could be replicated on all slices to speed up joins. Used frequently for dimension tables. AKA “broadcasting”
- AUTO distribution: Leave decision to Redshift. “Small enough” tables are distributed with an ALL strategy, large tables are distributed with EVEN strategy.
- KEY distribution: Rows having similar values are placed in the same slice

Sorting key
- Define columns as sort key
- Rows are sorted before distribution to slices
- Minimizes the query time
- Useful for columns that are used frequently in sorting like the date dimension and its corresponding foreign key in the fact table