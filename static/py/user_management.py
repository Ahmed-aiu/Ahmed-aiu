from flask import Blueprint, session, current_app
from datetime import datetime
import pytz
from sqlalchemy import inspect
import traceback
from static.py.utils import get_company_data


def create_account(UserInfo):
    logger = current_app.logger
    logger.info("Starting create_account function.")
    logger.debug(f"Received UserInfo: {UserInfo}")
    logger.debug("Retrieved Database and DB session from app config.")

    # Create a new session from the session factory
    SessionFactory = current_app.config['SESSION_FACTORY'] # Get the session factory from config
    db_session = SessionFactory() # Create a new session
    UserAccounts = current_app.config['USER_ACCOUNTS']
    UserGroups = current_app.config['USER_GROUPS']
    UserAppRights = current_app.config['USER_APP_RIGHTS']
    Costs = current_app.config['COSTS']
    user = UserInfo['mail']

    try:
        ## Account doesn't exist and the form data is valid, now insert new account into accounts table
        # Create timestamp
        creation_time = datetime.now(pytz.timezone('Europe/Berlin')).replace(microsecond=0)
        logger.debug(f"Current creation_time (timezone-aware): {creation_time}")

        formatted_creation_time = creation_time.strftime('%Y-%m-%d %H:%M:%S')
        logger.debug(f"Formatted creation_time for production: {formatted_creation_time}")

        user_data = UserAccounts(
            username=user,
            firstname=UserInfo['givenName'],
            lastname=UserInfo['surname'],
            created_at=formatted_creation_time,
            microsoft_id=UserInfo['id'],
        )
        logger.debug(f"Created UserAccounts object: {user_data}")
        logger.debug(f"User is from company {UserInfo['companyName']}")

        # Create user_costs object
        user_costs = Costs(username=user)
        logger.debug(f"Created Costs object: {user_costs}")

        # Create user_rights object with default rights
        possible_rights = [
            "SeChatBot",
            "RequirementsReview",
            "RequirementsGeneration",
            "CCode2Docu",
            "Screenshot2Docu",
            "ReverseEngineeringOfReq",
            "FunctionGeneration",
            "RfqDistribution",
            "AliceChatBot",
            "Ep006823RequirementGeneration",
            "EP005757SwTestSpecGeneration",
            "StellantisChatbot",
            "JLRStandardWritingChatbot",
            "EPFChatbot",
            "fevgpt",
            "pm_chatbot",
            "ii_006933_standardize_requirements",
        ]
        user_rights = UserAppRights(
            username=user,
            **{value: False for value in possible_rights}
        )
        logger.debug(f"Created UserAppRights object: {user_rights}")

        company_data = get_company_data(user) # stub for creation, currently unused

        # Create user_groups object with default groups
        user_groups = UserGroups(
            username=user,
            administrator=False,
            FEVGroup=True,
            subsidiary=company_data,
        )
        logger.debug(f"Created UserGroups object: {user_groups}")

        # Add all objects to the session
        db_session.add(user_data)
        logger.debug("Added user_data to DB session.")
        db_session.add(user_costs)
        logger.debug("Added user_costs to DB session.")
        db_session.add(user_rights)
        logger.debug("Added user_rights to DB session.")
        db_session.add(user_groups)
        logger.debug("Added user_groups to DB session.")

        # Commit the session
        db_session.commit()
        logger.info("Successfully committed new user account to the database.")

    except Exception as e:
        # Log the exception with traceback
        logger.error("An error occurred while creating a new account.")
        logger.error(f"Exception: {e}")
        logger.error(traceback.format_exc())
        db_session.rollback()
        logger.info("Rolled back the DB session due to the error.")
    finally:
        db_session.close()
        logger.debug("Closed the DB session.")
        logger.info("Finished create_account function.")


