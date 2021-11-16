from app import login, db
from datetime import datetime
from app.Model import user_models, tables



class ResearchField(db.Model):
    '''
    A database model containing research field categories that are present at
    a given organization.

    :input positions relationship: A relationship between postitions and research fields
    :input students relationship: A relationship between students and interested fields (reserach fields)
    '''
    __tablename__ = 'researchfield'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(32), nullable=False)
    positions   = db.relationship('Position',
                                    secondary=tables.fields, lazy='subquery',
                                    back_populates='research_fields')
    students    = db.relationship('Student',
                                    secondary=tables.interested_fields, lazy='subquery',
                                    back_populates='interested_fields')
    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f'<ResearchField id: {self.id} name: {self.name}>'



class Position(db.Model):
    '''
    A database model containing information needed for a posted position. This includes
    start and end dates, faculty identification, description, title, etc.
    '''
    
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(32))
    description     = db.Column(db.String(1000))
    start_date      = db.Column(db.DateTime, default=datetime.utcnow)
    end_date        = db.Column(db.DateTime)
    time_commitment = db.Column(db.Integer)
    #faculty_object?
    faculty_name    = db.Column(db.String(32))
    faculty_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    application_forms= db.relationship('Application', backref='position', lazy=True)


    required_qualifications = db.Column(db.String(256))

    research_fields = db.relationship('ResearchField',
                        secondary=tables.fields, lazy='subquery',
                        back_populates='positions'
                        )

    students        = db.relationship('Student',
                        secondary=tables.applied_positions, lazy='subquery',
                        back_populates='applied_positions'
                        )

    def get_students(self):
        applications = Application.query.filter_by(position_id=self.id).all()
        return [x for x in applications]
    
    def get_research_fields(self):
        return self.research_fields


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f'<Position id: {self.id} title: {self.title} faculty_id: {self.faculty_id}>'




class Application(db.Model):

    id         = db.Column(db.Integer, primary_key=True)
    position_id= db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_name = db.Column(db.String(32), nullable=False)
    description= db.Column(db.String(256), nullable=False)
    ref_name   = db.Column(db.String(32), nullable=False)
    ref_email  = db.Column(db.String(64), nullable=False)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f'<Application id: {self.id} pos_id: {self.position_id} stu_id: {self.student_id} description: {self.description[:16]}>'