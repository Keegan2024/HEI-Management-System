from flask_sqlalchemy import SQLAlchemy
name = db.Column(db.String(140), unique=True, nullable=False)
district = db.Column(db.String(120))
province = db.Column(db.String(120))
users = db.relationship('User', backref='facility', lazy=True)
children = db.relationship('Child', backref='facility', lazy=True)


class User(db.Model):
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(80), unique=True, nullable=False)
password_hash = db.Column(db.String(200), nullable=False)
role = db.Column(db.String(50), default='facility')
facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))


class Child(db.Model):
id = db.Column(db.Integer, primary_key=True)
mother_name = db.Column(db.String(140))
art_number = db.Column(db.String(80))
village = db.Column(db.String(120))
child_name = db.Column(db.String(140))
dob = db.Column(db.Date, nullable=False)
facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
status = db.Column(db.String(50), default='Active')
tests = db.relationship('EIDTest', backref='child', lazy=True, cascade='all, delete-orphan')


def create_tests(self):
"""Auto-generate the 7 EID tests when a child is registered."""
milestones = [
("At Birth", 0, 'days'),
("6 Weeks", 42, 'days'),
("6 Months", 6, 'months'),
("9 Months", 9, 'months'),
("12 Months", 12, 'months'),
("18 Months", 18, 'months'),
("24 Months", 24, 'months'),
]
for stage, offset, kind in milestones:
if kind == 'days':
due = self.dob + relativedelta(days=offset)
else:
due = self.dob + relativedelta(months=offset)
t = EIDTest(stage=stage, due_date=due)
self.tests.append(t)


class EIDTest(db.Model):
id = db.Column(db.Integer, primary_key=True)
stage = db.Column(db.String(50))
due_date = db.Column(db.Date)
done_date = db.Column(db.Date, nullable=True)
result = db.Column(db.String(50), nullable=True)
reason = db.Column(db.String(80), nullable=True)
remarks = db.Column(db.String(250), nullable=True)
child_id = db.Column(db.Integer, db.ForeignKey('child.id'))


@property
def status(self):
if self.reason:
return f"Exception: {self.reason}"
if self.done_date:
return "Done"
today = date.today()
if self.due_date < today:
return "Overdue"
if self.due_date == today:
return "Due Today"
return "Upcoming"
