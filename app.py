from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()
OWNER = os.getenv('OWNER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
HEROKU_URI = os.getenv('HEROKU_URI')

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    # Sets database location
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + str(OWNER) + ':' + str(DB_PASSWORD) + '@localhost/dnd'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://plwquqdmkziorw:b1bc4f04549868c5495efde4b62dbfa1c13f8eded2f218eab3f9078bd80e8089@ec2-54-91-178-234.compute-1.amazonaws.com:5432/d7tk3fs4asvj52'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creates a db object, to reference. Use this to query the db
db = SQLAlchemy(app)

class Monster(db.Model):
    __tablename__ = 'monster'
    id = db.Column(db.BigInteger, primary_key=True)
    monster = db.Column(db.String(200), nullable=False)
    ac = db.Column(db.Integer, nullable=False)
    max_hp = db.Column(db.Integer, nullable=False)
    damage_taken = db.Column(db.Integer)
    current_hp = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(200))

    def __init__(self, monster, ac, max_hp, current_hp, notes):
        self.monster = monster
        self.ac = ac
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.notes = notes

@app.route('/')
def index():
    # cur = con.cursor()
    # cur.execute("SELECT * FROM monster")
    # data_ret = cur.fetchall()
    data_ret = db.session.query(Monster)
    for row in data_ret:
        print(row.monster, end=' ')
        print(row.ac, end=' ')
        print(row.max_hp)
    return render_template('index.html', data=data_ret)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        monster = request.form['monster']
        ac = request.form['ac']
        max_hp = request.form['max HP']
        current_hp = request.form['current HP']
        notes = request.form['notes']
        if monster == '' or ac == '' or max_hp == '':
            return render_template('index.html', message = 'You forgot to enter monster, AC, or Max HP')
        # print(monster, ac, max_hp)
        data = Monster(monster, ac, max_hp, current_hp, notes)
        db.session.add(data)
        db.session.commit()
        return render_template('index.html')



if __name__ == '__main__':
    app.debug = True            # This will make the server keep reloading while developing
    app.run()
