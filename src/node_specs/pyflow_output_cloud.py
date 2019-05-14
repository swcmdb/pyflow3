def func(dummy):	
    from pymongo import MongoClient
    from cmdbpy.shared_mongo_functions import *
    db = MongoClient('mongo', 27017).test_database
    import sys
    sys.stdout = open("/tmp/output_cloud_log.txt", "w")
    
    # Create cloud output
    _ = mongo_fillna(db, 'AWS_Combine', 'AWS_Risk',
             ['Is_EP_Installed', 'Is_IDS_Network', 'PCI_VPC_IP_Data.Likelihood', 'Tenable_Data.Count_High_Severity_Vuln'],
             ['HostIDS_Log', 'NetworkIDS_Log', 'PCI_Likelihood', 'High_Severity_Vuln'], 0.0)

    _ = mongo_binary(db, 'AWS_Risk', 'AWS_Risk',
                 ['Tenable_Data.Count_High_Severity_Vuln'],
                 ['VA_Scan'])

    _ = mongo_reverse_binary(db, 'AWS_Risk', 'AWS_Risk',
                 ['HostIDS_Log', 'Is_CloudTrail_Log', 'Is_IDS_Network', 'VA_Scan', 'Is_Managed_Asset'],
                 ['HostIDS_Not_Log', 'CloudTrail_Not_Log', 'NetworkIDS_Not_Log', 'VA_Not_Scan', 'Not_Managed'])
    
    _ = mongo_set_data_risk(db, 'AWS_Risk', 'AWS_Risk', 'PCI_Likelihood', 4.0, 'Restricted', 'PCI')
    
    # Consolidate same fields from different sources
    _ = mongo_unwind_fields(db, 'AWS_Risk', 'AWS_Output', ['Tenable_Data'])

    _ = mongo_consolidate_fields(db, 'AWS_Output', 'AWS_Output',
                             ['Last_Discovered_Datetime', 'Tenable_Data.Last_Discovered_Datetime'],
                             'Last_Discovered_Datetime', 'max')
    
    _ = mongo_consolidate_fields(db, 'AWS_Output', 'AWS_Output',
                             ['First_Discovered_Datetime', 'Tenable_Data.First_Discovered_Datetime'],
                             'First_Discovered_Datetime', 'min')
    
    _ = mongo_consolidate_fields(db, 'AWS_Output', 'AWS_Output',
                             ['IP_Address', 'PCI_VPC_IP_Data.IP_Address', 'Tenable_Data.IP_Address'],
                             'IP_Address', 'union')
    
    _ = mongo_consolidate_fields(db, 'AWS_Output', 'AWS_Output',
                             ['MAC_Address', 'Tenable_Data.MAC_Address'],
                             'MAC_Address', 'union')
    
    _ = mongo_consolidate_fields(db, 'AWS_Output', 'AWS_Output',
                             ['AWS_Account_ID', 'PCI_VPC_IP_Data.aws_account_id'],
                             'AWS_Account_ID', 'union', arrayelem=0)
    
    sys.stdout = sys.__stdout__
    with open("/tmp/output_cloud_log.txt") as f:
        out = f.read()
    return out + "Creating Cloud Output ...... Done"
