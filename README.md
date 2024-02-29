### NBA Data Pipeline Project

This project leverages Apache Airflow, PostgreSQL, dbt (data build tool), and Metabase to automate the process of downloading NBA player data, transforming it, and visualizing the insights.

## Setup and Installation Guide

1. **Create Project Directory**

```
mkdir nba_project && cd nba_project
```

2. **Setup Python Virtual Environment**

```
python3 -m venv myenv
source myenv/bin/activate
```

3. **Install Apache Airflow**

 - Use the provided install_airflow.sh script from the repository to install Airflow.

4. **Initialize Airflow**

```
airflow standalone
```

 - This command will generate an Airflow directory in your home directory.

5. **Move Airflow Directory**

```
mv ~/airflow .
```

 - Move the Airflow directory into your nba_project.

6. **Prepare Airflow DAG Directory**

```
mkdir airflow/dags
```

7. **Setup DAG for NBA Pipeline**

 - Create nba_pipeline.py in the dags directory with the pipeline logic.

8. **Login to Airflow Web Interface**

 - Typically available at http://localhost:8080.

9. **Kaggle API Token**

 - Generate a Kaggle API token for downloading the NBA dataset.

10. **Enter Kaggle API Credentials in Airflow**

 - Add your Kaggle username and key in Airflow Variables through the web interface.

## PostgreSQL Setup

1. **Install PostgreSQL**

 - Use the install_postgresql.sh script from the repository.

2. **Database and User Configuration**

```
sudo -i -u postgres
createuser --interactive --pwprompt
createdb your_db
GRANT ALL PRIVILEGES ON DATABASE your_db TO your_user;
```

3. **Create Table Structure**

 - To create the table structure, use a tool like [ConvertCSV](https://www.convertcsv.com/csv-to-sql.htm) to generate a SQL creation query from your CSV file.

```
CREATE TABLE nba_players(
        FIELD1              INTEGER  NOT NULL PRIMARY KEY 
        ,"player name"       VARCHAR(24) NOT NULL
        ,"team abbreviation" VARCHAR(3) NOT NULL
        ,age                 NUMERIC(4,1) NOT NULL
        ,"player height"     NUMERIC(6,2) NOT NULL
        ,"player weight"     VARCHAR(18) NOT NULL
        ,college             VARCHAR(39)
        ,country             VARCHAR(32) NOT NULL
        ,"draft year"        VARCHAR(9) NOT NULL
        ,"draft round"       VARCHAR(9) NOT NULL
        ,"draft number"      VARCHAR(9) NOT NULL
        ,gp                  INTEGER  NOT NULL
        ,pts                 NUMERIC(4,1) NOT NULL
        ,reb                 NUMERIC(4,1) NOT NULL
        ,ast                 NUMERIC(4,1) NOT NULL
        ,"net rating"        NUMERIC(6,1) NOT NULL
        ,"oreb pct"          VARCHAR(20) NOT NULL
        ,"dreb pct"          VARCHAR(20) NOT NULL
        ,"usg pct"           VARCHAR(20) NOT NULL
        ,"ts pct"            VARCHAR(20) NOT NULL
        ,"ast pct"           VARCHAR(20) NOT NULL
        ,season              VARCHAR(7) NOT NULL
);
```

4. **Database Exploration**

 - Use psql commands to explore databases and tables.

## Airflow Configuration

1. **Encrypt Airflow Variables**

 - Install necessary packages and configure the Fernet key as described.

2. **Restart Airflow**

 - To apply encryption settings, restart Airflow.

## dbt Setup

1. **Install dbt**

```
pip install dbt-postgres
```

2. **Initialize dbt Project**

```
mkdir dbt && cd dbt
dbt init nba_dbt_project
cd nba_dbt_project
```

3. **Configure dbt**

 - Enter database connection details as prompted by dbt init. Use secure practices for handling credentials.
Develop dbt Models

4. **Create your dbt models within nba_dbt_project/models/.**

 - Define Tests in schema.yml

5. **Implement tests for duplicate and null values as necessary.**

 - Run and Test dbt Models

```
dbt run
dbt test
```

6. **Generate and Serve dbt Documentation**

```
dbt docs generate
dbt docs serve --port 8081
```

 - Adjust the port if necessary.

## GitHub Actions for CI/CD

1. **Create GitHub Actions worfklow**

```
mkdir ~/nba_project/.github/workflows
```

2. Use the provided dbt.yml from the repository to create the workflow.

3. When pushing the changes on the main branch, the GitHub Actions will run

## Metabase for Visualization

1. **Install Metabase**

```
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

2. **Setup Metabase Account**

 - Follow the Metabase setup wizard to connect your PostgreSQL database.

3. **Explore and Create Dashboards**

 - Utilize Metabase to visualize the data and create insightful dashboards.

## Additional Notes

 - Ensure to securely manage sensitive information, such as database credentials and API keys, using best practices or services like GitHub Secrets.
 - The provided scripts and commands assume a Unix-like environment. Adjustments may be necessary for other systems.
