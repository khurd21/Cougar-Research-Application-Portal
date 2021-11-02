# tables.py
# Contains the tables needed for the many-to-many relationships


from app import db


programming_languages = db.Table('programming_languages',
                                db.Column('language_id', db.Integer, db.ForeignKey('programminglanguages.id'), primary_key=True),
                                db.Column('user_id', db.Integer, db.ForeignKey('user.id'). primary_key=True)
                                )


interested_fields   = db.Table('interested_fields', 
                                db.Column('field_id', db.Integer, db.ForeignKey('researchfield.id'), primary_key=True),
                                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                                )


fields              = db.Table('fields',
                                db.Column('field_id', db.Integer, db.ForeignKey('researchfield.id'), primary_key=True),
                                db.Column('position_id', db.Integer, db.ForeignKey('position.id'), primary_key=True)
                                )

applied_positions   = db.Table('applied_positions',
                                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                                db.Column('position_id', db.Integer, db.ForeignKey('position.id'), primary_key=True)
                                )
