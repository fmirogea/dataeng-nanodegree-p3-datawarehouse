# Project: Data Warehouse

This is Project 3: Data Warehouse, part of Udacity's Nanodegree in Data Engineering.

## Project Description

In this project, we have to build an ETL pipeline for a database hosted on Redshift. This is achieved by loading data from S3 to staging tables on Redshift and executing SQL statements that create the analytics tables from these staging tables.

## Architecture Overview

The architecture of this project is defined as follows.

- The project files are in a GitHub repository.
- The Jupyter notebook currently runs on a Udacity instance.
- The Source Data used for this project lays already in an AWS S3 bucket.
- Using the project files, the Redshift infrastructure can be created and deleted, and the ETL pipeline can be triggered. 

![Architecture Overview](/media/Project3_DataWarehouse-Architecture.drawio.png)


## Project files and running the project

Running the project:

1. Specify the AWS Access Key and Secret in the `dwh.cfg` file 
2. Run the cells in `IaC.ipynb` to create the infrastructure in AWS.
3. Once the infrastructure has been created, run `python create_tables.py` to create the tables in Redshift.
4. Run `python create_tables.py` to run the ETL pipeline i.e. load the data from S3 into the staging tables in Redshift and execute the SQL statements to create the analytics tables.

## Costs

Costs associated with the Redshift cluster (us-east-1 zone on 24.02.2023):
- DWH_CLUSTER_TYPE=single-node, DWH_NUM_NODES=1, DWH_NODE_TYPE=dc2.large: 0,25 USD/h
- DWH_CLUSTER_TYPE=multi-node, DWH_NUM_NODES=2, DWH_NODE_TYPE=dc2.large: 0,51 USD/h
- DWH_CLUSTER_TYPE=multi-node, DWH_NUM_NODES=4, DWH_NODE_TYPE=dc2.large: 1,01 USD/h

A dc2.large node has 2 vCPU and 15 GiB Memory.

## File descriptions
Different files and folders can be found in the repository:

- The `media` folder contains diagramms used in this document to represent the data model and the etl process.
- The `create_tables.py` script contains the code necessary for creating the staging and analytics tables in Redshift.
- The `sql_queries.py` contains the different SQL queries used by the other scripts.
- The `etl.py` script contains the code necessary for running the pipeline.
- The `IaC.ipynb` Notebook includes the scripts required to create and delete the AWS Infrastructure by using the Python SDK based in Boto3.

## Database schema and ETL pipeline design

The relations during the ETL pipeline can be described as follows:
![ETL](/media/Project3_DataWarehouse-ETL.drawio.png)
- The staging tables contain the data in the same format as it could be found in the source. For those tables all fields are kept nullable. The goal is to get the data as it is in the source.

The data model can be described as follows:

![Data Model](/media/Project3_DataWarehouse-DataModel.drawio.png)

- Five analytical tables have been defined, following a Star Schema, optimizing for providing fast answers to analytical queries.
- The smaller tables `artists`, `songs` and `users` follow an ALL distribution i.e. are replicated on all slices to speed up joins.
- `times` and `songplays` tables are distributed following a KEY distribution. 


## Additional Documentation
Further notes on this project and Data Warehouse design can be found ![here](/DataWarehouse.md).