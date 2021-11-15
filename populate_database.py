from app import db, create_app
from app.Model import user_models, position_models, experience_models
from datetime import datetime, timedelta


app = create_app()
app.app_context().push()

db.create_all()


S = user_models.Student
F = user_models.Faculty

## STUDENTS
# ----------------------------------------------------------------------------------------------------------------------
s1 = S()
s1.username = 'Student123'
s1.email = 'student123@wsu.edu'
s1.first_name = 'John'
s1.last_name = 'Doe'
s1.set_password('123')
s1.phone_number = '5098823444'
s1.wsu_id = 915334469
s1.gpa = 3.5
s1.save_to_db()


s2 = S()
s2.username = 'Student223'
s2.email = 'student223@wsu.edu'
s2.first_name = 'Mary'
s2.last_name = 'Jane'
s2.set_password('123')
s2.phone_number = '5098723459'
s2.wsu_id = 914334469
s2.gpa = 4.0
s2.save_to_db()


s3 = S()
s3.username = 'Student233'
s3.email = 'student233@wsu.edu'
s3.first_name = 'Marco'
s3.last_name = 'Polo'
s3.set_password('123')
s3.phone_number = '5098623029'
s3.wsu_id = 914334569
s3.gpa = 2.31
s3.save_to_db()


## FACULTY
# ----------------------------------------------------------------------------------------------------------------------
f1 = F()
f1.first_name = 'Dr. Jane'
f1.last_name = 'Foster'
f1.email = 'janefoster@wsu.edu'
f1.phone_number = '4429876543'
f1.username = 'Faculty123'
f1.set_password('123')
f1.wsu_id = 915443123
f1.save_to_db()


f2 = F()
f2.first_name = 'Prof. Dido'
f2.last_name = 'Pelican'
f2.email = 'didopelican@wsu.edu'
f2.phone_number = '4439876543'
f2.username = 'Dido123'
f2.set_password('123')
f2.wsu_id = 914443123
f2.save_to_db()




if position_models.ResearchField.query.count() == 0:

    fields = [
            'Electronic Design Automation (EDA)',           'High Performance Computing & Scalable Data Science',
            'Artificial Intelligence & Machine Learning',   'Bioinfomatics',
            'Distributed & Networked Systems',              'Power Engineering',
            'Systems Engineering',                          'Software Engineering'
            ]


    languages = [
            'C/C++', 'C#', '.NET', 'Haskell', 'Java', 'JavaScript', 'PowerShell', 'Python',
            'Pearl', 'SQL', 'R', 'Ruby', 'Rust', 'Swift', 'SystemVerilog', 'TeX', 'VHDL',
            'PHP', 'Objective-C', 'MatLab', 'Assembly', 'Go'
            ]
    languages = sorted(languages)

    for field in fields:
        db.session.add(position_models.ResearchField(name=field))

    for language in languages:
        db.session.add(experience_models.ProgrammingLanguage(language=language))

    db.session.commit()



languages   = experience_models.ProgrammingLanguage.query.all()
fields      = position_models.ResearchField.query.all()


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
p1.research_fields = fields[-4:-1]
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


p3 = position_models.Position(faculty_id=f2.id)
p3.start_date = datetime.utcnow()
p3.end_date = datetime.utcnow() + timedelta(days=29)
p3.faculty_name = f2.first_name
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



## Checking for users
s1_q = user_models.Student.query.filter_by(username=s1.username).first()
assert s1_q is not None
assert s1_q is s1
f1_q = user_models.Faculty.query.filter_by(username=f1.username).first()
assert f1_q is not None


## Checking for languages
languages1 = experience_models.ProgrammingLanguage.query.all()
assert len(languages1) == len(languages)
s1_q.programming_languages = languages1[3:7]
s2.programming_languages = languages1[0:3]
s3.programming_languages = languages1[-4:-1]


## Checking for fields being added
fields1 = position_models.ResearchField.query.all()
assert len(fields1) == len(fields)
for i in range(len(fields)):
        assert fields[i].name == fields1[i].name


## Adding interested fields to students
s1.interested_fields = fields1[0:2]
s1.interested_fields.append(fields1[-1])
s2.interested_fields = fields1[1:3]
s3.interested_fields = fields1[-1::-2]

exp1 = experience_models.ResearchExperience(student_id=s1.id)
exp1.company = 'Unversity of California, Berkley'
exp1.title = 'Research Assistant'
exp1.start_date = datetime(2018, 1, 1)
exp1.end_date = datetime(2018, 12, 31)
exp1.description = 'At varius vel pharetra vel turpis nunc eget lorem. ' \
    'Enim nec dui nunc mattis enim. Est lorem ipsum dolor sit amet consectetur' \
        'adipiscing elit pellentesque. Egestas congue quisque egestas diam in arcu' \
            'cursus euismod quis. Nisl nisi scelerisque eu ultrices vitae auctor eu.'
exp1.save_to_db()


