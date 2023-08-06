from utils.schema import get_event_schema
from validations.schema_validation import validate_schema


def perform_quality_control(data):
    if (__is_accepted(data)):
        print('perform_quality_control move data to accepted area')
    else:
        print('perform_quality_control reject data')


def __is_accepted(data):
    if not __has_valid_schema(data):
        return False
    return True


def __has_valid_schema(data):
    if 'DataSource' not in data:
        return False
    if 'EventName' not in data:
        return False
    
    data_source = data['DataSource']
    event_name = data['EventName']
    
    schema = get_event_schema(data_source=data_source, event_name=event_name)
    return validate_schema(schema=schema, data=data)
