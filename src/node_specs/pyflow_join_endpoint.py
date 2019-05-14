def func(dummy):
    from pymongo import MongoClient
    from cmdbpy.shared_mongo_functions import *
    db = MongoClient('mongo', 27017).test_database
    import sys
    sys.stdout = open("/tmp/join_endpoint_log.txt", "w")
    
    # Merge endpoint data
    mongo_lookup(db, 'Infoblox', 'SentinelOne', 'Asset_Name')
    mongo_lookup(db, 'Infoblox|SentinelOne', 'JAMF', 'Asset_Name')
    mongo_lookup(db, 'Infoblox|SentinelOne|JAMF', 'Tenable', 'Asset_Name', 'Asset_Name',
                 False, 'Asset_Name', 'Endpoint_Combine')
    
    sys.stdout = sys.__stdout__
    with open("/tmp/join_endpoint_log.txt") as f:
        out = f.read()
    return out + 'Joining Endpoint Data ...... Done'
