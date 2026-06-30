# Flask_project
This is a simple flask project

How to run this program
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\venv\bin\Activate
pip install -r requirements.txt
```# lenovo-test-app


## Command to query table for users table
```bash
& "C:\Users\MiftahAhmadChoiri\AppData\Local\Python\pythoncore-3.14-64\python.exe" -c "import sqlite3; conn=sqlite3.connect('ticketing.db'); [print(r) for r in conn.execute('SELECT * FROM users')]"
```