## `requests` library Methods

The `requests` library in Python provides various methods to interact with web services using HTTP. Here’s a table summarizing all the main methods available:

| **Method**           | **Description** | **Example Usage** |
|----------------------|---------------|------------------|
| `requests.get()`     | Sends an HTTP `GET` request to retrieve data. | `response = requests.get('https://api.example.com/data')` |
| `requests.post()`    | Sends an HTTP `POST` request to send data to a server. | `response = requests.post('https://api.example.com/data', json={"key": "value"})` |
| `requests.put()`     | Sends an HTTP `PUT` request to update a resource. | `response = requests.put('https://api.example.com/data/1', json={"key": "new_value"})` |
| `requests.patch()`   | Sends an HTTP `PATCH` request for partial updates. | `response = requests.patch('https://api.example.com/data/1', json={"key": "updated_value"})` |
| `requests.delete()`  | Sends an HTTP `DELETE` request to remove a resource. | `response = requests.delete('https://api.example.com/data/1')` |
| `requests.head()`    | Sends an HTTP `HEAD` request to fetch only headers. | `response = requests.head('https://api.example.com/data')` |
| `requests.options()` | Sends an HTTP `OPTIONS` request to check supported methods. | `response = requests.options('https://api.example.com/data')` |

### **Additional Methods in `requests`**

| **Method**                | **Description** | **Example Usage** |
|---------------------------|---------------|------------------|
| `response.json()`         | Parses response data as JSON. | `data = response.json()` |
| `response.text`           | Returns response content as a string. | `print(response.text)` |
| `response.content`        | Returns response content as raw bytes. | `print(response.content)` |
| `response.status_code`    | Gets the HTTP status code of the response. | `print(response.status_code)` |
| `response.headers`        | Retrieves response headers. | `print(response.headers)` |
| `requests.Session()`      | Creates a session to persist settings across requests. | `session = requests.Session()` |
| `requests.adapters`       | Allows customizing connection behavior. | `adapter = requests.adapters.HTTPAdapter()` |
| `requests.auth`           | Provides authentication support. | `requests.get(url, auth=('user', 'pass'))` |
| `requests.exceptions`     | Handles request-related errors. | `try: requests.get(url) except requests.exceptions.RequestException: pass` |

