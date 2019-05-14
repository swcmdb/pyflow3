def func(dummy):
    from pymongo import MongoClient
    from cmdbpy.shared_mongo_functions import *
    db = MongoClient('mongo', 27017).test_database
    import sys
    sys.stdout = open("/tmp/join_cloud_log.txt", "w")
    
    # Merge cloud device data
    db['AWS_EC2_IP'].drop()
    db['AWS_EC2'].aggregate([{"$addFields" : {"AWS_IP":{"$concat":[{"$toString" : "$AWS_Account_ID"}, "|", 
                                                                   {"$toString" : "$IP_Address"}]}}},
                             {"$out" : "AWS_EC2_IP"}
                            ])
    db['PCI_VPC_IP'].drop()
    db['PCI_VPC_WtPageRank'].aggregate([{"$addFields" : {"AWS_IP":{"$concat":[{"$toString" : "$aws_account_id"}, "|", 
                                                                              {"$toString" : "$IP_Address"}]}}},
                             {"$out" : "PCI_VPC_IP"}
                            ])
    mongo_lookup(db, 'AWS_EC2_IP', 'Tenable', 'Asset_Name')
    mongo_fulljoin(db, 'AWS_EC2_IP|Tenable', 'PCI_VPC_IP', "AWS_IP")
    mongo_lookup(db, 'AWS_EC2_IP|Tenable|PCI_VPC_IP', 'LINUX_SECURE', 'Asset_Name', 'Asset_Name', 
                 True, 'Asset_Name', 'AWS_Combine')
    
    sys.stdout = sys.__stdout__
    with open("/tmp/join_cloud_log.txt") as f:
        out = f.read()
    return out + 'Joining Cloud Device Data ...... Done'
