def get_company_data(user):
    # Create user_groups object with default groups
    companies = list(get_company_map().values())
    company_data = {
        **{value: False for value in companies},
        "All Subsidiaries": True
    }
    if user.lower().endswith('.io'):
        company_data["FEV.io GmbH"] = True
    return company_data


def get_company_map():
    # Keys from UserInfo['companyName'], values from the EPF Framework
    company_map = {
        'FEV Europe':              'FEV Europe GmbH',
        'FEV Group':               'FEV Group GmbH',
        'FEV India':               'FEV India',
        'FEV Romania':             'FEV Romania',
        'FEV Service Management':  'FEV Service Management GmbH',
        'FEV Turkey':              'FEV Turkey',
        'FEV Vehicle':             'FEV Vehicle GmbH',
        'FEV.io':                  'FEV.io GmbH',
        'All Subsidiaries':        'All Subsidiaries',
    }
    return company_map
