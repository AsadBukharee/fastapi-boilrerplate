#!/bin/bash
set -e
echo -n "blah"
psql -v ON_ERROR_STOP=1 --username postgres --password postgres --dbname sso_idp <<-EOSQL
    CREATE USER asad With PASSWORD 'postgres';
    CREATE DATABASE khaiti_db;
    GRANT ALL PRIVILEGES ON DATABASE sso_idp TO postgres;

EOSQL