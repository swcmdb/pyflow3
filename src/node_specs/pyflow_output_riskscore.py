def func(params, lastdays, dummy):
    """
    :ptypes: String, Int, String
    """
    from pymongo import MongoClient
    from cmdbpy.shared_mongo_functions import read_mongo, import_df
    from cmdbpy.func_output_risk_score import create_wt_risk_score
    from cmdbpy.shared_text_functions import find_new_entity
    from cmdbpy.shared_utils_functions import create_epoch_time
    import pkg_resources
    import pandas as pd
    import time
    db = MongoClient('mongo', 27017).test_database
    RESOURCE_PATH = pkg_resources.resource_filename('cmdbpy', '/resources/')
    import sys
    sys.stdout = open("/tmp/output_riskscore_log.txt", "w")
    
    if params is None or len(params) < 1:
        params = "model_parameters.yaml"

	# Concatenate all device outputs
    aws = read_mongo(db, 'AWS_Output')
    endpoint = read_mongo(db, 'CMDB_Output')
    combined = pd.concat([aws, endpoint], axis=0, sort=False)
    
    # Create risk score with weight table
    combined = create_wt_risk_score(RESOURCE_PATH, combined, params, "yaml")
    combined['Is_Cloud_Device'] = combined['AWS_Account_ID'].apply(lambda x: 0 if pd.isnull(x) else 1)
    
    # Create timestamp and new entity indicators based on last 7 days
    create_epoch_time(combined)
    last_days = int(time.time()) - 60 * 60 * 24 * lastdays
    try:
        hist = read_mongo(db, 'AWS_CMDB_Output', query={'_time': {'$gt': last_days}})
    except:
        hist = None
    _, _, combined = find_new_entity(combined, hist, 'Asset_Name', append=True)
    _, _, combined = find_new_entity(combined, hist, 'Owner_Email', append=True)
    
    # Append results back to MongoDB: Don't create sourcetype, keep previous records
    import_df(combined, db, 'AWS_CMDB_Output', False, False)
    
    sys.stdout = sys.__stdout__
    with open("/tmp/output_riskscore_log.txt") as f:
        out = f.read()
    return out + "Calculating Risk Score ...... Done"

