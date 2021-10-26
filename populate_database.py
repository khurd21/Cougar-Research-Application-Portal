from app import db, create_app
from app.Model import user_models, position_models

app = create_app()
app.app_context().push()

db.create_all()

if position_models.ResearchField.query.count() == 0:
    fields = [
            'Electronic Design Automation (EDA)',           'High Performance Computing & Scalable Data Science',
            'Artificial Intelligence & Machine Learning',   'Bioinfomatics',
            'Distributed & Networked Systems',              'Power Engineering',
            'Systems Engineering',                          'Software Engineering'
            ]

    for field in fields:
        db.session.add(position_models.ResearchField(name=field))

    db.session.commit()

s1 = user_models.Student()
s1.username = 'Student123'
s1.email = 'student123@wsu.edu'
s1.first_name = 'John'
s1.last_name = 'Doe'
s1.set_password('123')
s1.phone_number = '5098823444'
s1.wsu_id = 915334469

fields = position_models.ResearchField.query.all()

for i in range(2):
    s1.interested_fields.append(fields[i])

f1 = user_models.Faculty()
f1.first_name = 'Dr. Jane'
f1.last_name = 'Foster'
f1.email = 'janefoster@wsu.edu'
f1.phone_number = '4429876543'
f1.username = 'Faculty123'
f1.set_password('123')
f1.wsu_id = 915443123
f1.interested_fields = fields[:3]
f1.save_to_db()

from datetime import datetime, timedelta

p1 = position_models.Position(faculty_id=f1.id)
p1.start_date = datetime.utcnow()
p1.end_date = datetime.utcnow() + timedelta(days=30)
p1.faculty_name = f1.first_name
p1.required_qualifications = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit,' \
        ' sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'

p1.description = 'Est ante in nibh mauris cursus mattis molestie a. Dui nunc mattis' \
        'enim ut tellus. Facilisis volutpat est velit egestas dui. Nec feugiat nisl pretium' \
        ' fusce id velit ut tortor pretium. Donec et odio pellentesque diam volutpat commodo sed.' \
        ' Commodo elit at imperdiet dui accumsan sit amet. Id donec ultrices tincidunt arcu' \
        ' non sodales neque sodales. Vitae congue mauris rhoncus aenean vel elit. ' \
        'Ultricies tristique nulla aliquet enim tortor. Lectus proin nibh nisl condimentum.'
p1.time_commitment = 20
p1.research_fields = fields[:-3]
p1.title = 'Nunc faucibus'
p1.save_to_db()



p2 = position_models.Position(faculty_id=f1.id)
p2.start_date = datetime.utcnow()
p2.end_date = datetime.utcnow() + timedelta(days=600)
p2.faculty_name = f1.first_name
p2.required_qualifications = 'Viverra accumsan in nisl nisi scelerisque. Lorem ipsum dolor sit amet.' \
        ' Placerat duis ultricies lacus sed. Neque egestas congue quisque egestas diam in arcu' \
        ' cursus euismod. Mi bibendum neque egestas congue quisque egestas diam in arcu.' \
        ' Nisi lacus sed viverra tellus in hac habitasse platea. Diam quam nulla porttitor' \
        ' massa id neque aliquam vestibulum morbi.'

p2.description = 'Consequat semper viverra nam libero justo laoreet sit amet cursus. Aliquam' \
        ' vestibulum morbi blandit cursus risus at ultrices mi tempus. Tempus quam pellentesque' \
        ' nec nam aliquam sem et tortor.'
p2.time_commitment = 20
p2.research_fields = fields[:-3]
p2.title = 'Porttitor leo'
p2.save_to_db()

f2 = user_models.Faculty()
f2.first_name = 'Prof. Dido'
f2.last_name = 'Pelican'
f2.email = 'didopelican@wsu.edu'
f2.phone_number = '4439876543'
f2.username = 'Dido123'
f2.set_password('123')
f2.wsu_id = 914443123
f2.save_to_db()

p3 = position_models.Position(faculty_id=f2.id)
p3.start_date = datetime.utcnow()
p3.end_date = datetime.utcnow() + timedelta(days=29)
p3.faculty_name = f1.first_name
p3.required_qualifications = 'Auctor neque vitae tempus quam. Integer enim neque volutpat' \
        ' ac tincidunt vitae semper. Sed viverra tellus in hac habitasse platea. Semper' \
        ' quis lectus nulla at volutpat diam ut venenatis. Nibh sed pulvinar proin gravida.'

p3.description = 'Orci a scelerisque purus semper eget duis at tellus. Fames ac turpis' \
        ' egestas maecenas pharetra. Ultrices dui sapien eget mi proin sed libero. Mauris' \
        ' pellentesque pulvinar pellentesque habitant morbi tristique senectus.'
p3.time_commitment = 20
p3.research_fields = fields[-3:-1]
p3.title = 'Ut ornare'
p3.save_to_db()
