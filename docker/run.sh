#!/bin/bash
docker load < splunk_save.tar
docker load < metabase_save.tar
docker load < mongo_save.tar
docker load < python_save.tar
docker load < tomcat_save.tar
docker load < pyflow_save.tar
docker-compose up -d
