from flask import current_app
from sqlalchemy import text

def execute_sql_command(sql_commands):
    
    #get DB connection
    # Create a new session from the session factory
    SessionFactory = current_app.config['SESSION_FACTORY'] # Get the session factory from config
    db_session = SessionFactory() # Create a new session
    
    #Create empty results list
    results = []
    
    for sql_command in sql_commands:      
        try:
            #execute multiple sql commands
            for sql_command in sql_commands:
                result = db_session.execute(text(sql_command))
                
                #save results in list
                if result.returns_rows:
                    results.append(result.fetchall())
                    
            #commit any changes to DB 
            db_session.commit()
            current_app.logger.info(f"SQL command {sql_command} executed successfully")
        except Exception as e:
            current_app.logger.info(f"Error executing SQL command {sql_command}. Detailed information: {e}")
            db_session.rollback()
        return results

def add_access_permission_to_db(new_access_permission_name):
    #Create App Column in GroupAppRights and deny access for all
    sql_command1 = f"ALTER TABLE [dbo].[GroupAppRights] ADD {new_access_permission_name} BIT DEFAULT 0 WITH VALUES"
    #Allow administrator to access new instandce
    sql_command2 = f"UPDATE [dbo].[GroupAppRights] SET {new_access_permission_name} = '1' WHERE id = 1"
    #Create App Column in UserAppRights and deny access 
    sql_command3 = f"ALTER TABLE [dbo].[UserAppRights] ADD {new_access_permission_name} BIT DEFAULT 0 WITH VALUES"
    
    sql_commands = [sql_command1,sql_command2,sql_command3]
    temp = execute_sql_command(sql_commands)

def get_user_groups():
    #define SQL command to get all usergroups from GroupAppRights table
    sql_command = "SELECT UserGroup FROM [dbo].[GroupAppRights]"
    sql_results = execute_sql_command([sql_command])
    user_groups = [row[0] for result in sql_results for row in result]
    return user_groups

def get_users():
    #define SQL command to get all usernames from UserAppRights table
    sql_command = "SELECT username FROM [dbo].[UserAppRights]"
    sql_results = execute_sql_command([sql_command])
    users = [row[0] for result in sql_results for row in result]
    return users

def get_apps():
    #define SQL command to get all app names (Access-Names) from UserAppRights table
    sql_command = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'UserAppRights' AND COLUMN_NAME NOT IN ('id', 'username');"
    sql_results = execute_sql_command([sql_command])
    users = [row[0] for result in sql_results for row in result]
    return users

def adjust_user_rights(user, app, rights):
    #get id for user
    userid=execute_sql_command([f"SELECT id FROM [dbo].[UserAppRights] WHERE username = '{user}';"])
    id=userid[0][0][0]
    
    #set rights for user
    execute_sql_command([f"UPDATE [dbo].[UserAppRights] SET {app} = '{rights}' WHERE id = {id}"])
    
def adjust_group_rights(group, app, rights):
    #get id for user
    groupid=execute_sql_command([f"SELECT id FROM [dbo].[GroupAppRights] WHERE UserGroup = '{group}';"])
    id=groupid[0][0][0]
    
    #set rights for user
    execute_sql_command([f"UPDATE [dbo].[GroupAppRights] SET {app} = '{rights}' WHERE id = {id}"])