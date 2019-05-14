def func(edgeweight, dummy):
    from cmdbpy.func_network_flow_pagerank import network_flow_pagerank
    from pymongo import MongoClient
    import sys
    sys.stdout = open("/tmp/ml_pagerank_log.txt", "w")
    
    pci_vpc_wt_pr = network_flow_pagerank(db=MongoClient('mongo', 27017).test_database, 
                                          query={"sourcetype":"PCI_VPC"}, 
                                          sourcetype='PCI_VPC',
                                          outsourcetype='PCI_VPC_WtPageRank',
                                          weight=edgeweight,
                                          src_ip='src_ip',
                                          dest_ip='dest_ip',
                                          accountid='aws_account_id')
    
    sys.stdout = sys.__stdout__
    with open("/tmp/ml_pagerank_log.txt") as f:
        out = f.read()
    return out + "Graph model results ready in MongoDB"