def login_user(UserInfo):
    logger = current_app.logger
    logger.info("Starting login_user function.")
    logger.debug(f"Received UserInfo: {UserInfo}")

    # Get DB information 
    # Create a new session from the session factory
    SessionFactory = current_app.config['SESSION_FACTORY'] # Get the session factory from config
    db_session = SessionFactory() # Create a new session
    UserAccounts = current_app.config['USER_ACCOUNTS']
    UserGroups = current_app.config['USER_GROUPS']
    UserAppRights = current_app.config['USER_APP_RIGHTS']
    GroupAppRights = current_app.config['GROUP_APP_RIGHTS']

    logger.debug("Retrieved Database and DB session from app config.")
    user = UserInfo['mail']

    try:
        # Lookup information from database
        logger.debug("Querying UserAccounts table.")
        user_login = db_session.query(UserAccounts).filter_by(username=user).first()
        logger.debug(f"Retrieved user_login: {user_login}")

        logger.debug("Querying UserGroups table.")
        user_groups = db_session.query(UserGroups).filter_by(username=user).first()
        logger.debug(f"Retrieved user_groups: {user_groups}")

        logger.debug("Querying UserAppRights table.")
        user_rights = db_session.query(UserAppRights).filter_by(username=user).first()
        logger.debug(f"Retrieved user_rights: {user_rights}")

        combined_allowed_routes = []
        allowed_user_routes = []

        # Inspect user rights for routes
        logger.debug("Inspecting user rights for allowed routes.")
        inspector = inspect(user_rights.__class__)
        user_rights_columns = [column.name for column in inspector.columns if column.name not in ['id', 'username']]
        logger.debug(f"User rights columns: {user_rights_columns}")

        for column in user_rights_columns:
            right = getattr(user_rights, column)
            logger.debug(f"Checking right '{column}': {right}")
            if right:
                allowed_user_routes.append(column)
                logger.debug(f"Added '{column}' to allowed_user_routes.")

        combined_allowed_routes = allowed_user_routes.copy()
        logger.debug(f"Initial combined_allowed_routes: {combined_allowed_routes}")

        # Inspect user groups for additional routes
        member_of_groups = []
        logger.debug("Inspecting user groups.")
        group_inspector = inspect(user_groups.__class__)
        user_groups_columns = [column.name for column in group_inspector.columns if
                               column.name not in ['id', 'username']]
        logger.debug(f"User groups columns: {user_groups_columns}")

        for column in user_groups_columns:
            group_member = getattr(user_groups, column)
            logger.debug(f"Checking group membership '{column}': {group_member}")
            if group_member:
                member_of_groups.append(column)
                logger.debug(f"Added '{column}' to member_of_groups.")

        logger.debug(f"Member of groups: {member_of_groups}")

        for group in member_of_groups:
            logger.debug(f"Processing group: {group}")

            group_rights = db_session.query(GroupAppRights).filter_by(UserGroup=group).first()
            logger.debug(f"Retrieved group_rights for '{group}': {group_rights}")

            if not group_rights:
                logger.warning(f"No GroupAppRights found for group '{group}'. Skipping.")
                continue

            allowed_group_routes = []
            logger.debug(f"Inspecting group rights for group '{group}'.")
            inspector = inspect(group_rights.__class__)
            group_rights_columns = [column.name for column in inspector.columns if
                                    column.name not in ['id', 'UserGroup']]
            logger.debug(f"Group rights columns for '{group}': {group_rights_columns}")

            for column in group_rights_columns:
                group_right = getattr(group_rights, column)
                logger.debug(f"Checking group right '{column}': {group_right}")
                if group_right:
                    allowed_group_routes.append(column)
                    logger.debug(f"Added '{column}' to allowed_group_routes for group '{group}'.")

            combined_allowed_routes = list(set(combined_allowed_routes) | set(allowed_group_routes))
            logger.debug(f"Updated combined_allowed_routes after processing group '{group}': {combined_allowed_routes}")

        # Write user data into session
        logger.debug("Writing user data into session.")
        session['loggedin'] = True
        session['admin'] = getattr(user_groups, 'administrator', False)
        session['id'] = user_login.id
        session['username'] = user_login.username
        session['firstname'] = user_login.firstname
        session['mail'] = user_login.username
        session['rights'] = combined_allowed_routes
        session['groups'] = member_of_groups
        session['company'] = UserInfo['companyName']
        logger.info(
            f"User '{session['username']}' LOGIN SUCCESSFUL with rights: {session['rights']} and groups: {session['groups']}.")

    except Exception as e:
        # Log the exception with traceback
        logger.error("An error occurred during user login.")
        logger.error(f"Exception: {e}")
        logger.error(f"User '{session['username']}' LOGIN FAILED")
        logger.error(traceback.format_exc())
        if db_session.is_active:
            db_session.rollback()
            logger.info("Rolled back the DB session due to the error.")
