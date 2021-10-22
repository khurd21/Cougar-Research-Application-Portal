from app import login, db
from datetime import datetime
from app.Model import user_models, tables



class ResearchField(db.Model):
    __tablename__ = 'researchfield'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(32), nullable=False)
    positions   = db.relationship('Position',
                                    secondary=tables.fields, lazy='subquery',
                                    back_populates='research_fields')
    students    = db.relationship('Student',
                                    secondary=tables.interested_fields, lazy='subquery',
                                    back_populates='interested_fields')

    def __repr__(self):
        return f'<ResearchField id: {self.id} name: {self.name}>'



class Position(db.Model):
    
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(32))
    description     = db.Column(db.String(1000))
    start_date      = db.Column(db.DateTime, default=datetime.utcnow)
    end_date        = db.Column(db.DateTime)
    time_commitment = db.Column(db.Integer)
    faculty_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    required_qualifications = db.Column(db.String(256))
    research_fields = db.relationship('ResearchField',
                        secondary=tables.fields, lazy='subquery',
                        back_populates='positions'
                        )

    students        = db.relationship('Student',
                        secondary=tables.applied_positions, lazy='subquery',
                        back_populates='applied_positions'
                        )


    def __repr__(self):
        return f'<Position id: {self.id} title: {self.title} faculty_id: {self.faculty_id}>'
