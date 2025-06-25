# global imports
from flask import Blueprint, render_template, session, request, redirect, url_for, current_app, jsonify, send_file, after_this_request
import json, os
from collections import OrderedDict
from static.py import token_handling
from static.py import get_flask_folders
from static.py.decorators import inject_config, check_login_and_rights, track_time
# route specific imports
from ..py import rfq_report_generation, ai_rfq_analysis

template_folder, static_folder, static_url_path = get_flask_folders.get(file=__file__)

# Initalize Blueprint
rfq_bp = Blueprint(
            'rfq_bp',
            __name__,
            template_folder=template_folder,
            static_folder=static_folder,
            static_url_path=static_url_path
            )

@rfq_bp.route("/rfqd", methods = ['POST','GET'])
@check_login_and_rights('RfqDistribution')
@track_time()
@inject_config(['auth','sid_to_room','tab_id_to_sid','sid_to_tab_id','socketio','db_session','UserAccounts'])
def rfq_distribution(auth, sid_to_room, tab_id_to_sid, sid_to_tab_id,socketio, db_session, UserAccounts):
    action = request.values.get('action')
    if request.method == 'POST' and action == 'analysis':
        # Handle RFQ analysis
        files_list = request.files.getlist('files')
        # Convert list to dictionary with filenames as keys
        files = {}
        for file_storage in files_list:
            files[file_storage.filename] = file_storage
        # Now 'files' is a dictionary as expected by 'extract_text_from_files'
        rfq_analysis_result, prompt_tokens_used, completion_tokens_used = ai_rfq_analysis.analysis(files)
        # Write used tokens to database
        token_handling.save_tokens_used(db_session, UserAccounts, session,prompt_tokens_used,completion_tokens_used,'ai_rfq_analysis')
        session['rfq_analysis_result'] = rfq_analysis_result
        # Perform Output Handling
        rfq_result = json.loads(rfq_analysis_result)
        rfq_summary = rfq_result['Summary']
        rfq_maincats = rfq_result['Main-Categories']
        rfq_subcats = rfq_result['Sub-Categories']
        rfq_departs = rfq_result['Departments']
        rfq_project_start = rfq_result['Project-Start']
        rfq_project_duration = rfq_result['Project-Duration']
        rfq_contact_tech = rfq_result['Contact-Technical']
        rfq_contact_sales = rfq_result['Contact-Commercial']
        rfq_proposal_deadline = rfq_result['Proposal-Deadline']
        # Render only the dynamic content block as HTML string
        result_html = render_template(
            'rfq_distribution_combined.html',
            rfq_summary=rfq_summary,
            rfq_maincats=rfq_maincats,
            rfq_subcats=rfq_subcats,
            rfq_departs=rfq_departs,
            rfq_project_start=rfq_project_start,
            rfq_project_duration=rfq_project_duration,
            rfq_contact_tech=rfq_contact_tech,
            rfq_contact_sales=rfq_contact_sales,
            rfq_proposal_deadline=rfq_proposal_deadline,
            analysis_completed=True,  # Flag to indicate analysis is done
            partial=True  # Flag to render only the dynamic content
        )
        return jsonify({'result_html': result_html})
    elif action == 'download':
        # Handle download
        try:
            report_path, report_name = rfq_report_generation.generate(session['rfq_analysis_result'], session['username'])
            if report_path is not None:
                @after_this_request
                def remove_file(response):
                    try:
                        os.remove(report_path)
                    except Exception as e:
                        current_app.logger.error(f"Error removing or closing downloaded file handle: {e}")
                    return response
                return send_file(report_path, as_attachment=True)
            else:
                return "No file found", 404
        except Exception as e:
            return str(e)
    else:
        # Render the full page
        return render_template('rfq_distribution_combined.html', login=session.get('loggedin', False))