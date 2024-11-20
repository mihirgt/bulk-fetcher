from python_graphql_client import GraphqlClient
import analytics
from datetime import datetime, timedelta
from time import sleep

start_time = datetime.fromisoformat("2024-11-18T00:00:00.000")
end_time = start_time

# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://api.traceable.ai/graphql")
api_key = "put your api key here"

headers = {
    "Authorization": api_key
}

# pull data for 24 hours in 1 hour increments
for x in range(1, 24):
    start_time = end_time
    end_time = start_time + timedelta(hours=1)
    # fetch count in time range
    st = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    et = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    count_variables = {
        "start_time": st,
        "end_time": et
    }
    data = client.execute(analytics.COUNT_QUERY, variables=count_variables, headers=headers)
    batch_count = data['data']['submitAnalyticsQueryBatch']['count_query']['results'][0]['count_calls']['value']

    # fire submit query
    variables = {
        "limit": batch_count,
        "start_time": st,
        "end_time": et
    }
    data = client.execute(analytics.SUBMIT_QUERY, variables=variables, headers=headers)
    batchId = data['data']['submitAnalyticsQueryBatch']['batchId']

    #check status
    check_variable = {
        "batchId": batchId
    }
    data = client.execute(analytics.CHECK_STATUS, variables=check_variable, headers=headers)
    status = data['data']['analyticsQueryBatch']['state']
    while status != "SUCCEEDED":
        sleep(10)
        data = client.execute(analytics.CHECK_STATUS, variables=check_variable, headers=headers)
        status = data['data']['analyticsQueryBatch']['state']

    offset = 0
    max_fetch = 100
    while offset < batch_count:

        fetch_variables = {
            "batchId": batchId,
            "limit": max_fetch,
            "offset": offset
        }
        data = client.execute(analytics.FETCH_DATA, variables=fetch_variables, headers=headers)
        print(data)
        if offset + max_fetch + 1 < batch_count:
            offset = offset + max_fetch + 1
