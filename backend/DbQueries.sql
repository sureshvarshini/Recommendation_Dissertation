/* Navigate to where app.py is*/ 

/*Create all databases*/
flask shell
from app import db 
db.create_all() /*this will create both the databases - profile, food*/

/*Drop all databases*/
from app import db
db.drop_all()

/*Enter inside SQL shell to check for tables created - after db is created*/
sqlite3 food.db
.tables /* Should see your model(table) name for `food` database*/

/*SQL Queries - sample*/
/*Fetch distinct user_id and food_id*/
SELECT DISTINCT user_id FROM rating; 
SELECT * from profile;
UPDATE profile set gender=REPLACE(gender, "feMale","Female");
delete from water where id=5;
ALTER TABLE profile ADD activity_level VARCHAR;
INSERT OR REPLACE INTO profile (id, username, email, password, firstname, lastname, age, gender, height, weight, illness, activity_level) VALUES (2, 'second-user', 'second@user.com', 'pbkdf2:sha256:600000$OyvZ2baOa3o7d2x2$fda497f84292965fc1b091db20859f46030f087539fde3982b285a150daec4d9', 'Second', 'User', 67, 'Male', 167, 89, 'Hypertension', 'sedentary')
INSERT INTO profile (id, username, email, password, firstname, lastname, age, gender, height, weight, illness, activity_level) VALUES (1, 'freeman', 'first@user.com', 'pbkdf2:sha256:600000$OyvZ2baOa3o7d2x2$fda497f84292965fc1b091db20859f46030f087539fde3982b285a150daec4d9', 'Freeman', 'Truman', 89, 'Female', 189, 66, 'Diabetes', 'active')