import sys
import os
import psycopg2
import configParser
import subprocess

from typing import List

EXIT_TOO_FEW_ARGS = 1
ENV_VAR_USER = "RESUME_DB_USERNAME"
ENV_VAR_PASSWORD = "RESUME_DB_PASSWORD"
ENV_VAR_HOST = "RESUME_DB_HOST"
ENV_VAR_PORT = "RESUME_DB_PORT"

def load_env_vars(config:dict):

    config["host"] = os.getenv(ENV_VAR_HOST)
    if(config["host"] == None):
        raise ValueError("RESUME_DB_HOST environment variable not set")

    config["port"] = os.getenv(ENV_VAR_PORT)
    if(config["port"] == None):
        raise ValueError("RESUME_DB_PORT environment variable not set")

    config["user"] = os.getenv(ENV_VAR_USER)
    if(config["user"] == None):
        raise ValueError("RESUME_DB_USERNAME environment variable not set")

    config["password"] = os.getenv(ENV_VAR_PASSWORD)
    if(config["password"] == None):
        raise ValueError("RESUME_DB_PASSWORD environment variable not set")

def main():
    
    if len(sys.argv) < 2:
        print("Missing config file path argument")
        exit(EXIT_TOO_FEW_ARGS)

    configFilePath = sys.argv[1]

    #parse config file
    config = configParser.ConfigParser.parse_file(configFilePath)
    load_env_vars(config=config)
 
    database = config["database"]
    
    host = config["host"]
    port = config["port"]
    user = config["user"]
    password = config["password"]
    

    # need to connect to the default db in case our db does not exist
    with psycopg2.connect(host=host,user=user,password=password,port=port,database="postgres") as create_connection:
        db_exists = check_db_exists(conn=create_connection,database=database,user=user,password=password)
        if db_exists == False:
            print(f"Database {database} does not exist yet. Please create it")
            exit()
    
    update_proc_params = None
    if(args_has_rollback(sys.argv)):
        # do rollback
        return # implement later
    else:
        # plain update
        update_proc_params = get_update_proc_params(config=config)
    
    print("Running liquibase from: "+os.getcwd())
    print("Running: "+" ".join(update_proc_params))


    liquibase_proc_result = subprocess.call(args=update_proc_params)

    print("Liquibase run result: "+str(liquibase_proc_result))

def args_has_rollback(args : List[str]) -> bool:
    try:
        args.index("rollback")
        return True
    except ValueError:
        return False

def get_jdbc_url(config:dict) -> str:
    database = config["database"]
    host = config["host"]
    port = config["port"]

    url = f"jdbc:postgresql://{host}:{port}/{database}"

    return url

# get proc params for a typical liquibase run
def get_update_proc_params(config:dict) -> List[str]:
    
    log_level = config["liquibaseLogLevel"]
    change_file:str = config["liquibaseChangeFile"]
    username = config["user"]
    password = config["password"]
    url = get_jdbc_url(config=config)

    liquibase_command = ""
    search_path:str = "./tools/liquibase/sql/"
    command = "update"

    if os.name == "nt":
        liquibase_command = "tools\liquibase\lib\liquibase\liquibase.bat"
        change_file = change_file.replace("/","\\")
        search_path = search_path.replace("/","\\")
    else:
        liquibase_command = "tools\liquibase/lib/liquibase/liquibase"


    params = [
        liquibase_command,
        f"--search-path={search_path}",
        f"--log-level={log_level}",
        command,
        f"--url={url}",
        f"--changelog-file={change_file}",
        f"--username={username}",
        f"--password={password}"
    ]

    return params


# create the specified database if needed. This allows us to run the tool without
# pre-creating the required database
def check_db_exists(conn: psycopg2.connect,database:str,user:str,password:str) -> bool: 

    has_db = False
    
    with conn.cursor() as cursor:
        show_db_sql = f"SELECT datname FROM pg_database WHERE datname LIKE '{database}'"
        cursor.execute(show_db_sql)
        has_db = cursor.fetchone()
        cursor.close()

    return has_db != None



if __name__ == "__main__":
    main()