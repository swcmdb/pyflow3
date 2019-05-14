def func(dummy):
    from pymongo import MongoClient, TEXT
    db = MongoClient('mongo', 27017).test_database
    import sys
    sys.stdout = open("/tmp/output_final_log.txt", "w")
    
    # Create text index on every field that contains string data for each document in the collection
    # To search any text in the index, use {$text: {$search: 'your_search_string'}} under MongoDB
    db['AWS_CMDB_Output'].create_index([('$**', TEXT)], name='search_index')
    
    # Clean up temporary data
    drop_list = ['AD_User|BOX_FILE_Topic', 'AWS_EC2_IP|Tenable', 'AWS_EC2_IP|Tenable|PCI_VPC_IP',
                 'Infoblox|SentinelOne', 'Infoblox|SentinelOne|JAMF']
    for d in drop_list:
        db[d].drop()
        
    sys.stdout = sys.__stdout__
    with open("/tmp/output_final_log.txt") as f:
        out = f.read()
    return out + "Final Combined Output Indexed ...... Done"
