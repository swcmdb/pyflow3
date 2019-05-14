def func(dummy):
    from pymongo import MongoClient
    from cmdbpy.shared_mongo_functions import *
    db = MongoClient('mongo', 27017).test_database
    import sys
    sys.stdout = open("/tmp/join_user_log.txt", "w")
    
    # Merge endpoint data
    mongo_lookup(db, 'AD_User', 'BOX_FILE_Topic', 'Owner_Email', 'Owner_Email', True)
    mongo_lookup(db, 'AD_User|BOX_FILE_Topic', 'Lookup_BU_Data', 'Owner_Department', 'Owner_Department', 
                 True, 'Asset_Name', 'User_Combine')
    
    sys.stdout = sys.__stdout__
    with open("/tmp/join_user_log.txt") as f:
        out = f.read()
    return out + 'Joining User Data ...... Done'
