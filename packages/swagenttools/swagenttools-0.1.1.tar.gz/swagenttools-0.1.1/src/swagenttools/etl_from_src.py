import os
import time
import pandas as pd
from .seeker import UserAgent, Seeker
from sqlalchemy import create_engine


################################################################
#                     extract_from_src                         #
################################################################
def extract_from_src(content_size):
    """ > gets raw data from site, assigns new useragent
        ______________________________________________________

        params:
            - content_size: number of replays to collect

        returns:
            - JSON formatted object with (content_size) records 

    """
    # extract data from source <swranking.com>
    seeker = Seeker(UserAgent('Chrome').random_agent(), pageSize=content_size)
    matches = seeker.get_matches()
    return matches


################################################################
#                         transform                            #
################################################################
def transform(matches):
    """ > strips the returned json and makes dataframe
        ______________________________________________________

        params:
            - matches: JSON formatted object with raw data

        returns:
            - df: fully parsed dataframe ready to transport to db
    """
    # check if data was in the correct format
    if (matches == None) and (matches['retCode'] != 0) and (matches['enMessage'] != 'Success'):
        return False # data was unsuccessful -> based on return should rerun function

    replays = []
    matches = matches['data']['list']
    for match in matches:
        replays.append({
            # replay information
            'replay_id': match['replayId'],
            'created_at': match['createDate'],
            'winner': match['status'],

            # get all the info for player 1
            'player1_id': match['playerOne']['playerId'],
            'player1_name': match['playerOne']['playerName'].strip(),
            'player1_country': match['playerOne']['playerCountry'],
            'player1_rank': match['playerOne']['playerRank'],
            'player1_score': match['playerOne']['playerScore'],

            # get all the info for player 2
            'player2_id': match['playerTwo']['playerId'],
            'player2_name': match['playerTwo']['playerName'].strip(),
            'player2_country': match['playerTwo']['playerCountry'],
            'player2_rank': match['playerTwo']['playerRank'],
            'player2_score': match['playerTwo']['playerScore'],

            # the draft monster player 1 chose and the leader banned monsters by id
            'p1_unit1_id': match['playerOne']['monsterInfoList'][0]['monsterId'],
            'p1_unit2_id': match['playerOne']['monsterInfoList'][1]['monsterId'],
            'p1_unit3_id': match['playerOne']['monsterInfoList'][2]['monsterId'],
            'p1_unit4_id': match['playerOne']['monsterInfoList'][3]['monsterId'],
            'p1_unit5_id': match['playerOne']['monsterInfoList'][4]['monsterId'],
            'p1_unit_leader': match['playerOne']['leaderMonsterId'],
            'p1_unit_banned': match['playerOne']['banMonsterId'],
    
            # the draft monster player 2 chose and the leader banned monsters by id
            'p2_unit1_id': match['playerTwo']['monsterInfoList'][0]['monsterId'],
            'p2_unit2_id': match['playerTwo']['monsterInfoList'][1]['monsterId'],
            'p2_unit3_id': match['playerTwo']['monsterInfoList'][2]['monsterId'],
            'p2_unit4_id': match['playerTwo']['monsterInfoList'][3]['monsterId'],
            'p2_unit5_id': match['playerTwo']['monsterInfoList'][4]['monsterId'],
            'p2_unit_leader': match['playerTwo']['leaderMonsterId'],
            'p2_unit_banned': match['playerTwo']['banMonsterId']
        })

    # at this point you want to save the data or load it into a DB
    # pd.set_option("display.unicode.east_asian_width", True)
    df = pd.DataFrame.from_dict(replays)
    df['created_at'] = pd.to_datetime(df['created_at'])

    print("{} new replays were retrieved from site...".format(len(df)))
    return df


################################################################
#                    load_batch_to_db                          #
################################################################
def load_batch_to_DB(batch, connection):
    """ > appends the newly found data to the full_replays db.
        _______________________________________________________

        params:
            - batch: dataframe with new data (size X)
            - connection: the engine or conn format variable
    """
    try:
        # start a count
        error_cnt = 0
        for i, row in batch.iterrows():
            # get the results of the next value to append 
            sql = "SELECT * FROM full_replays WHERE replay_id = {}".format(row.replay_id)
            found = pd.read_sql(sql, con=connection)

            # if value found in db dont add else add
            if len(found) == 0:
                batch.iloc[i:i+1].to_sql(name="full_replays", if_exists='append', con=connection, index=False)
            else:
                error_cnt += 1
            
            if i == len(batch) % 100:
                print('progressing... {}/{}'.format(i+1, len(batch)))
        # print the amount of results that were actually added to the db    
        print("{} new replays were added...".format(len(batch) - error_cnt))
    except Exception as error:
        print('Error while appending to PostgreSQL', error)


################################################################
#                         db_connect                           #
################################################################
def db_connect(user, pass_env, db, port=5432, host='localhost'):
    """ > makes connection with specified database
        ________________________________________________________
        
        params:
            - user: user registered in database.
            - pass_env: name of the environment variable assigned 
            the password for the db.
            -db: name of db from where to make changes or extract 
            data.
            - port: port adress, default 5432
            - host: host address, default localhost 

        returns:
            - the engine after a connection has been established.
    """
    try:
        # connection string contains all necessary info
        connection_string = "postgresql://{}:{}@{}:{}/{}".format(user, os.getenv(pass_env), host, port, db)
        engine = create_engine(connection_string)
        # log connection established. 
        print("\nYou are connected to --->", engine.url.database, "\n") 
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if engine is not None:
            return engine # return engine only



if __name__ == '__main__':
    # set up the engine
    engine = db_connect(user='oulex', pass_env='swagent_db_password', db='sw-agent')

    # for testing purposes only
    itr = 10
    delay = 30
    for i in range(itr):
        print('Starting sequence... {}/{}'.format(i+1, itr))
        matches = extract_from_src(10)
        matches = transform(matches)
        load_batch_to_DB(matches, connection=engine)
        time.sleep(delay)
 
