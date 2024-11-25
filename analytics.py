SUBMIT_QUERY="""
mutation testMutation($limit: Int!, $start_time: DateTime!, $end_time: DateTime!) {
  submitAnalyticsQueryBatch(
    input: {
      batchScope: "API_FETCH"
      executeAsync: true
      queries: [
        {
          name: "query_list"
          scope: "API_TRACE"
          limit:$limit
          between: {
            startTime:$start_time
            endTime:$end_time
          }
          filterBy: [
            {
              keyExpression: { key: "environment" }
              operator: EQUALS
              value: "nec"
              type: ATTRIBUTE
            }
          ]
          orderBy: [{ direction: DESC, keyExpression: { key: "startTime" } }]
          selections: [
            { expression: { key: "protocol" } }
            { expression: { key: "startTime" } }
            { expression: { key: "requestUrl" } }
            { expression: { key: "requestMethod" } }
            { expression: { key: "ipAddress" } }
          ]
        }
      ]
    }
  ) {
    author
    batchId
    executionMode
    creationTimestamp
    queryDetails {
      query {
        between {
          startTime
          endTime
        }
        name
        scope
        limit
        offset
        orderBy {
          aggregation
          keyExpression {
            key
            subpath
          }
          direction
          size
        }
        selections {
          aggregation
          expression {
            key
            subpath
          }
          size
          units
        }
        filterBy {
          idScope
          keyExpression {
            key
            subpath
          }
          operator
          type
          value
        }
        groupBy {
          groupLimit
          includeRest
          expressions {
            key
            subpath
          }
        }
        interval {
          size
          units
        }
      }
      state
    }
    query_list: queryResult(name: "query_list", scope: "API_TRACE") {
      results {
        protocol: selection(expression: { key: "protocol" }) {
          value
          type
        }
        startTime: selection(expression: { key: "startTime" }) {
          value
          type
        }
        requestUrl: selection(expression: { key: "requestUrl" }) {
          value
          type
        }
        requestMethod: selection(expression: { key: "requestMethod" }) {
          value
          type
        }
        ipaddress: selection(expression: { key: "ipAddress" }) {
          value
          type
        }
      }
      count
      total
    }
  }
}
"""

COUNT_QUERY="""
mutation ct($start_time: DateTime!, $end_time: DateTime!) {
  submitAnalyticsQueryBatch(
    input: {
      batchScope: "API_FETCH"
      queries: [
        {
          name: "count"
          scope: "API_TRACE"
          limit: 1
          between: {
            startTime: $start_time
            endTime: $end_time
          }
          filterBy: [
            {
              keyExpression: { key: "environment" }
              operator: EQUALS
              value: "nec"
              type: ATTRIBUTE
            }
          ]

          orderBy: [
            {
              aggregation: COUNT
              direction: DESC
              keyExpression: { key: "calls" }
            }
          ]
          selections: [{ expression: { key: "calls" }, aggregation: COUNT }]
        }
      ]
    }
  ) {
       batchId,
       executionMode
       count_query: queryResult(name: "count", scope: "API_TRACE") {
       results {
         count_calls: selection(
          expression: { key: "calls" }
          aggregation: COUNT
        ) {
          value
          type
          __typename
        }
        __typename
       }
      __typename
     }
   }
}
"""


FETCH_DATA="""
query testQuery($batchId: String!, $limit: Int!, $offset: Int!){
  analyticsQueryBatch(batchId: $batchId) {
    author
    batchId
    creationTimestamp
    expirationTimestamp
    executionMode
    queryDetails {
      query {
        limit
        offset
      }
    }
    state
    query_list: queryResult(name: "query_list", limit: $limit, offset: $offset, scope: "API_TRACE") {
      results {
        protocol: selection(expression: { key: "protocol" }) {
          value
          type
        }
        startTime: selection(expression: { key: "startTime" }) {
          value
          type
        }
        requestUrl: selection(expression: { key: "requestUrl" }) {
          value
          type
        }
        requestMethod: selection(expression: { key: "requestMethod" }) {
          value
          type
        }
        ipaddress: selection(expression: { key: "ipAddress" }) {
          value
          type
        }
      }
      count
      total
    }
  }
}"""


CHECK_STATUS="""
query checkStatus($batchId: String!){
  analyticsQueryBatch(batchId: $batchId) {
    author
    batchId
    creationTimestamp
    expirationTimestamp
    executionMode
    state
  }
}
"""