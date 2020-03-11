import sqlite3 #import the sql package
from flask import Flask, render_template, g # g is the global helper

PATH = 'db/jobs.sqlite' #sets path to the db

app = Flask(__name__)

#create the open connection function to connect to the db
#set row fac to sqlite - all rows returned from db are called tuples
#this will make row indexing easier
def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH) #if none set to Path
    connection.row_factory = sqlite3.Row
    return connection

#create query db function
#add 4 parametes  sql, values, commit and single. values is set to empty tuple()
#asssign the return value to a variable called a cursor
# if commit is true, assign var results to return func connection.commit()

def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results

#create a function to close database conneciton
#@appteardown ensures close connecton is called- its considered a decarator
@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()



@app.route('/')
@app.route('/jobs')
def jobs():
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template ('index.html', jobs=jobs)

@app.route('/job/<job_id>')
def job(job_id):
    job = ('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id
    WHERE job.id = ?')#,[job_id], single=True)
    return render_template('job.html', job=job)
