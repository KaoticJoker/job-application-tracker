import json
import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from mysql.connector import Error, IntegrityError
from database import get_db

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'development-only-change-me')

TABLES = {
 'companies': {'pk':'company_id','title':'Companies','fields':[('company_name','Company name','text',True),('industry','Industry','text',False),('website','Website','url',False),('city','City','text',False),('state','State','text',False),('notes','Notes','textarea',False)]},
 'jobs': {'pk':'job_id','title':'Jobs','fields':[('company_id','Company','company',True),('job_title','Job title','text',True),('job_type','Job type','job_type',False),('salary_min','Minimum salary','number',False),('salary_max','Maximum salary','number',False),('job_url','Job URL','url',False),('date_posted','Date posted','date',False),('requirements','Requirements JSON','json',False)]},
 'applications': {'pk':'application_id','title':'Applications','fields':[('job_id','Job','job',True),('application_date','Application date','date',True),('status','Status','status',False),('resume_version','Resume version','text',False),('cover_letter_sent','Cover letter sent','checkbox',False),('interview_data','Interview data JSON','json',False)]},
 'contacts': {'pk':'contact_id','title':'Contacts','fields':[('company_id','Company','company',True),('contact_name','Contact name','text',True),('title','Title','text',False),('email','Email','email',False),('phone','Phone','text',False),('linkedin_url','LinkedIn URL','url',False),('notes','Notes','textarea',False)]},
}
JOB_TYPES=['Full-time','Part-time','Contract','Internship']
STATUSES=['Applied','Screening','Interview','Offer','Rejected','Withdrawn']

def fetch_all(sql, params=()):
    conn=get_db()
    try:
        cur=conn.cursor(dictionary=True)
        try:
            cur.execute(sql,params)
            return cur.fetchall()
        finally: cur.close()
    finally: conn.close()

def fetch_one(sql, params=()):
    rows=fetch_all(sql,params)
    return rows[0] if rows else None

def execute(sql, params=()):
    conn=get_db()
    try:
        cur=conn.cursor()
        try:
            cur.execute(sql,params)
            conn.commit()
            return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally: cur.close()
    finally: conn.close()

def config(table):
    if table not in TABLES: abort(404)
    return TABLES[table]

def options():
    return {'company':[(x['company_id'],x['company_name']) for x in fetch_all('SELECT company_id, company_name FROM companies ORDER BY company_name')],
            'job':[(x['job_id'],f"{x['job_title']} — {x['company_name']}") for x in fetch_all('SELECT j.job_id,j.job_title,c.company_name FROM jobs j JOIN companies c ON c.company_id=j.company_id ORDER BY j.job_title')],
            'job_type':[(x,x) for x in JOB_TYPES], 'status':[(x,x) for x in STATUSES]}

def parse_form(cfg):
    values={}
    for field,label,kind,required in cfg['fields']:
        raw=request.form.get(field,'').strip()
        if kind=='checkbox': values[field]=1 if request.form.get(field) else 0; continue
        if required and not raw: raise ValueError(f'{label} is required.')
        if kind=='json' and raw:
            try: values[field]=json.dumps(json.loads(raw))
            except json.JSONDecodeError as e: raise ValueError(f'{label} must be valid JSON: {e.msg}')
        elif kind in ('number','company','job') and raw:
            try:
                values[field]=int(raw)
                if values[field]<0: raise ValueError()
            except ValueError: raise ValueError(f'{label} must be a nonnegative whole number.')
        elif kind=='date' and raw:
            try: values[field]=date.fromisoformat(raw).isoformat()
            except ValueError: raise ValueError(f'{label} must be a valid date.')
        elif kind=='job_type' and raw not in JOB_TYPES: raise ValueError('Invalid job type.')
        elif kind=='status' and raw not in STATUSES: raise ValueError('Invalid status.')
        else: values[field]=raw or None
    if cfg is TABLES['jobs'] and values.get('salary_min') is not None and values.get('salary_max') is not None and values['salary_min']>values['salary_max']:
        raise ValueError('Minimum salary cannot exceed maximum salary.')
    return values

@app.route('/')
def dashboard():
    counts={t:fetch_one(f'SELECT COUNT(*) AS n FROM {t}')['n'] for t in TABLES}
    statuses=fetch_all('SELECT status,COUNT(*) AS n FROM applications GROUP BY status ORDER BY n DESC')
    recent=fetch_all("""SELECT a.application_id,a.application_date,a.status,j.job_title,c.company_name
       FROM applications a JOIN jobs j ON j.job_id=a.job_id JOIN companies c ON c.company_id=j.company_id
       ORDER BY a.application_date DESC,a.application_id DESC LIMIT 8""")
    return render_template('dashboard.html',counts=counts,statuses=statuses,recent=recent)

