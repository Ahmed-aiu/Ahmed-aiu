from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timezone
import pytz
import logging
from static.py import user_management

GPT_4o_instances = [
                    "ai_dawn_colMatching",
                    "ai_dawn_project",
                    "ai_dawn_response_processing",
                    "ai_dawn_xlsx_sheet_selection",
                    "ai_jlr_colMatching",
                    "ai_jlr_project",
                    "ai_jlr_response_processing",
                    "ai_jlr_xlsx_sheet_selection",
                    "ai_fd_docu",
                    "ai_fd_reverse_f_doc",
                    "ai_fd_reverse_f_req",
                    "ai_fd_reverse_f_req_ascet",
                    "ai_rfq_analysis",
                    "ai_rr_ambiguity",
                    "ai_rr_colMatching",
                    "ai_rr_ears_syntax",
                    "ai_rr_name",
                    "ai_rr_response_processing",
                    "ai_rr_set_consistency",
                    "ai_rr_singularity",
                    "ai_rr_spelling",
                    "ai_rr_verifiability",
                    "ai_rr_xlsx_sheet_selection",
                    "ai_se_chatbot",
                    "ai_tb_alice_chatbot",
                    "ai_tb_stellantis_chatbot",
                    "ai_tb_jlr_standard_writing",
                    "ai_fevgpt",
                    "ai_pm_chatbot",
                    "ii_006933_standardize_requirements"

                    ]

def save_tokens_used(db_session,UserAccounts,session,prompt_tokens_used,completion_tokens_used,ai_instance):
        
    # Update the UserAccounts table
    try:
        user_account = db_session.query(UserAccounts).filter_by(id=session.get('id')).first()
    except Exception as e:
        # Rollback only if the session is active
        if db_session.is_active:
            logging.debug(f"Rolling back the session due to error: {e}")
            db_session.rollback()
        logging.error(f"Database Error: {e}")
        user_account = None
    
    if user_account.token_usage is None:
        user_account.token_usage = {}

    # token usage
    previous_prompt_tokens = user_account.token_usage.get(f"{ai_instance}_prompt_tokens", 0.0)
    user_account.token_usage[f"{ai_instance}_prompt_tokens"] = previous_prompt_tokens + prompt_tokens_used

    previous_completion_tokens = user_account.token_usage.get(f"{ai_instance}_completion_tokens", 0.0)
    user_account.token_usage[f"{ai_instance}_completion_tokens"] = previous_completion_tokens + completion_tokens_used

    # last ai usages
    # Create timestamp for last usage
    last_usage = datetime.now(pytz.timezone('Europe/Berlin')).replace(microsecond=0)
    last_usage = last_usage.strftime('%Y-%m-%d %H:%M:%S')

    if user_account.last_ai_usages is None:
        user_account.last_ai_usages = {}
    
    user_account.last_ai_usages[ai_instance] = last_usage

    # times ai instance was used
    if user_account.number_of_ai_usages is None:
        user_account.number_of_ai_usages = {}


    # Ensure the cell is initialized and increment the value
    user_account.number_of_ai_usages[ai_instance] = (
        user_account.number_of_ai_usages.get(ai_instance, 0) + 1
    )
        
    try:
        #db.session.add(user_costs)
        db_session.add(user_account)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Error: {e}")
    finally:
        db_session.close()


def save_characters_used(db_session,UserAccounts,session,no_free_characters,no_payed_characters,translation_instance):
       
    # Update the UserAccounts table
    try:
        user_account = db_session.query(UserAccounts).filter_by(id=session.get('id')).first()
    except Exception as e:
        # Rollback only if the session is active
        if db_session.is_active:
            logging.debug(f"Rolling back the session due to error: {e}")
            db_session.rollback()
        logging.error(f"Database Error: {e}")
        user_account = None

    if user_account.translation_character_usage is None:
        user_account.translation_character_usage = {}

    # token usage
    previous_free_characters = user_account.translation_character_usage.get(f"{translation_instance}_free_characters", 0.0)
    user_account.translation_character_usage[f"{translation_instance}_free_characters"] = previous_free_characters + no_free_characters

    previous_payed_characters = user_account.translation_character_usage.get(f"{translation_instance}_payed_characters", 0.0)
    user_account.translation_character_usage[f"{translation_instance}_payed_characters"] = previous_payed_characters + no_payed_characters
    
    # last translastion usages
    # Create timestamp for last usage
    last_usage = datetime.now(pytz.timezone('Europe/Berlin')).replace(microsecond=0)
    last_usage = last_usage.strftime('%Y-%m-%d %H:%M:%S')

    if user_account.last_translation_usage is None:
        user_account.last_translation_usage = {}
    
    user_account.last_translation_usage[translation_instance] = last_usage

    # times ai instance was used
    if user_account.number_of_translation_usages is None:
        user_account.number_of_translation_usages = {}


    # Ensure the cell is initialized and increment the value
    user_account.number_of_translation_usages[translation_instance] = (
        user_account.number_of_translation_usages.get(translation_instance, 0) + 1
    )
        
    try:
        #db.session.add(user_costs)
        db_session.add(user_account)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Error: {e}")
    finally:
        db_session.close()