exp2 = experience_models.ResearchExperience(student_id=s2.id)
exp2.company = 'University of Washington'
exp2.title = 'Teacher Assistant'
exp2.start_date = datetime(2017, 1, 1)
exp2.end_date = datetime(2017, 12, 31)
exp2.description = 'Ultricies leo integer malesuada nunc vel risus. Arcu non odio euismod' \
    'lacinia at. Ullamcorper sit amet risus nullam eget felis eget nunc lobortis. Malesuada' \
        'fames ac turpis egestas integer eget aliquet nibh. Ut aliquam purus sit amet luctus venenatis lectus.'
exp2.save_to_db()
    

exp3 = experience_models.ResearchExperience(student_id=s1.id)
exp3.company = 'Washington State University'
exp3.title = 'Software Engineer'
exp3.start_date = datetime(2016, 1, 1)
exp3.end_date = datetime(2016, 12, 31)
exp3.description = 'Integer quis auctor elit sed vulputate. Convallis aenean et tortor at risus viverra.' \
    'Senectus et netus et malesuada fames ac turpis egestas. Sed viverra ipsum nunc aliquet bibendum enim' \
        'facilisis. Pellentesque habitant morbi tristique senectus. Iaculis nunc sed augue lacus viverra.' \
            'Amet venenatis urna cursus eget nunc scelerisque viverra mauris.'
exp3.save_to_db()


exp4 = experience_models.ResearchExperience(student_id=s3.id)
exp4.company = 'Electric Co.'
exp4.title = 'Data Scientist'
exp4.start_date = datetime(2015, 1, 1)
exp4.end_date = datetime(2015, 12, 31)
exp4.description = 'Est velit egestas dui id ornare arcu odio ut. Et netus et malesuada fames ac.' \
    'Nec feugiat nisl pretium fusce id velit ut tortor pretium. Quisque id diam vel quam elementum pulvinar etiam non quam.'


tech1 = experience_models.TechnicalElective(student_id=s1.id)
tech1.course_title = 'Introduction to Python'
tech1.course_prefix = 'CPTS'
tech1.course_num = '101'
tech1.save_to_db()


tech2 = experience_models.TechnicalElective(student_id=s2.id)
tech2.course_title = 'Software Engineering 1'
tech2.course_prefix = 'CPTS'
tech2.course_num = '322'
tech2.save_to_db()


tech3 = experience_models.TechnicalElective(student_id=s2.id)
tech3.course_title = 'Programming Language Design'
tech3.course_prefix = 'CPTS'
tech3.course_num = '355'
tech3.save_to_db()


tech4 = experience_models.TechnicalElective(student_id=s3.id)
tech4.course_title = 'Neural Network Design'
tech4.course_prefix = 'CPTS'
tech4.course_num = '434'
tech4.save_to_db()


app1 = position_models.Application(student_id=s1.id, position_id=p1.id)
app1.description = 'Etiam tempor orci eu lobortis elementum nibh tellus molestie.' \
    'Ac feugiat sed lectus vestibulum mattis ullamcorper velit sed ullamcorper.' \
        'Et ultrices neque ornare aenean euismod elementum nisi. Ultrices tincidunt arcu non sodales.' \
            'Accumsan lacus vel facilisis volutpat est. Pellentesque nec nam aliquam sem et tortor consequat id porta.'
app1.ref_name = 'Dr. Calico Cat'
app1.ref_email = 'calico_cat@edi.edu'
app1.save_to_db()


app2 = position_models.Application(student_id=s2.id, position_id=p2.id)
app2.description = 'Facilisis magna etiam tempor orci eu. Tortor id aliquet' \
    'lectus proin nibh nisl condimentum id. Suspendisse in est ante in nibh mauris cursus.' \
        'Massa tempor nec feugiat nisl pretium fusce id.'
app2.ref_name = 'Jackson Donner'
app2.ref_email = 'jackson_donner@test.com'
app2.save_to_db()


app3 = position_models.Application(student_id=s1.id, position_id=p3.id)
app3.description = 'Etiam tempor orci eu lobortis elementum nibh tellus molestie.' \
    'Ac feugiat sed lectus vestibulum mattis ullamcorper velit sed ullamcorper.' \
        'Nibh mauris cursus mattis molestie a iaculis. Cras adipiscing enim eu turpis egestas pretium aenean pharetra.'
app3.ref_name = 'Dr. Helmer Glue'
app3.ref_email = 'helmerg@ghi.edu'
app3.save_to_db()

db.session.commit()


test_app = position_models.Application.query.filter_by(student_id=s1.id).all()
assert len(test_app) == 2
for t in test_app:
    print(t)


## Display contents to ensure accuracy
print(f'Student 1: \n{s1}')
print(f'RE: {s1.research_experience}')
print(f'AP: {s1.applied_positions}')
print(f'TE: {s1.technical_electives}')
print(f'IF: {s1.interested_fields}')


print(f'Student 2: \n{s2}')
print(f'RE: {s2.research_experience}')
print(f'AP: {s2.applied_positions}')
print(f'TE: {s2.technical_electives}')
print(f'IF: {s2.interested_fields}')


print(f'Student 3: \n{s3}')
print(f'RE: {s3.research_experience}')
print(f'AP: {s3.applied_positions}')
print(f'TE: {s3.technical_electives}')
print(f'IF: {s3.interested_fields}')