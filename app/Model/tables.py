from app import db


interested_fields = db.Table('interested_fields', 
                                db.Column('field_id', db.Integer, db.ForeignKey('researchfield.id'), primary_key=True),
                                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                                )


fields = db.Table('fields',
                    db.Column('field_id', db.Integer, db.ForeignKey('researchfield.id'), primary_key=True),
                    db.Column('position_id', db.Integer, db.ForeignKey('position.id'), primary_key=True)
                    )

applied_positions = db.Table('applied_positions',
                                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                                db.Column('position_id', db.Integer, db.ForeignKey('position.id'), primary_key=True)
                                )
