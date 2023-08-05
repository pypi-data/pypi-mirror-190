from requests import Session
from .atlas_parsing import parse_payee_search_for_vendor_id, parse_rfp_details
from .models import RFP, RFPCreationData

def search(session:Session, *, rfp_number:int) -> RFP:
    response = session.post(
        'https://adminappsts.mit.edu/rfp/SearchForRfps.action',
        data={
            'taxable': '',
            'criteria.parked': 'true',
            '__checkbox_criteria.parked': 'true',
            'criteria.posted': 'true',
            '__checkbox_criteria.posted': 'true',
            '__checkbox_criteria.deleted': 'true',
            'criteria.companyCode': 'CUR',
            'criteria.rfpNumber': str(rfp_number),
            'criteria.createdDateFrom':'', #MM/DD/YY
            'criteria.createdDateTo': '',
            'criteria.payeeName': '',
            'criteria.shortDescription': '',
            'criteria.costObjectNumber': '',
            'criteria.glAccountNumber': ''
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    )
    return parse_rfp_details(response)

def submit_rfp(session: Session, *, rfp: RFPCreationData) -> RFP:
    payee_search_response = session.post(
        'https://adminappsts.mit.edu/rfp/SearchForPayee.action',
        data={
            'taxable': 'false',
            'payeeType': 'MIT',
            'payeeName': rfp.payee.name
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    )
    payee_vendor_id = parse_payee_search_for_vendor_id(payee_search_response)
    payee_search_response = session.post(
        'https://adminappsts.mit.edu/rfp/SearchForPayee.action',
        data={
            'taxable': 'false',
            'payeeType': 'MIT',
            'payeeName': rfp.payee.name
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    )