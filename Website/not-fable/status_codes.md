## 1xx: Informational

Indicate that the request has been received and the process is continuing.

Examples:

100 Continue: The client should continue with the request.

101 Switching Protocols: The server is switching protocols as requested.

## 2xx: Successful

Indicate that the request was successfully received, understood, and accepted.

Examples:

200 OK: The request was successful.

201 Created: A new resource has been created.

204 No Content: The request was successful but no content is returned.

## 3xx: Redirection

Indicate that further action is needed to fulfill the request.

Examples:

301 Moved Permanently: The resource has been moved permanently to a new URL.

302 Found: The resource is temporarily under a different URL.

304 Not Modified: The resource has not been modified since last requested.

## 4xx: Client Error

Indicate errors caused by the client.

Examples:

400 Bad Request: The server cannot process the request due to client error.

401 Unauthorized: Authentication is required and has failed or is missing.

403 Forbidden: The client does not have access rights.

404 Not Found: The requested resource could not be found.

409 Conflict: The request could not be completed due to a conflict.

## 5xx: Server Error

Indicate errors caused by the server.

Examples:

500 Internal Server Error: The server encountered an unexpected condition.

502 Bad Gateway: The server received an invalid response from an upstream server.

503 Service Unavailable: The server is currently unable to handle the request.

504 Gateway Timeout: The server did not receive a timely response.

