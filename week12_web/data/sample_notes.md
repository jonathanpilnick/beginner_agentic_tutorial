# Sample study notes: HTTP and web APIs

(Sample notes for trying the project starter. Paste your own notes instead.)

- HTTP is the protocol browsers and programs use to talk to web servers: a client sends a request, the server sends back a response.
- A request has a method (GET to read, POST to send data, DELETE to remove), a path such as /api/chat, headers, and sometimes a body.
- A response has a status code: 200 OK, 400 Bad Request (the client sent something wrong), 401 Unauthorized (missing or wrong credentials), 404 Not Found, 503 Service Unavailable.
- JSON is the usual body format for web APIs. Python dicts and lists map to JSON objects and arrays.
- REST is an architectural style for APIs: resources have URLs, and the HTTP method says what to do with them.
- Secrets such as tokens and API keys belong in environment variables, never in the code or in git.
