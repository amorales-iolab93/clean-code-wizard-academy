

import datetime
from typing import Dict, Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel


def get_db_wizard_record():
    wizard_request_record = [{
        'AcademyId': 'kingdom#clover_kingdom',
        'ResourceId': 'wizard#323b5cca-b124-4883-9212-00438cfd78b4',
        'Disabled': False,
        'CreatedAt': 1721756170,
        'UpdatedAt': 1721836220,
        'RequestId': '323b5cca-b124-4883-9212-00438cfd78b4',
        'Name': 'Hermes',
        'LastName': 'Trismegisto',
        'Age': 30,
        'MagicSkill': 'Light',
        'WizardRequestStatus': 'approved',
        'Grimorie':'one-leaf-clover'
    },
    {
        'AcademyId': 'kingdom#clover_kingdom',
        'ResourceId': 'wizard#323b5cca-b124-4883-9212-00438cfd78b6',
        'Disabled': False,
        'CreatedAt': 1721756170,
        'UpdatedAt': 1721836220,
        'RequestId': '323b5cca-b124-4883-9212-00438cfd78b6',
        'Name': 'Saruman',
        'LastName': 'Wizard',
        'Age': 15,
        'MagicSkill': 'Light',
        'WizardRequestStatus': 'approved',
        'Grimorie':'one-leaf-clover'
    },
    {
        'AcademyId': 'kingdom#clover_kingdom',
        'ResourceId': 'wizard#323b5cca-b124-4883-9212-00438cfd78b5',
        'Disabled': False,
        'CreatedAt': 1721756170,
        'UpdatedAt': 1721836220,
        'RequestId': '323b5cca-b124-4883-9212-00438cfd78b5',
        'Name': 'Rasputín',
        'LastName': 'Wizard',
        'Age': 68,
        'MagicSkill': 'Light',
        'WizardRequestStatus': 'approved',
        'Grimorie':'two-leaf-clover'
    },
    {
        'AcademyId': 'kingdom#clover_kingdom',
        'ResourceId': 'wizard#323b5cca-b124-4883-9212-00438cfd78b8',
        'Disabled': False,
        'CreatedAt': 1721756170,
        'UpdatedAt': 1721836220,
        'RequestId': '323b5cca-b124-4883-9212-00438cfd78b8',
        'Name': 'Merlín',
        'LastName': 'Wizard',
        'Age': 100,
        'MagicSkill': 'Light',
        'WizardRequestStatus': 'approved',
        'Grimorie':'four-leaf-clover'
    },
    {
        'AcademyId': 'kingdom#clover_kingdom',
        'ResourceId': 'wizard#323b5cca-b124-4883-9212-00438cfd78b11',
        'Disabled': False,
        'CreatedAt': 1721756170,
        'UpdatedAt': 1721836220,
        'RequestId': '323b5cca-b124-4883-9212-00438cfd78b11',
        'Name': 'Druidas',
        'LastName': 'Wizard',
        'Age': 15,
        'MagicSkill': 'Light',
        'WizardRequestStatus': 'in_process'
    },
    {
        'AcademyId': 'kingdom#clover_kingdom',
        'ResourceId': 'wizard#323b5cca-b124-4883-9212-00438cfd78b01',
        'Disabled': False,
        'CreatedAt': 1721756170,
        'UpdatedAt': 1721836220,
        'RequestId': '323b5cca-b124-4883-9212-00438cfd78b01',
        'Name': 'Saruman',
        'LastName': 'Wizard',
        'Age': 15,
        'MagicSkill': 'Light',
        'WizardRequestStatus': 'rejected'
    }]
    return wizard_request_record



def get_db_wizard_empty_record():
    wizard_request_record = []
    return wizard_request_record

def get_db_wizard_request():
    wizard_request = {
        'AcademyId': 'kingdom#clover_kingdom',
        'ResourceId': 'wizard#323b5cca-b124-4883-9212-00438cfd78b4',
        'Disabled': False,
        'CreatedAt': 1721756170,
        'UpdatedAt': 1721836220,
        'RequestId': '323b5cca-b124-4883-9212-00438cfd78b4',
        'Name': 'Alan Jonathan',
        'LastName': 'Morales Sanchez',
        'Age': 30,
        'MagicSkill': 'Light',
        'WizardRequestStatus': 'approved',
        'Grimorie':'one-leaf-clover'
    }
    return wizard_request

def set_db_wizard_request(**values):
    wizard_request = {
        'AcademyId': 'kingdom#clover_kingdom',
        'ResourceId': 'wizard#323b5cca-b124-4883-9212-00438cfd78b4',
        'Disabled': False,
        'CreatedAt': 1721756170,
        'UpdatedAt': 1721836220,
        'RequestId': '323b5cca-b124-4883-9212-00438cfd78b4',
        'Name': 'Alan Jonathan',
        'LastName': 'Morales Sanchez',
        'Age': 30,
        'MagicSkill': 'Light',
        'WizardRequestStatus': 'approved',
        'Grimorie':'one-leaf-clover'
    }
    wizard_request.update(values)
    return wizard_request

