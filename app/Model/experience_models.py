from app import db
from app.Model import tables


class ProgrammingLanguage(db.Model):

    __tablename__ = 'programminglanguages'

    id       = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(32), nullable=False)

    students = db.relationship('Student',
                secondary=tables.programming_languages, lazy='subquery',
                back_populates='programming_languages'
                )


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



class ResearchExperience(db.Model):

    __tablename__ = 'researchexperience'
    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title       = db.Column(db.String(64), nullable=False)
    company     = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    start_date  = db.Column(db.DateTime, nullable=False)
    end_date    = db.Column(db.DateTime, nullable=False)
   

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



class TechnicalElective(db.Model):

    __tablename__ = 'technicalelective'
    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_num  = db.Column(db.Integer, nullable=False)
    course_prefix = db.Column(db.String(8), nullable=False)
    course_title = db.Column(db.String(32), nullable=False)
    course_description = db.Column(db.String(256), nullable=False)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
