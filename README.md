# TEC Energy Dev Project

This take home project downloads gas shipment data from [Energy Transfer](https://twtransfer.energytransfer.com/ipost/TW/capacity/operationally-available), validates it, and stores it in a PostgreSQL database.

## Requirements

- Python 3.7+
- PostgreSQL
- Pip3

## Installation

1. Clone repository:
```bash
https://github.com/JanVillapaz/tec-energy-project.git
```

Install requirements.txt

2. Install required packages: 
```bash
pip install -r /path/to/requirements.txt
```

3. Configure DB
- Create Postgres DB named `natural_gas_db`
- Update the database config in `main.py` with your credentials

## Database Schema
- For schema, please consult `create_table.sql` file in `db` folder

## Usage
Run the main script
```bash
python main.py
```

## Author
Developed by Jan Eunice Villapaz


## References
- [Old Python School Project](https://github.com/JanVillapaz/INF5190-AUT2021/blob/main/README.md)

