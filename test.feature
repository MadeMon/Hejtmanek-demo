Feature: Test
    Background: 
        Given Kubernetes resource polling configuration
        | maxAttempts          | 10   |
        | delayBetweenAttempts | 1000 |


    Scenario: Pod is running
        Given Kubernetes pod labeled with app.kubernetes.io/instance=demo-application is running

    Scenario: GET request
        Given URL: http://demo-application
        When send GET /
        Then verify HTTP response body: Hello, World!
        And receive HTTP 200 OK
