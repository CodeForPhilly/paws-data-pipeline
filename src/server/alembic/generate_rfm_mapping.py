import itertools
import structlog
logger = structlog.get_logger()

def get_all_combinations(chars):
    yield from itertools.product(*([chars] * 3))


def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str


def start():
    mapping_rows = []

    mapping_rows.append(
        '''-- Run this script in your SQL query tool
-- Run truncate command if this table is already populated
-- TRUNCATE TABLE rfm_mapping; 
-- BEGIN;
-- Fields are                 (rfm_score, label, (background) color, text color)
        '''
    )

    combinations = []
    for x in get_all_combinations('12345'):
        combinations.append(convertTuple(x))

    for rfm_score in combinations:
        label = ''
        background_color = ''
        color_text = ''
        r_m_average = (int(rfm_score[1]) + (int(rfm_score[2]))) / 2
        r = int(rfm_score[0])

        if r == 5 and (3 < r_m_average <= 5):
            label = 'High impact, engaged'
            background_color = '#034858'
            color_text = '#ffffff'
        elif r == 5 and (1 <= r_m_average <= 3):
            label = 'Low impact, engaged'
            background_color = '#47b8a7'
            color_text = '#000000'
        elif (3 <= r <= 4) and (3 < r_m_average <= 5):
            label = 'High impact, slipping'
            background_color = '#990000'
            color_text = '#ffffff'
        elif (3 <= r <= 4) and (1 <= r_m_average <= 3):
            label = 'Low impact, slipping'
            background_color = '#f77d4e'
            color_text = '#000000'
        elif (1 <= r <= 2) and (3 < r_m_average <= 5):
            label = 'High impact, disengaged'
            background_color = '#cf3030'
            color_text = '#ffffff'
        elif (1 <= r <= 2) and (1 <= r_m_average <= 3):
            label = 'Low impact, disengaged'
            background_color = '#eed0aa'
            color_text = '#000000'

        mapping_rows.append(
            "insert into rfm_mapping values('{}', '{}','{}', '{}');".format(rfm_score, label, background_color,
                                                                            color_text))

    mapping_rows.append('-- COMMIT;')

    with open('populate_rfm_mapping.sql', 'w') as f:
        for item in mapping_rows:
            f.write("%s\n" % item)


    logger.debug('Completed generate_rfm_mapping')


start()
