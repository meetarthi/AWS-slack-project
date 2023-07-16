import psycopg2
import psycopg2.extras as extras
import requests
import json

def lambda_handler(event, context):
    # TODO implement
    
    server_status = False
    
    try:
        api = requests.get('http://api.open-notify.org/iss-now.json')
        data = json.loads(api.content)
        timestamp = data['timestamp']
        message_status = data['message']
        longitude_data = data['iss_position']['longitude']
        latitude_data = data['iss_position']['latitude']
        if message_status == "success":
            server_status = True
    except requests.exceptions.RequestException as e: 
        pass
        
    
    if server_status:
        conn = psycopg2.connect(
            host = 'database.h3axyzj0mace.ap-northeast-1.rds.amazonaws.com',
            port = 5432,
            user = 'username',
            password = 'ayx246',
            database = 'project'
        )
        
        cols = 'timestamp,message_status,longitude_data,latitude_data'
        data = [(timestamp, message_status, longitude_data, latitude_data)]
        query = "INSERT INTO %s(%s) VALUES %%s" % ('slack_data', cols)
        cursor = conn.cursor()
    
        try:
            extras.execute_values(cursor, query, data)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            cursor.close()
        print("the dataframe is inserted")
        cursor.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data saved in RDS')
        }
    else:
        raise Exception('Failed')