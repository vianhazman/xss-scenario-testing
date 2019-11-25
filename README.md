## Form XSS Experiment


1. Install virtualenv if not exist
```pip install venv```

2. Create virtual environment
```python -m venv env```
(run this on project ROOT folder)

2. Activate virtual environment

    Windows: ``` env\Scripts\activate.bat```
    
    Mac:
     ```source env/bin/activate```

3. Install needed requirements
```pip install -r requirements.txt```

4. Migrate Database
```python manage.py makemigrations```
```python manage.py migrate```

5. Runserver on local
```python manage.py runserver```