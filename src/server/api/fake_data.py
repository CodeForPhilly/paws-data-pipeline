""" Fake data that can be returned when an API token is missing for local
    development, or for running pytest

    Shelterluv Data contains:
        Matched: Animal & Event End point
"""

shelterluv_data = {
    'animals': {
        "animal_details": {
            '12345': {
                "Age": 24,
                "DOBUnixTime": 1568480456,
                "Name": "Lola aka Fake Cat",
                "Type": "Cat",
                "Photos":
                ["https://images.unsplash.com/photo-1456926631375-92c8ce872def?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OHx8YW5pbWFsfGVufDB8fDB8fA%3D%3D&w=1000&q=80"],
                "Status": "Healthy In Home",
            },
        },
        "person_details": {
            "shelterluv_short_id": 2,
        },
    },
    'events': {
        '12345':[
            {
            'AssociatedRecords': [
                {'Id': 12345, 'Type': 'Animal' },
                {'Id': 12345, 'Type': 'Person'},
            ],
            'Subtype': 'Foster Home',
            'Time': '1602694822',
            'Type': 'Outcome.Adoption',
            'User': 'Fake User',
            },
        ]
    },
}


def sl_mock_data(end_point: str)-> dict:
    """ Shelterluv mock data.
        Takes the end_point as a str of `animals` or `events` and  returns
        a dict representing a test data for that end_point.
    """

    return shelterluv_data.get(end_point)
