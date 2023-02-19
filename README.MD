
HTTP tester with Python/PyCurl

Author: P-C Markovski
Date: (Git repo init): 2019-06-21
Purpose: Source code for a course on Python and REST API testing.

Database requirements

Note the code :  con = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='LookYonder!', db='restapitests', autocommit=True)
A MySQL compliant database with a database "restapitests" is required.
Table structure as follows :

CREATE TABLE loadmetrics (
responsecode varchar(50),
rtt varchar(50),
url varchar(500))”

