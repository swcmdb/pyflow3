def func(topics, words, dummy):
    """
    :ptypes: Int,Int
    :returns: out
    :rtype: String
    """
    from pymongo import MongoClient
    from cmdbpy.func_file_sharing_topic import cloud_file_topic
    import sys
    sys.stdout = open("/tmp/ml_topic_log.txt", "w")
    
    box_topic = cloud_file_topic(db=MongoClient('mongo', 27017).test_database, 
                               query={"sourcetype":"BOX_FILE"}, 
                               sourcetype='BOX_FILE',
                               outsourcetype = 'BOX_FILE_Topic',
                               userid='Owner_Email',
                               textfield='Box_File_Name',
                               mongo=True,
                               num_topics=topics,
                               num_words=words)
    
    sys.stdout = sys.__stdout__
    with open("/tmp/ml_topic_log.txt") as f:
        out = f.read()
    return out + "File sharing results ready in MongoDB"
