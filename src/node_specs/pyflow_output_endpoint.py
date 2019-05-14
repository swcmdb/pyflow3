def func(dummy):	
    from pymongo import MongoClient
    from cmdbpy.shared_mongo_functions import *
    db = MongoClient('mongo', 27017).test_database
    import sys
    sys.stdout = open("/tmp/output_endpoint_log.txt", "w")
    
    # Create Endpoint output
    mongo_lookup(db=db, 
                 src_collection='Endpoint_Combine', 
                 dst_collection='User_Combine', 
                 src_field='Asset_Name', 
                 dst_field='Asset_Name', 
                 mergeObj=True,
                 index_key='Asset_Name', 
                 out_collection='CMDB_Combine')
    
    # Create new fields for risk score calculation
    _ = mongo_fillna(db, 'CMDB_Combine', 'CMDB_Risk',
                 ['Data_Risk', 'SentinelOne_Data.Is_EP_Updated', 'SentinelOne_Data.Is_EP_Installed', 'SentinelOne_Data.Count_Threat'],
                 ['Data_Risk', 'EP_Updated', 'EP_Installed', 'EP_Infections'], 0.0)

    _ = mongo_fillna(db, 'CMDB_Risk', 'CMDB_Risk',
                 ['Data_Type', 'Data_Classification'],
                 fillvalue='Unknown')

    _ = mongo_binary(db, 'CMDB_Risk', 'CMDB_Risk',
                 ['Tenable_Data.Count_High_Severity_Vuln'],
                 ['VA_Scan']) 

    _ = mongo_reverse_binary(db, 'CMDB_Risk', 'CMDB_Risk',
                 ['Is_Managed_Asset', 'VA_Scan', 'SentinelOne_Data.Is_EP_Installed', 'SentinelOne_Data.Is_EP_Updated'],
                 ['Not_Managed', 'VA_Not_Scan', 'EP_Not_Installed', 'EP_Not_Updated']) 
    
    # Consolidate same fields from different sources
    _ = mongo_unwind_fields(db, 'CMDB_Risk', 'CMDB_Output', ['SentinelOne_Data', 'JAMF_Data'])

    _ = mongo_consolidate_fields(db, 'CMDB_Output', 'CMDB_Output',
                             ['Last_Discovered_Datetime', 'SentinelOne_Data.Last_Discovered_Datetime', 'JAMF_Data.Last_Discovered_Datetime'],
                             'Last_Discovered_Datetime', 'max')
    
    _ = mongo_consolidate_fields(db, 'CMDB_Output', 'CMDB_Output',
                             ['First_Discovered_Datetime', 'SentinelOne_Data.First_Discovered_Datetime', 'JAMF_Data.First_Discovered_Datetime'],
                             'First_Discovered_Datetime', 'min')
    
    _ = mongo_consolidate_fields(db, 'CMDB_Output', 'CMDB_Output',
                             ['IP_Address', 'SentinelOne_Data.IP_Address', 'JAMF_Data.IP_Address'],
                             'IP_Address', 'union')
    
    _ = mongo_consolidate_fields(db, 'CMDB_Output', 'CMDB_Output',
                             ['MAC_Address', 'SentinelOne_Data.MAC_Address', 'JAMF_Data.MAC_Address'],
                             'MAC_Address', 'union')

    sys.stdout = sys.__stdout__
    with open("/tmp/output_endpoint_log.txt") as f:
        out = f.read()
    return out + "Creating Endpoint Output ...... Done"
