def func(spl_filepath, mapping_output, dummy):
    import pkg_resources
    from cmdbpy.func_input_automatic_mapping import update_spl_query, read_spl_files, write_spl_files
    from cmdbpy.shared_mongo_functions import read_mongo
    from pymongo import MongoClient
    import sys
    sys.stdout = open("/tmp/input_updatespl_log.txt", "w")
    db = MongoClient('mongo', 27017).test_database
    RESOURCE_PATH = pkg_resources.resource_filename('cmdbpy', '/resources/')
    if spl_filepath is None or len(spl_filepath) < 2:
        spl_filepath = RESOURCE_PATH
    if mapping_output is None or len(mapping_output) < 2:
        mapping_output = 'Auto_Mapping_Output'
    
    # Load mapping output from MongoDB
    data_mapping = read_mongo(db, mapping_output)
    # Update pre-defined SPL queries from the mapping
    spl_update = update_spl_query(read_spl_files(spl_filepath), data_mapping)
    # Write queries to txt files
    write_spl_files(spl_filepath, spl_update, 'spl_query', 'spl_filename')
    
    sys.stdout = sys.__stdout__
    with open("/tmp/input_updatespl_log.txt") as f:
        out = f.read()
    return out + "Updated SPL files under: " + spl_filepath
    
    
