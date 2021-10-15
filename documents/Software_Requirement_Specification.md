# Software Requirements Specification

## Cougar Research Application Portal
 
--------
**Prepared by:**

* `Kyle Hurd`,`Copy&Submit(CS)`
* `AbdulAziz Al-Dalaan`,`Copy&Submit(CS)`
* `Jake Berreth`, `Copy&Submit(CS)`

---

**Course** : CptS 322 - Software Engineering Principles I

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [Software Requirements Specification](#software-requirements-specification)
  - [Cougar Research Application Portal](#cougar-research-application-portal)
  - [Table of Contents](#table-of-contents)
  - [Document Revision History](#document-revision-history)
- [1. Introduction](#1-introduction)
  - [1.1 Document Purpose](#11-document-purpose)
  - [1.2 Product Scope](#12-product-scope)
  - [1.3 Document Overview](#13-document-overview)
- [2. Requirements Specification](#2-requirements-specification)
  - [2.1 Customer, Users, and Stakeholders](#21-customer-users-and-stakeholders)
  - [2.2 Use Cases](#22-use-cases)
    - [2.2.1 Student Use Cases](#221-student-use-cases)
    - [2.2.2 Faculty Use Cases](#222-faculty-use-cases) 
  - [2.3 Non-Functional Requirements](#23-non-functional-requirements)
- [3. User Interface](#3-user-interface)
    - [3.1 Student User Interface](#31-student-user-interface)
    - [3.2 Faculty User Interface](#32-faculty-user-interface)
- [4. References](#4-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

## Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2021-10-05 |Initial draft | 1.0        |

----
# 1. Introduction

This document is an overview of the Cougar Research Application Portal project. It includes Table of Contents and Document Revision History sections for easy navigation and version management. It also includes an introduction section that consists of this statement, Document Purpose, Product Scope, and Document Overview sections. These introduce the Software Requirement Specification document and the product that is being created. Following the list of use-cases is a swim-lane diagram, a list of non-functional requirements, a user interface diagram, and a list of references used in the creation of this document and the product. 

## 1.1 Document Purpose

The purpose of the Software Requirement Specification (SRS) document is to outline the functions that the software must perform. This specification is useful because it may be read by the designers of the product to guide the planning and implementation process. It also provides clear documentation, which allows for transparency and minimizes confusion. This is essential because it limits the chances for the product implementation to stray from the initial needs of the client/customer. The document is intended to be read by the product designers/creators and the client. It should only be directly edited by the product designers/creators. 

## 1.2 Product Scope

At Washington State University, there are opportunities for undergradutae students to become involved in research. However, there is not always effective communication between faculty and students about these opportunities. Therefore, there is a need for an online platform that will enable faculty to advertise research positions that students may apply for. The product that will be created is a web application where:
-students can enter their contact information, completed coursework, research interests, and prior research experience
-faculty can advertise research opportunities for undergraduate students
-students can apply for research positions
-faculty can select the candidates that they would like to interview for the position

## 1.3 Document Overview

The next section is the Requirement Specification. This includes a list of use-cases, a swim-lane diagram, and a list of non-functional requirements. Following this is a user interface diagram and a list of references used in the creation of this document and the product. 

----
# 2. Requirements Specification

This section specifies the software product's requirements. 

## 2.1 Customer, Users, and Stakeholders

**Customers:** Faculty  
**Users:** Faculty, students  
**Stakeholders:** Faculty, students, Washington State University  

----
## 2.2 Use Cases

The use cases for the software that will be created, are listed below. This section includes two categories, which are "Student Use Cases" and "Faculty Use Cases."

---

### 2.2.1 Student Use Cases

| Use case # 1      |   |
| ------------------|-- |
| **Name**              | Create Student Account |
| **Users**             | Students |
| **Rationale**         | When students apply for research positions, the faculty will need some way of tracking who has applied for which positions. This can by done by allowing students to create an account that includes contact information, completed coursework, research interests, and prior research experience. This will organize the student's information under an account so it is easily viewable and managable. |
| **Triggers**          | User selects create account option |
| **Preconditions**     | User is a student at WSU |
| **Actions**           | **1.** The user indicates that the software is to perform the functionality of creating a student account. <br/> **2.** The software responds by requesting the create account functionality. <br/> **3.** The user inputs registration information and creates an account. <br/> **4.** The software registers the user and creates an account for them. |
| **Alternative paths** | **1.** In step 3, the user does not want to create an account and indicates this. Then, the software responds by exiting the registration functionality.  |
| **Postconditions**    | The user has created an account.  |
| **Acceptance tests**  | Make sure the user has a corresponding account.  |
| **Iteration**         | 1 |

<br/><br/>

| Use case # 2      |   |
| ------------------|-- |
| **Name**              | Student Login |
| **Users**             | Students |
| **Rationale**         | When users apply to a position, there needs to be a way to verify whether the user is in fact a student, prior to accessing the application. By making it so that a student enters the proper credentials on a page before accessing the full capabilities of the application, we will be able to know that the user is a student. |
| **Triggers**          | Users selects the login option. |
| **Preconditions**     | User has created a student account |
| **Actions**           |   **1.** The user indicates that the software is to perform a student login operation. <br/> **2.** The software responds by prompting the user for a username and password. <br/> **3.** The user enters the proper student credentials (username and password), then indicates to login <br/> **4.** The software responds by logging in the user if the credentials are correct. |
| **Alternative paths** | **1.** The user indicates that the software is to perform a student login operation. <br/> **2.** The software responds by prompting the user for a username and password. <br/> **3.** The user enters the incorrect student credentials (username and password), then indicates to login. <br/> **4.** The software responds by prompting the user to create a student account. |
| **Postconditions**    |  The user is logged in as a student |
| **Acceptance tests**  |  Make sure the user logs in only with the proper student credentials. <br/>
Make sure the user is logged in. |
| **Iteration**         |  1 |

<br/><br/>

| Use case # 3      |   |
| ------------------| -- |
| **Name**              | View Open Research Positions |
| **Users**             | Students |
| **Rationale**         | Students using this application will be searching for research opportunities at their university. It is necessary to create a convenient way for students to view positions that professors are actively wishing to find a student researcher for. |
| **Triggers**          | User selects the open research position option |
| **Preconditions**     | User has already created an account |
| **Actions**           | **1.** The user indicates that they want to view open research positions. <br/> **2.** The software responds by displaying the current open research positions. |
| **Alternative paths** |   |
| **Postconditions**    | The user is now able to view the open research positions.  |
| **Acceptance tests**  | Ensure the open research positions are displayed.  |
| **Iteration**         | 1 |

<br/><br/>

| Use case # 4      |   |
| ------------------| -- |
| **Name**              | Display Research Position Information |
| **Users**             | Students, faculty |
| **Rationale**         |  When students look for a research position, they will need to have to ability to view open research position information so that they can choose which positions match their interests and which positions they would like to apply for. Faculty need a way to advertise positions they are wishing to fill. By displaying research position information, they can inform students about research positions, which will increase the chances of receiving strong candidate applications. |
| **Triggers**          | User selects view research information option |
| **Preconditions**     | User is logged in |
| **Actions**           | **1.** The user indicates that the software is to display the research position information for a research position. <br> 2. The software responds by displaying the information corresponding to the selected research position. |
| **Alternative paths** |   |
| **Postconditions**    | The research position information is displayed |
| **Acceptance tests**  | Ensure sure the research position information is displayed |
| **Iteration**         |  1 |

<br/><br/>

| Use case # 5      |   |
| ------------------| -- |
| **Name**              | Apply for Research Position |
| **Users**             | Students |
| **Rationale**         | When students find a research position they want, they will need to have the ability to apply for that position. This will allow students to submit an application for a research position, so that they can be considered for it. |
| **Triggers**          | User selects apply option  |
| **Preconditions**     | User is logged in as a student  |
| **Actions**           | **1.** The user indicates that the software is to perform apply for position funcationality. <br> **2.** The software responds by allowing the user to apply for a research position. </br> **3.** The user enters application information. <br> **4.** The software responds by submitting the student application.|
| **Alternative paths** | **1**. In step 3, the user decides they want to stop applying for a position. The software responds by exiting the apply functionality.  |
| **Postconditions**    | The user has applied for a position |
| **Acceptance tests**  | Make sure the user's application corresponds to the user's account |
| **Iteration**         |  2 |

<br/><br/>


| Use case # 6      |   |
| ------------------ |--|
| **Name**              | View Applied For Application and Check Application Status |
| **Users**             | Students |
| **Rationale**         | When students have applied for research positions, there needs to be a way for them to check the research positions that they have applied to and check on the current state of their application. |
| **Triggers**          |  User selects the status option |
| **Preconditions**     |  User is logged in as a student |
| **Actions**           |  **1.** The user indicates they want to view the status of their application(s). <br/> **2.** The software responds by displaying their applications and the status of the applications that they have applied to. |
| **Alternative paths** | **1.** The student indicates that they want to view the status of their application(s). <br/> **2.** The software responds by displaying that the user has no current applications that they have applied for. |
| **Postconditions**    |  The status of the user's application(s) is displayed and that the correct application status is displayed. |
| **Acceptance tests**  |  Make sure the correct status is displayed for each applied for application. </br> Make sure all displayed applications are currently applied for by the user. |
| **Iteration**         | 2 |

<br/><br/>

| Use case # 7      |   |
| ------------------ |--|
| **Name**              | Widthdraw a Pending Application |
| **Users**             | Student |
| **Rationale**         | When a user applies for a position, they could have made a typo or mistakenly applied for the wrong position. This will be remedied by allowing the user to withdraw a pending application. |
| **Triggers**          | User indicates they want to retract their application  |
| **Preconditions**     | User has applied to the research position they wish to withdraw |
| **Actions**           | **1.** The user indicates they want to withdraw an application. <br/> **2.** The software responds by removing their application from the selected position. |
| **Alternative paths** | |
| **Postconditions**    | The user's application is removed. |
| **Acceptance tests**  | Make sure the user's selected application is removed. |
| **Iteration** | 1|

<br/><br/>

---

### 2.2.2 Faculty Use Cases


| Use case # 1      |   |
| ------------------|-- |
| **Name**              | Create Faculty Account |
| **Users**             | Faculty |
| **Rationale**         | When students apply for research positions, the faculty will need some way of tracking who has applied for their positions. They also need to be able to post their own research positions. This can be done by allowing faculty members to create an account. This will organize the faculty member's information and positions under an account so it is easily viewable and managable. |
| **Triggers**          | User selects create account option |
| **Preconditions**     | User is a faculty member at WSU |
| **Actions**           | **1.** The user indicates that the software is to perform the functionality of creating a faculty account. <br/> **2.** The software responds by requesting the create account functionality. <br/> **3.** The user inputs registration information and indicates they want to create an account. <br/> **4.** The software registers the user. |
| **Alternative paths** | **1.** In step 3, the user does not want to create an account and indicates this. Then, the software responds by exiting registration functionality. |
| **Postconditions**    | The user has created an account. |
| **Acceptance tests**  | Make sure the user has a corresponding account. |
| **Iteration**         | 1 |

<br/><br/>

| Use case # 2      |   |
| ------------------|-- |
| **Name**              | Faculty Login |
| **Users**             | Faculty |
| **Rationale**         | When users register and create positions, there needs to be a way to properly verify whether the user is in fact a faculty member. Therefore, by requiring a faculty member to enter the proper credentials before accessing the full capabilities of a faculty member (create positions), we will verify that the user is a faculty member. |
| **Triggers**          |  User selects the login option. |
| **Preconditions**     | User has already created a faculty account |
| **Actions**           |   **1.** The user indicates that the software is to perform a faculty login operation. <br/> **2.** The software responds by prompting for a username and password. <br/> **3.** The user enters the proper credentials (username and password), then indicates to login. <br/> **4.** The software responds by logging in the user if the credentials are correct. |
| **Alternative paths** | **1.** The user indicates that the software is to perform a student login operation. <br/> **2.** The software responds by prompting the user for a username and password. <br/> **3.** The user enters the incorrect student credentials (username and password), then indicates to login. <br/> **4.** The software responds by prompting the user to create a faculty account. |
| **Postconditions**    |  The user is logged in as a faculty member |
| **Acceptance tests**  |  Make sure that the user logs in only with the proper Faculty credentials. </br> Make sure the user is logged in.   |
| **Iteration**         |  1 |

<br/><br/>

| Use case # 3      |   |
| ------------------|-- |
| **Name**              | Create Undergraduate Research Position |
| **Users**             | Faculty |
| **Rationale**         | A main purpose of this product is to allow faculty to advertise research positions to students. In order to this, they will need to have the ability to create a research positions that students can apply for. |
| **Triggers**          |  User selects create position option. |
| **Preconditions**     | User has created a faculty account |
| **Actions**           |   **1.** The user indicates that the software is to create a research position. <br/> **2.** The software responds by prompting the faculty member for position information. <br/> **3.** The user enters the information. <br/> **4.** The software responds by creating the position based on the information entered by the user. |
| **Alternative paths** | **1.** In step 3, the user decides they do not want to create the position. The software responds by exiting create position functionality. |
| **Postconditions**    |  The user has created a research position. |
| **Acceptance tests**  |  Make sure the research position corresponds to the faculty account.   |
| **Iteration**         |  2 |

<br/><br/>

| Use case # 4      |   |
| ------------------ |--|
| **Name**              | View Position Applicants and Application Status |
| **Users**             | Faculty |
| **Rationale**         | Faculty users will need to see all of the students who wish to be considered for the posted research position. This is so the faculty member(s) can make an informed decision about who they want to interview and hire. It will also be important for faculty to be able to view the status of an applicant's application, so they know who will be interviewed or hired for the position. |
| **Triggers**          | User selects display position applicants option |
| **Preconditions**     | Research position is open |
| **Actions**           | **1.** The user indicates they want to view the students who have applied for the research position. <br/> **2.** The software responds by displaying the students who have applied for the position and the application status. |
| **Alternative paths** |  |
| **Postconditions**    | Position applicants are displayed  |
| **Acceptance tests**  | Make sure the applicants for the selected research position only are displayed |
| **Iteration**         | 2 |

<br><br>

| Use case # 5      |   |
| ------------------|-- |
| **Name**              | View Student Qualifications |
| **Users**             | Faculty |
| **Rationale**         | When a faculty member wants to choose a student for their research position, they will need to view students' applications, so that they can compare them and decide on the best candidate.  |
| **Triggers**          | User selects view qualifications option |
| **Preconditions**     | User has created a faculty account |
| **Actions**           |   **1.** The user indicates that the software is to perform student qualifications functionality. <br/> **2.** The software responds by prompting faculty member for student information. <br/> **3.** The user enters the student information. <br/> **4.** The software responds by displaying student qualifications. |
| **Alternative paths** | **1.** In step 3, the user decides they do not want to view student qualifications. The software responds by exiting view qualifications functionality. |
| **Postconditions**    | The student qualifications are displayed |
| **Acceptance tests**  | Make sure the student qualifications are being displayed |
| **Iteration**         |  2 |

<br/><br/>

| Use case # 6      |   |
| ------------------ |--|
| **Name**              | Approve Student for Interview |
| **Users**             | Faculty |
| **Rationale**         | Once a faculty member has viewed a student's qualifications, there needs to be a way to approve the student for an interview. This way, it will be easy for faculty to keep track of who they want to interview. |
| **Triggers**          | The user selects the approve for interview option |
| **Preconditions**     | The student that faculty are looking to approve or not approve has applied for the reasearch position. </br> The user is logged in. |
| **Actions**           |  **1.** The user indicates they want to approve an applicant for an interview. <br/> **2.** The software responds by prompting the user to select the student they want to approve. <br/> **3.** The user indicates that they are approving the student for an interview or not. <br/> **4.** The software responds by updating the student user's application status depending on the faculty user's choice. |
| **Alternative paths** |**1.** In step 3, the user indicates they do not want to approve or not approve a student's application. The software responds by exiting approve student functionality.  |
| **Postconditions**    | The student user's application status is updated to signify they are approved for an interview |
| **Acceptance tests**  | Make sure the student user's application has the correct status of being approved or not. |
| **Iteration**         | 3 |

<br/><br/>

| Use case # 7      |   |
| ------------------|-- |
| **Name**              | Update Application Status |
| **Users**             | Faculty |
| **Rationale**         | When a faculty member wants to let students know if a position is closed or not, they can change the status of the application to reflect if someone has been hired for it or not hired. This allows faculty to keep a position posted, but easily close or open it. This will also allow students to make note of positions they may want in the future, but that are currently closed. |
| **Triggers**          | User selects update application option |
| **Preconditions**     | User has created an account <br> The application exists. |
| **Actions**           |   **1.** The user indicates that the software is to update an application. <br/> **2.** The software responds by prompting the user for new status. <br/> **3.** The user enters the new status. <br/> **4.** The software responds by updating the application. |
| **Alternative paths** | **1.** In step 3, the user decides they do not want to view update the application. The software responds by exiting update application functionality. |
| **Postconditions**    | The application status is updated. |
| **Acceptance tests**  | Make sure the application status is correctly updated. |
| **Iteration**         | 3 |

<br/><br/>

| Use case # 8      |   |
| ------------------ |--|
| Name              | Delete Research Position |
| Users             | Faculty |
| Rationale         | If a research position is filled or the faculty user no longer wishes for students to apply, this will allow them to have the option to remove the research position. |
| Triggers          | User selects the delete research position option |
| Preconditions     | Research position must be posted |
| Actions           | **1.** The user indicates they want to remove the research position. <br/> **2.** The software responds by removing the research position and making the post unavailable for student users. The software also responds by displaying new position status on student's applications. |
| Alternative paths | |
| Postconditions    | The research position has been removed and applications for the position display that it is no longer available. |
| Acceptance tests  | Make sure the position has been deleted and applications are updated to reflect that the position has been removed. |
| Iteration         | 3 |

**The following is a swim-lane diagram that illustrates the message flow and activities for following scenario:**
“A student applies to a research position; initially its status will appear as “Pending”. The faculty who created that position reviews the application and updates the application status to either “Approved for Interview”, or “Hired”, or “Not hired”. The updated status of the application is displayed on the student view.
The student may delete the pending applications (i.e., whose status is still “Pending”. )”

![](readme_imgs/swimlane.png)
----
## 2.3 Non-Functional Requirements

The following is a list of non-function requirements.

**1.** Dependability: All operations that the system must perform shall be reliable.

**2.** Reusability:  The system shall have aspects within it that may be reused in the future. 

**3.** Portability:  The system shall be able to perform equivalently on all devices, web browsers (Google Chrome and Firefox), and operating systems.    

**4.** Performance:  The system shall perform consistently and effectively.  

**5.** Security:  The system shall not disclose any personal user information.

----
# 3. User Interface

## 3.1 Student User Interface
![](readme_imgs/StudentUI.png)
## 3.2 Faculty User Interface
![](readme_imgs/FacultyUI.png)
----
# 4. References

No references

----
----
