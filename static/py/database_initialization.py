from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.sql import func
from sqlalchemy.dialects.mssql import JSON
from sqlalchemy.ext.mutable import MutableDict
from azure.identity import AzureCliCredential, InteractiveBrowserCredential, ChainedTokenCredential, DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
import pyodbc
import os
import struct
from flask import Blueprint, session, current_app
import logging

Base = declarative_base()


def initialize_database(db_session):
    # Initialize tables of the database
    class UserAppRights(Base):
        __tablename__ = 'UserAppRights'
        id = Column(Integer, primary_key=True)
        username = Column(String(120), unique=True, nullable=False)
        SeChatBot = Column(Boolean)
        RequirementsReview = Column(Boolean)
        RequirementsGeneration = Column(Boolean)
        CCode2Docu = Column(Boolean)
        Screenshot2Docu = Column(Boolean)
        ReverseEngineeringOfReq = Column(Boolean)
        FunctionGeneration = Column(Boolean)
        RfqDistribution = Column(Boolean)
        AliceChatBot = Column(Boolean)
        Ep006823RequirementGeneration = Column(Boolean)
        EP005757SwTestSpecGeneration = Column(Boolean)
        StellantisChatbot = Column(Boolean)
        JLRStandardWritingChatbot = Column(Boolean)
        EPFChatbot = Column(Boolean)
        admin_interface = Column(Boolean)
        fevgpt = Column(Boolean)
        pm_chatbot = Column(Boolean)
        ii_006933_standardize_requirements = Column(Boolean)
        document_translation = Column(Boolean)

        def __repr__(self):
            return '<UserAppRights %r>' % self.username

    class Costs(Base):
        __tablename__ = 'Costs'
        id = Column(Integer, primary_key=True)
        username = Column(String(80), unique=True, nullable=False)
        costs = Column(Float)
        total_prompt_tokens = Column(Integer)
        total_completion_tokens = Column(Integer)
        ai_rfq_analysis_prompt_tokens = Column(Integer)
        ai_rfq_analysis_completion_tokens = Column(Integer)
        ai_rr_ambiguity_prompt_tokens = Column(Integer)
        ai_rr_ambiguity_completion_tokens = Column(Integer)
        ai_rr_colMatching_prompt_tokens = Column(Integer)
        ai_rr_colMatching_completion_tokens = Column(Integer)
        ai_rr_ears_syntax_prompt_tokens = Column(Integer)
        ai_rr_ears_syntax_completion_tokens = Column(Integer)
        ai_rr_name_prompt_tokens = Column(Integer)
        ai_rr_name_completion_tokens = Column(Integer)
        ai_rr_set_consistency_prompt_tokens = Column(Integer)
        ai_rr_set_consistency_completion_tokens = Column(Integer)
        ai_rr_singularity_prompt_tokens = Column(Integer)
        ai_rr_singularity_completion_tokens = Column(Integer)
        ai_rr_spelling_prompt_tokens = Column(Integer)
        ai_rr_spelling_completion_tokens = Column(Integer)
        ai_rr_verifiability_prompt_tokens = Column(Integer)
        ai_rr_verifiability_completion_tokens = Column(Integer)
        ai_rr_xlsx_sheet_selection_prompt_tokens = Column(Integer)
        ai_rr_xlsx_sheet_selection_completion_tokens = Column(Integer)
        ai_se_chatbot_prompt_tokens = Column(Integer)
        ai_se_chatbot_completion_tokens = Column(Integer)
        ai_tb_alice_chatbot_prompt_tokens = Column(Integer)
        ai_tb_alice_chatbot_completion_tokens = Column(Integer)
        ai_tb_stellantis_chatbot_prompt_tokens = Column(Integer)
        ai_tb_stellantis_chatbot_completion_tokens = Column(Integer)
        ai_dawn_colMatching_prompt_tokens = Column(Integer)
        ai_dawn_colMatching_completion_tokens = Column(Integer)
        ai_dawn_project_prompt_tokens = Column(Integer)
        ai_dawn_project_completion_tokens = Column(Integer)
        ai_dawn_xlsx_sheet_selection_prompt_tokens = Column(Integer)
        ai_dawn_xlsx_sheet_selection_completion_tokens = Column(Integer)
        ai_jlr_colMatching_prompt_tokens = Column(Integer)
        ai_jlr_colMatching_completion_tokens = Column(Integer)
        ai_jlr_project_prompt_tokens = Column(Integer)
        ai_jlr_project_completion_tokens = Column(Integer)
        ai_jlr_xlsx_sheet_selection_prompt_tokens = Column(Integer)
        ai_jlr_xlsx_sheet_selection_completion_tokens = Column(Integer)
        ai_fd_docu_prompt_tokens = Column(Integer)
        ai_fd_docu_completion_tokens = Column(Integer)
        ai_fd_reverse_f_doc_prompt_tokens = Column(Integer)
        ai_fd_reverse_f_doc_completion_tokens = Column(Integer)
        ai_fd_reverse_f_req_prompt_tokens = Column(Integer)
        ai_fd_reverse_f_req_completion_tokens = Column(Integer)

        def __repr__(self):
            return '<Costs %r>' % self.username

    class UserAccounts(Base):
        __tablename__ = 'UserAccounts'
        id = Column(Integer, primary_key=True, autoincrement=True)
        username = Column(String(80), unique=True, nullable=False)
        firstname = Column(String(120), nullable=False)
        lastname = Column(String(120), nullable=False)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        microsoft_id = Column(String(80))
        last_usage = Column(DateTime(timezone=True), server_default=func.now())
        instances = Column(Integer)
        total_time_spent = Column(Float, default=0.0)  # Total time in milliseconds
        route_usage_durations = Column(MutableDict.as_mutable(JSON), default=dict)  # route times in milliseconds
        token_usage = Column(MutableDict.as_mutable(JSON), default=dict)
        last_ai_usages = Column(MutableDict.as_mutable(JSON), default=dict)
        number_of_ai_usages = Column(MutableDict.as_mutable(JSON), default=dict)
        translation_character_usage = Column(MutableDict.as_mutable(JSON), default=dict)
        last_translation_usage = Column(MutableDict.as_mutable(JSON), default=dict)
        number_of_translation_usages = Column(MutableDict.as_mutable(JSON), default=dict)
        def __repr__(self):
            return '<UserAccounts %r>' % self.username

    class UserGroups(Base):
        __tablename__ = 'UserGroups'
        id = Column(Integer, primary_key=True)
        username = Column(String(80), unique=True, nullable=False)
        administrator = Column(Boolean, nullable=True)
        FEVGroup = Column(Boolean, nullable=True)
        subsidiary = Column(MutableDict.as_mutable(JSON), default=dict)

        def __repr__(self):
            return '<UserGroups %r>' % self.username

    class GroupAppRights(Base):
        __tablename__ = 'GroupAppRights'
        id = Column(Integer, primary_key=True)
        UserGroup = Column(String(120), unique=True, nullable=False)
        SeChatBot = Column(Boolean)
        FdChatBot = Column(Boolean)
        RequirementsReview = Column(Boolean)
        RequirementsGeneration = Column(Boolean)
        CCode2Docu = Column(Boolean)
        Screenshot2Docu = Column(Boolean)
        ReverseEngineeringOfReq = Column(Boolean)
        FunctionGeneration = Column(Boolean)
        RfqDistribution = Column(Boolean)
        AliceChatBot = Column(Boolean)
        Ep006823RequirementGeneration = Column(Boolean)
        EP005757SwTestSpecGeneration = Column(Boolean)
        StellantisChatbot = Column(Boolean)
        JLRStandardWritingChatbot = Column(Boolean)
        EPFChatbot = Column(Boolean)
        admin_interface = Column(Boolean)
        fevgpt = Column(Boolean)
        pm_chatbot = Column(Boolean)
        ii_006933_standardize_requirements = Column(Boolean)
        document_translation = Column(Boolean)

        def __repr__(self):
            return '<GroupAppRights %r>' % self.UserGroup
    
    class Feedback(Base):
        __tablename__ = 'Feedback'
        id = Column(Integer, primary_key=True)
        username = Column(String(120), nullable=False)   
        feedback_type = Column(String(255), nullable=False) 
        topic = Column(String(255), nullable=False)
        steps_to_reproduce = Column(Text, nullable=False)
        user_description  = Column(Text, nullable=False)
        attachments  = Column(Text, nullable=False)
        device_information = Column(String(2048), nullable=False) 
        created_at = Column(DateTime(timezone=True), server_default=func.now())
        
        def __repr__(self):
            return '<Feedback %r>' % self.username   

    # Create all tables
    Base.metadata.create_all(db_session.get_bind())    
    
    return UserAccounts,UserGroups,UserAppRights,Costs,GroupAppRights,Feedback

