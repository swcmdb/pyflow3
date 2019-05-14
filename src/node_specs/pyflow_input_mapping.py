def func(maxsearches, ratiothreshold, dummy):
    """
    :ptypes: Int,Float
    """
    import os
    import pandas as pd
    import pkg_resources
    import splunklib.client as client
    from cmdbpy.func_input_automatic_mapping import automatic_data_mapping, update_spl_query, read_spl_files, exec_spl_files
    from cmdbpy.shared_splunk_functions import execute_query
    from cmdbpy.shared_mongo_functions import import_df
    from pymongo import MongoClient
    import sys
    sys.stdout = open("/tmp/input_mapping_log.txt", "w")
    db = MongoClient('mongo', 27017).test_database
    RESOURCE_PATH = pkg_resources.resource_filename('cmdbpy', '/resources/')
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
    
	# Read pre-defined data sources
    predefine = pd.read_csv(os.path.join(RESOURCE_PATH, 'Data Source Mapping.csv'))
    predefine = predefine.fillna('')
    
    # Run automatic mapping
    automatic_mapping, spl_update, splunk = automatic_data_mapping(RESOURCE_PATH, SERVICE, 
                                                                   maxsearches=maxsearches, 
                                                                   outputfile=False, 
                                                                   ratiothreshold=ratiothreshold)
    import_df(predefine, db, 'Predefined_Data_Layout', False)
    import_df(automatic_mapping, db, 'Auto_Mapping_Output', False)
    import_df(spl_update, db, 'SPL_Update_Query', False)
    import_df(splunk, db, 'Splunk_Data_Layout', False)

    index_list = ','.join(list(automatic_mapping['customer_index'].unique()))
    sys.stdout = sys.__stdout__
    with open("/tmp/input_mapping_log.txt") as f:
        out = f.read()
    return out + "Automatic data mapping ...... Done - " + index_list
