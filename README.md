# Project: Data Warehouse

This is Project 3: Data Warehouse, part of Udacity's Nanodegree in Data Engineering.

## Project Description

In this project, we have to build an ETL pipeline for a database hosted on Redshift. This is achieved by loading data from S3 to staging tables on Redshift and executing SQL statements that create the analytics tables from these staging tables.

## Project files and running the project

Running the project:

1 - Specify the AWS Access Key and Secret.
2 - Run the cells in `IaC.ipynb` to create the infrastructure in AWS.
3 - Once the infrastructure has been created, run `python create_tables.py` to create the tables in Redshift.
4 - Run `python create_tables.py` to run the ETL pipeline i.e. load the data from S3 into the staging tables in Redshift and execute the SQL statements to create the analytics tables.

## File descriptions (To do!!)

Different files and folders can be found in the repository:

- The `Data` folder contains the song and log datasets.
- The `media` folder contains diagramms used in this document to represent the data model and the etl process.
- The `create_tables.py` script contains the code necessary for creating the database and its tables.
- The `sql_queries.py` contains the different SQL queries used by the other scripts.
- The `etl.py` script contains the code necessary for running the pipeline.
- The `etl.ipynb` Notebook was used for coding in an interactive way the `etl.py` script.
- The `test.ipynb` Notebook includes some SQL queries for debugging i.e. testing the content of the tables at any time.
- The `er_generator.py` script contains the code necessary for generating the entity relation diagram.


## Architecture Overview


## Database schema and ETL pipeline design