def connect_to_database():
    # Establish database connection
    connection_string = f"Driver={os.getenv('DB_DRIVER')};Server=tcp:{os.getenv('DB_SERVER')},1433;Database={os.getenv('DB_DATABASE')};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;MARS_Connection=yes;"

    # Get credential for Azure SQL Database
    if os.getenv('FLASK_ENV') != 'development': # production & testing environment
        credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
        token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    else: # local development environment
        try:
            # Get the token for Azure SQL Database
            credential = AzureCliCredential()
            token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
            logging.info("Successfully obtained access token using CLI.")
        except ClientAuthenticationError as e:
            logging.info(f"Authentication via CLI failed. Using Interactive Browser Authentication.")
            credential = InteractiveBrowserCredential()
            token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
            logging.info("Successfully obtained access token using CLI.")

    try:
        # Pack the token into the required structure for pyodbc
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by Microsoft in msodbcsql.h
        # Connect to the database using the token
        conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
        logging.info("Successfully connected to the database.")
    except pyodbc.Error as e:
        logging.error(f"Error in DB raw connection: {e}")
        return None
    
    # Pass the raw connection to SQLAlchemy
    engine = create_engine(
        'mssql+pyodbc://', 
        creator=lambda: conn,
        pool_size=10,  # Increase the pool size
        max_overflow=5,  # Allow up to 5 additional connections
        pool_timeout=30,  # Wait up to 30 seconds for a connection
        pool_recycle=1800  # Recycle connections after 30 minutes
        )

    # Create a session
    SessionFactory = sessionmaker(bind=engine)
    # Create a scoped session
    db_session = SessionFactory()

    return SessionFactory, db_session, conn
