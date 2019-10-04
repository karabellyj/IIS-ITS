# IIS-ITS
## Prerequisites
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.in
mkdir data
touch data/db.sqlite3
./manage.py migrate
./manage.py runserver
```
