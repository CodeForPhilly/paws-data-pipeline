from os import path

import structlog

logger = structlog.get_logger()


def find_pem_file():
    """
    Search likely places for the .pem file needed for SalesForce operations, 
    returning filename if found or empty string if not.
    """

    locations = ['server/bin', 'bin', 'server/pem']
    file_name = 'connected-app-secrets.pem'

    pem_file = ''

    for file_path in locations:
         if path.exists(path.join(file_path, file_name)):
            pem_file = path.normpath(path.join(file_path, file_name))
            logger.info("Found pem file at   %s   ", pem_file)
            break
        
    return pem_file