@app.route('/<table>')
def listing(table):
    cfg=config(table)
    if table=='jobs':
        rows=fetch_all('SELECT j.*,c.company_name FROM jobs j JOIN companies c ON c.company_id=j.company_id ORDER BY j.job_id DESC')
    elif table=='applications':
        rows=fetch_all("""SELECT a.*,j.job_title,c.company_name FROM applications a JOIN jobs j ON j.job_id=a.job_id
           JOIN companies c ON c.company_id=j.company_id ORDER BY a.application_id DESC""")
    elif table=='contacts':
        rows=fetch_all('SELECT ct.*,c.company_name FROM contacts ct JOIN companies c ON c.company_id=ct.company_id ORDER BY ct.contact_id DESC')
    else: rows=fetch_all('SELECT * FROM companies ORDER BY company_id DESC')
    return render_template('list.html',table=table,cfg=cfg,rows=rows)

@app.route('/<table>/new',methods=['GET','POST'])
def create(table):
    cfg=config(table)
    if request.method=='POST':
        try:
            vals=parse_form(cfg)
            fields=list(vals)
            execute(f"INSERT INTO {table} ({','.join(fields)}) VALUES ({','.join(['%s']*len(fields))})",tuple(vals.values()))
            flash('Record created.','success')
            return redirect(url_for('listing',table=table))
        except (ValueError,Error) as e: flash(str(e),'danger')
    return render_template('form.html',table=table,cfg=cfg,row=request.form if request.method=='POST' else {},choices=options(),mode='Add')

@app.route('/<table>/<int:record_id>')
def detail(table,record_id):
    cfg=config(table)
    row=fetch_one(f"SELECT * FROM {table} WHERE {cfg['pk']}=%s",(record_id,))
    if not row: abort(404)
    return render_template('detail.html',table=table,cfg=cfg,row=row)

@app.route('/<table>/<int:record_id>/edit',methods=['GET','POST'])
def edit(table,record_id):
    cfg=config(table)
    row=fetch_one(f"SELECT * FROM {table} WHERE {cfg['pk']}=%s",(record_id,))
    if not row: abort(404)
    if request.method=='POST':
        try:
            vals=parse_form(cfg)
            execute(f"UPDATE {table} SET "+','.join(f'{f}=%s' for f in vals)+f" WHERE {cfg['pk']}=%s",tuple(vals.values())+(record_id,))
            flash('Record updated.','success')
            return redirect(url_for('detail',table=table,record_id=record_id))
        except (ValueError,Error) as e: flash(str(e),'danger')
    return render_template('form.html',table=table,cfg=cfg,row=request.form if request.method=='POST' else row,choices=options(),mode='Edit')

@app.route('/<table>/<int:record_id>/delete',methods=['POST'])
def delete(table,record_id):
    cfg=config(table)
    try:
        execute(f"DELETE FROM {table} WHERE {cfg['pk']}=%s",(record_id,))
        flash('Record deleted.','success')
    except IntegrityError: flash('Cannot delete: this record is referenced by another record. Delete dependent records first.','danger')
    except Error as e: flash(str(e),'danger')
    return redirect(url_for('listing',table=table))

def rank_jobs(skills, jobs):
    wanted={s.casefold() for s in skills}
    ranked=[]
    for job in jobs:
        raw=job.get('requirements')
        try:
            req=json.loads(raw) if isinstance(raw,str) else (raw or {})
            required=req.get('required_skills',[]) if isinstance(req,dict) else []
            required=[str(s).strip() for s in required if str(s).strip()] if isinstance(required,list) else []
        except (ValueError,TypeError): required=[]
        if not required: continue
        matched=[s for s in required if s.casefold() in wanted]
        missing=[s for s in required if s.casefold() not in wanted]
        ranked.append(dict(job,score=round(100*len(matched)/len(required)),matched=matched,missing=missing,total=len(required)))
    return sorted(ranked,key=lambda x:(-x['score'],-len(x['matched']),x['job_title'].casefold()))

@app.route('/job-match',methods=['GET','POST'])
def job_match():
    skills_text=request.form.get('skills','') if request.method=='POST' else ''
    skills=list(dict.fromkeys(s.strip() for s in skills_text.split(',') if s.strip()))
    results=[]
    if request.method=='POST':
        jobs=fetch_all('SELECT j.*,c.company_name FROM jobs j JOIN companies c ON c.company_id=j.company_id')
        results=rank_jobs(skills,jobs)
    return render_template('job_match.html',skills_text=skills_text,skills=skills,results=results,submitted=request.method=='POST')

if __name__=='__main__':
    app.run(debug=os.getenv('FLASK_DEBUG','0')=='1')
