# Cougar Research Application Portal

--------
**Prepared by:**

* `Kyle Hurd`,`Copy&Submit(CS)`
* `AbdulAziz Al-Dalaan`,`Copy&Submit(CS)`
* `Jake Berreth`, `Copy&Submit(CS)`

---

**Course** : CptS 322 - Software Engineering Principles I

**Instructor**: Sakire Arslan Ay

---

Our group, `Copy & Submit`, created a research application portal for faculty members to recruit
students for research positions. This was for a term project in Cpts 322, Software Engineering Principles I
at Washington State University.

## Previews

#### Index

![](documents/readme_imgs/user_interface_imgs/index.png)

#### Login

![](documents/readme_imgs/user_interface_imgs/login.png)


#### Active Research Positions

![](documents/readme_imgs/user_interface_imgs/active_research_positions.png)

## Set Up

If running on MacOS or Linux, you can do the following:  

```
python -m venv venv
pip install -r requirements.txt
./run.sh
```

The `reset_db.sh` file can be used to wipe and repopulate the database with information from
`populate_database.py`.
