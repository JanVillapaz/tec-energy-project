# TEC Energy Dev Project

This take home project downloads gas shipment data from [Energy Transfer](https://twtransfer.energytransfer.com/ipost/TW/capacity/operationally-available), validates it, and stores it in a PostgreSQL database.

## Requirements

- Python 3.7+
- PostgreSQL
- Pip3

## Installation

### 1. Clone repository:
```bash
git clone https://github.com/JanVillapaz/tec-energy-project.git

```

### 2. Change directory (to the clone repo)

```sh
cd tec-energy-project
```

### 3. Create a Virtual Environment
This is to keep the dependencies isolated
```sh
python -m venv venv
```

#### Activate it

- For Windows
```sh
venv/scripts/activate
```

- For Mac / Linux / Git Bash
```sh
source venv/Script/activate
```

#### If successful
`(venv)` will appear on CMD / GitBash / Console / PowerShell


### 4. Install dependensies: 
```bash
pip install -r /path/to/requirements.txt
```

### 5. Configure DB
- Create Postgres DB named `natural_gas_db`. This can easily be done on PgAdmin
- Update the database config in `main.py` with your credentials.

## Database Schema
- For schema, please consult `create_table.sql` file in `db` folder.

## Usage
Run the main script
```bash
python main.py
```

## Deliverables
- [x] DDL of a database table(s) where the data will be inserted. (Postgres SQL preferred, but any relational DB is okay)

- [x] The necessary query(s) to insert this data.

- [x] The code to facilitate the downloading, validation, and insertion of the data. C# and Python are our preferred languages but feel free to use something else if you would feel more comfortable.

- [x] Instructions on how to run the code in the form of a readme.

- [x] The deliverables should all be uploaded to a public git repository (like GitHub)

## Author
Developed by Jan Eunice Villapaz

## References
- [Old Python School Project](https://github.com/JanVillapaz/INF5190-AUT2021/blob/main/README.md)
- [Making Python loggers output all messages to stdout in addition to logfile](https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file)
- [How to Download Files From URLs With Python](https://realpython.com/python-download-file-from-url/#:~:text=To%20download%20a%20file%20using,the%20URL%20or%20query%20parameters.)
- [PostgreSQL Python: Connect to PostgreSQL Database Server](https://neon.tech/postgresql/postgresql-python/connect)
-[Change a column type in a DataFrame in Python Pandas](https://sentry.io/answers/change-a-column-type-in-a-dataframe-in-python-pandas/#:~:text=If%20we%20want%20to%20convert%20a%20column%20to%20a%20sensible,should%20use%20the%20convert_dtypes%20method.)
