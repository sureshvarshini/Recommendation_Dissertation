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