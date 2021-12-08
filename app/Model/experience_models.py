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

    
    def __repr__(self):
        return f'<ResearchExperience id: {self.id} student_id: {self.student_id} title: {self.title}>'



class TechnicalElective(db.Model):

    __tablename__ = 'technicalelective'
    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grade_id    = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False)

    course_num  = db.Column(db.Integer, nullable=False)
    course_prefix = db.Column(db.String(8), nullable=False)
    course_title = db.Column(db.String(32), nullable=False)
    course_description = db.Column(db.String(256), nullable=False)


    def get_grade(self):
        if (grade := Grade.query.filter_by(id=self.grade_id).first()):
            return grade.grade


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f'<TechnicalElective id: {self.id} student_id: {self.student_id} grade_id: {self.grade_id}'



class Grade(db.Model):

    id        = db.Column(db.Integer, primary_key=True)
    grade     = db.Column(db.String(2), nullable=False)
    students  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f'<Grade id: {self.id} grade: {self.grade}>'