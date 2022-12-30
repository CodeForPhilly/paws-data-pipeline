User Management API
----------


*** Create user record 
    
Requires admin role  

Form POST Parameters  
----------
username : str  
full_name : str  
password : str  
role : str, one of `user`, `editor`, `admin`  

Returns    
----------
User created: 201 + username  
Invalid role: 422 + "Bad role"  
Duplicate user: 409 +  DB error  


*** Get users


Returns
----------
One header row of field names, one row per user  
"['username', 'full_name', 'active', 'role'],  
['admin', None, 'Y', 'admin'],  
['editor', None, 'Y', 'editor'],  
['steve11', 'Steve the User', 'Y', 'admin'],  
['user', None, 'Y', 'user'],"