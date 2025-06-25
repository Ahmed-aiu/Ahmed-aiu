# decorators.py
from functools import wraps
from static.py import user_management
from flask import session, redirect, url_for, current_app, flash, request
from time import time
import logging

def inject_config(config_keys=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Define all available configuration keys and their corresponding variable names
            all_configs = {
                'auth': current_app.config.get('AUTH'),
                'sid_to_room': current_app.config.get('SID_TO_ROOM'),
                'tab_id_to_sid': current_app.config.get('TAB_ID_TO_SID'),
                'sid_to_tab_id': current_app.config.get('SID_TO_TAB_ID'),
                'socketio': current_app.config.get('SOCKETIO'),
                # 'db_session': current_app.config.get('DB_SESSION'),
                'db_session': current_app.config.get('SESSION_FACTORY'),  # Use session factory
                'UserAccounts':current_app.config.get('USER_ACCOUNTS'),
                'UserGroups': current_app.config.get('USER_GROUPS'), 
                'UserAppRights':current_app.config.get('USER_APP_RIGHTS'), 
                'Costs': current_app.config.get('COSTS'), 
                'GroupAppRights':current_app.config.get('GROUP_APP_RIGHTS') 
            }
            
            # If no specific keys are given, inject all; otherwise, inject only the specified keys
            config_to_inject = {}
            for name, value in all_configs.items():
                if not config_keys or name in config_keys:
                    if name == 'db_session' and value:  # Handle db_session separately
                        config_to_inject[name] = value()  # Create a new session instance
                    else:
                        config_to_inject[name] = value

            try:
                # Call the original function with the configurations as arguments
                return func(*args, **config_to_inject, **kwargs)
            finally:
                # Ensure the session is closed after the function execution
                if 'db_session' in config_to_inject:
                    db_session = config_to_inject['db_session']
                    try:
                        db_session.close()
                    except Exception as e:
                        current_app.logger.error(f"Error closing db_session: {e}")

            # # If no specific keys are given, inject all; otherwise, inject only the specified keys
            # config_to_inject = {name: value for name, value in all_configs.items() 
            #                     if not config_keys or name in config_keys}
            
            # # Call the original function with the configurations as arguments
            # return func(*args, **config_to_inject, **kwargs)
        return wrapper
    return decorator

def snake_to_words(snake_str):
    words = snake_str.replace('_', ' ')
    return words.capitalize()  # Capitalize the first letter if needed

def save_time_spent(route_name, time_spent, user_id):
    current_app.logger.info(f"Start saving time spent: route_name={route_name}, time_spent_ms={time_spent}, user_id={user_id}")

    #check if user is correctly identified
    if user_id is not None:

        # Create a new session from the session factory
        SessionFactory = current_app.config['SESSION_FACTORY'] # Get the session factory from config
        db_session = SessionFactory() # Create a new session
        UserAccounts = current_app.config['USER_ACCOUNTS']


        # Update the UserAccounts table
        try:    
            user_account = db_session.query(UserAccounts).filter_by(id=user_id).first()
        except Exception as e:
            # Rollback only if the session is active
            if db_session.is_active:
                logging.debug(f"Rolling back the session due to error: {e}")
                db_session.rollback()
            logging.error(f"Database Error: {e}")
            user_account = None
        
        # Initialize total_time_spent if None
        if user_account.total_time_spent is None:
            user_account.total_time_spent = 0.0

        # Update the total time spent
        user_account.total_time_spent += time_spent

        # Initialize route_times if None
        if user_account.route_usage_durations is None:
            user_account.route_usage_durations = {}

        # Update route-specific time in the JSON field
        previous_route_time = user_account.route_usage_durations.get(route_name, 0.0)
        user_account.route_usage_durations[route_name] = previous_route_time + time_spent

        # Commit the changes
        try:
            #db.session.add(route_time_record)
            db_session.add(user_account)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            current_app.logger.error(f"Error while updating time spent: {e}", exc_info=True)
        finally:
            db_session.close()

    else:
        #skip time tracking if user is not identified
        current_app.logger.error(f"User not identified. Skipped saving time spent for route: {route_name}.", exc_info=True)


def check_login_and_rights(required_right=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Track route and store in session
            session['REDIRECT_ROUTE'] = request.url       
            
            # Authentication and authorization check
            auth = current_app.config.get('AUTH')
            user = auth.get_user() if auth else None
            user_rights = session.get('rights', [])

            if user and (required_right is None or required_right in user_rights):
                return func(*args, **kwargs)
            elif user is None or user_rights == []:
                return redirect(url_for("home_bp.home"))
            else:
                current_app.logger.warning("Unauthorized access attempt.")
                flash(
                    f"You do not have the necessary permissions to access {snake_to_words(func.__name__)}. "
                    f"Please contact the project maintainers to request access.", "error"
                )
                return redirect(url_for("home_bp.home"))

        return wrapper
    return decorator

def track_time():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Retrieve the current time for this request
            current_time = time()

            # Initialize variables to store route information
            last_route_name = session.get('last_route_name')
            last_route_time = session.get('last_route_time')

            if last_route_name and last_route_time:
                # Calculate the time spent on the previous route
                time_spent = current_time - last_route_time  # Time in seconds

                # Log the time spent on the last route
                current_app.logger.info(
                    f"Time spent on route '{last_route_name}': {time_spent:.4f} seconds"
                )

                # Persist the route time into the database using the new function
                try:
                    # Retrieve user_id from session
                    user_id = session.get('id')

                    # Call the new save_time_spent function
                    save_time_spent(last_route_name, time_spent, user_id)
                except Exception as e:
                    # Log any exceptions
                    current_app.logger.error(f"Failed to log route time for '{last_route_name}': {e}")

            # Store the current route name and time for the next request
            session['last_route_name'] = request.endpoint or func.__name__
            session['last_route_time'] = current_time
            
            return func(*args, **kwargs)

        return wrapper
    return decorator