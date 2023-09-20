
import boto3
import pyodbc

def lambda_handler(event, context):
    try:
        # Extract user-submitted data from the event
        #event['firstName'] = 'bindu venkata raghav'
        #event['lastName'] = 'dukka'
        first_name = event['firstName']
        last_name = event['lastName']
        data = f"First Name: {first_name}, Last Name: {last_name}"
        
        # Store data in S3
        s3 = boto3.client('s3')
        bucket_name = 'end-to-end-chandu'
        object_key = 'data_file.txt'
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)
        
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=database-4.cd7jlzbbidqi.us-east-2.rds.amazonaws.com,1433;Database=test;Uid=admin;Pwd=Chandu55;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

        cursor = conn.cursor()
        query = f"INSERT INTO names (fname, lname) VALUES ('{first_name}', '{last_name}')"
        cursor.execute(query)
        conn.commit()
        conn.close()
        
        return {
            'statusCode': 200,
            'body': 'Data stored in S3 and MySQL successfully.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
