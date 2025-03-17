# TEC Energy Dev Project

This take home project downloads gas shipment data from [Energy Transfer](https://twtransfer.energytransfer.com/ipost/TW/capacity/operationally-available), validates it, and stores it in a PostgreSQL database.

## Requirements

- Python 3.7+
- PostgreSQL
- Pip3

## Installation

### 1. Clone repository:
```bash
https://github.com/JanVillapaz/tec-energy-project.git
```

### 2. Install required packages: 
```bash
pip install -r /path/to/requirements.txt
```

### 3. Configure DB
- Create Postgres DB named `natural_gas_db`.
- Update the database config in `main.py` with your credentials.

## Database Schema
- For schema, please consult `create_table.sql` file in `db` folder.

## Usage
Run the main script
```bash
python main.py
```

## Author
Developed by Jan Eunice Villapaz

## References
- [Old Python School Project](https://github.com/JanVillapaz/INF5190-AUT2021/blob/main/README.md)
- [Making Python loggers output all messages to stdout in addition to logfile](https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file)
- [How to Download Files From URLs With Python](https://realpython.com/python-download-file-from-url/#:~:text=To%20download%20a%20file%20using,the%20URL%20or%20query%20parameters.)
