def func(spl_filepath, file_keyword, dummy):
    import os
    import pandas as pd
    import pkg_resources
    import splunklib.client as client
    from cmdbpy.func_input_automatic_mapping import automatic_data_mapping, update_spl_query, read_spl_files, exec_spl_files
    from cmdbpy.shared_splunk_functions import execute_query
    from cmdbpy.shared_mongo_functions import import_df
    from pymongo import MongoClient
    import sys
    sys.stdout = open("/tmp/input_runspl_log.txt", "w")
    db = MongoClient('mongo', 27017).test_database
    RESOURCE_PATH = pkg_resources.resource_filename('cmdbpy', '/resources/')
    if spl_filepath is None or len(spl_filepath) < 2:
        spl_filepath = RESOURCE_PATH
    if file_keyword is None or len(file_keyword) < 2:
        file_keyword = 'SPLUNK_'
    # Splunk server settings
    HOST = "splunk"
    PORT = 8089
    USERNAME = "admin"
    PASSWORD = '12345678'
    SERVICE = client.connect(
                host=HOST,
                port=PORT,
                username=USERNAME,
                password=PASSWORD,
                verify=False)
    
    # Run SPL query files in batch and import data into MongoDB
    data, names, errors = exec_spl_files(SERVICE, RESOURCE_PATH, db=db)
    
    sys.stdout = sys.__stdout__
    with open("/tmp/input_runspl_log.txt") as f:
        out = f.read()
    return out + "ERROR LIST: " + ",".join(errors)
    
