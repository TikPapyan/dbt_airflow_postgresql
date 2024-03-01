### NBA Data Pipeline Project

This project showcases the construction of an end-to-end data pipeline, emphasizing the integration of diverse technologies to facilitate the process of downloading NBA player data, transforming it, and visualizing the insights.

## Technologies Used

- **Kaggle NBA players dataset**: Source of NBA player statistics and demographics.
- **Apache Airflow**: Orchestrates the data pipeline's workflow.
- **PostgreSQL**: Stores the transformed data for analysis.
- **dbt (data build tool)**: Transforms raw data into an analytical format.
- **GitHub Actions**: Automates testing and deployment of the data pipeline.
- **Metabase**: Visualizes data through interactive dashboards.

This diverse set of technologies enables a comprehensive approach to data analytics, from initial data ingestion to in-depth analysis and visual presentation.

## Data Source and Integration

### Kaggle NBA players dataset

The [Kaggle NBA Players Dataset](https://www.kaggle.com/datasets/justinas/nba-players-data) is a comprehensive collection of data on NBA players, encompassing statistics, demographics, and performance metrics across multiple seasons. It serves as the primary data source for this project, offering insights into player performance and trends in professional basketball. To access and download this dataset, an **API token** from Kaggle is required, enabling automated data retrieval within the pipeline.

## Local Environment Setup

### Setting up the environment

1. **Creating a directory**

 - Create a dedicated directory (`nba_project`) to organize and isolate the project environment

```
mkdir nba_project
```

2. **Activating Virtual Environment**

```
python3 -m venv myenv
source myenv/bin/activate
```

## Apache Airflow Setup

Integrate Apache Airflow to orchestrate and automate your data pipeline workflows:

1. **Install Apache Airflow**

 - Use the provided `install_airflow.sh` script from the repository to install Airflow.

2. **Initialize Airflow**

```
airflow standalone
```

 - This command will generate an Airflow directory in your home directory.

3. **Move Airflow Directory**

```
mv ~/airflow .
```

 - Move the Airflow directory into your `nba_project`.

4. **Prepare Airflow DAG Directory**

```
mkdir airflow/dags
```

5. **Setup DAG for NBA Pipeline**

 - Create `nba_pipeline.py` in the dags directory with the pipeline logic.

6. **Login to Airflow Web Interface**

 - Typically available at http://localhost:8080.

7. **Encrypt Airflow Variables**

   i. Install required package
      ```bash
      pip install 'apache-airflow[crypto]'
      ```
   ii. Create a small Python script and run it to generate the fernet key
      ```python
      from cryptography.fernet import Fernet
      fernet_key = Fernet.generate_key()
      print(fernet_key.decode()) # This will print your new Fernet key.
      ```
   iii. Find the `fernet_key` in `airflow.cfg` file and paste the generated fernet key there

8. **Restart Airflow**

 - To apply encryption settings, restart Airflow.

9. **Enter Kaggle API Credentials in Airflow**

 - Add your Kaggle username and key in Airflow Variables through the web interface.

![Kaggle API credentials in Airflow Variables](https://github.com/TikPapyan/dbt_airflow_postgresql/blob/main/screenshots/kaggle_credentials.png)

## PostgreSQL Setup

Set up PostgreSQL to serve as the robust, relational database for storing and managing your pipeline's data

1. **Install PostgreSQL**

 - Use the `install_postgresql.sh` script from the repository.

2. **Database and User Configuration**

Access the PostgreSQL environment, create a new database user, establish a database, and assign full access rights to the new user:

```
sudo -i -u postgres       # Switch to the PostgreSQL system user
createuser --interactive --pwprompt  # Interactively create a new user with a password prompt
createdb your_db          # Create a new database named 'your_db'
GRANT ALL PRIVILEGES ON DATABASE your_db TO your_user;  # Grant the new user full access to 'your_db'
```

3. **Enter PostgreSQL database Credentials in Airflow**

 - Add your PostgreSQL database credentials in Airflow Variables through the web interface.

![PostgreSQL database credentials in Airflow Variables](https://github.com/TikPapyan/dbt_airflow_postgresql/blob/main/screenshots/postgres_credentials.png)

4. **Create Table Structure**

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

5. **Database Exploration**

 - Use `psql` commands to explore databases and tables.

 ```
 \l: List all databases
 \c your_db: Connect to your database
 \dt: List tables in the current database
 ```

## dbt Setup

Install dbt to manage data transformation workflows efficiently:

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

![dbt init prompt](https://github.com/TikPapyan/dbt_airflow_postgresql/blob/main/screenshots/dbt_init.png)

4. **Create dbt Models**

In your `nba_dbt_project/models/` directory, create SQL files for your dbt models. Define and implement tests for data integrity in `schema.yml`:

```
sources:
  - name: public
    description: "Public schema in the PostgreSQL database."
    tables:
      - name: nba_players
        description: "Table containing NBA player data."
        columns:
          - name: field1
            description: "A unique identifier for each player."
            tests:
              - unique
              - not_null
```

5. **Implement tests for duplicate and null values as necessary.**

 - Run and Test dbt Models

```
dbt run
dbt test
```

![dbt run result](https://github.com/TikPapyan/dbt_airflow_postgresql/blob/main/screenshots/dbt_run.png)
![dbt test result](https://github.com/TikPapyan/dbt_airflow_postgresql/blob/main/screenshots/dbt_test.png)

6. **Generate and Serve dbt Documentation**

```
dbt docs generate
dbt docs serve --port 8081
```

 - Adjust the port if necessary (especially if you run Airflow, which is being ran on 8080 by default).

## GitHub Actions for CI/CD

Automate testing and deployment of your data pipeline using GitHub Actions:

1. **Set Up GitHub Actions Workflow**

```
mkdir ~/nba_project/.github/workflows
```

2. Configure Workflow

Copy the `dbt.yml` workflow file (provided in your repository) into the newly created workflows directory. This file should define steps for testing and deploying your dbt models and Airflow DAGs.

3. Automate CI/CD Pipeline

Commit and push changes to your repository's main branch. GitHub Actions will automatically execute the workflows defined in `dbt.yml` to test and deploy your changes

## Metabase for Visualization

Leverage Metabase for intuitive data visualization and dashboard creation:

1. **Deploy Metabase**

Deploy Metabase using Docker for quick setup:

```
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

2. **Initialize Metabase**

Access Metabase at `http://localhost:3000` and follow the setup wizard to configure your account and connect it to your PostgreSQL database.

3. **Visualize Data**

Create and customize dashboards in Metabase to explore and visualize your transformed NBA player data for insights.

## Conclusion

In conclusion, setting up a robust data pipeline with dbt, PostgreSQL, and Apache Airflow lays a solid foundation for managing and analyzing data efficiently. By integrating these powerful tools, you can automate data workflows, securely store and transform data, and prepare it for insightful analysis and visualization with Metabase. This comprehensive approach not only streamlines your data processing tasks but also empowers you to uncover valuable insights from the NBA players dataset, enhancing your data-driven decision-making capabilities. With the setup and configuration steps outlined, you're well-equipped to embark on a journey of sophisticated data exploration and analysis
