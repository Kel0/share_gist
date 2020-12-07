# Introduction
Share-Gist was built from ground-up with REST API that makes it easy for developers.

These docs describe how to use Share-Gist API. 

# Responses
Share-Gist API returns json response in following format:
```python
{
    "status": int,
    "details": list or dict or str
}
```
The `status` attribute indicates status of response

The `details` attribute contains callback data, or error message in case when exception will raise.


## Status Codes

Share-Gist API returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |


# Access
You should append the api_token=[API_KEY] as a GET parameter to authorize yourself to the API. 

```http
GET /api/v1/method/?api_token=API_TOKEN
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_token` | `string` | **Required**. Your Share-Gist API key |


# Methods
### Lexers
<hr>

#### Get all lexers 
i.e.: Python, Json, JavaScript etc...

```http
GET /api/v1/lexers/?api_token=...
```
Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_token` | `string` | **Required**. Your Share-Gist API key |

Success response example

```json
{
  "status": 200,
  "details": [
    {
      "model": "paste.lexer",
      "pk": 1,
      "fields": {
        "name": "json"
      }
    },
    {
      "model": "paste.lexer",
      "pk": 2,
      "fields": {
        "name": "python"
      }
    }
  ]
}
```
<hr>

#### Create lexer
```http
POST /api/v1/lexers/?api_token=...
```

Required data

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `lexer_name` | `string` | **Required**. Lexer's name |

Python example
```python
import json

import requests


resp = requests.post("/api/v1/lexers/?api_token=...", data=json.dumps(
    {"lexer_name": "Ruby"}
))
print(resp.content)  # b'{"status": 201, "details": {"id": 8, "name": "Ruby"}}'
```

### Pastes
#### Get paste 

```http
GET /api/v1/snippet/?api_token=...&uuid=25215afe-8421-26fg-820b-a8a15909c179
```

Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_token` | `string` | **Required**. Your Share-Gist API key |
| `uuid` | `string` | **Required**. Unique id of paste |


Success response example

```json
{
  "status": 200,
  "details": {
    "id": 1,
    "lex": {
      "id": 1,
      "name": "json"
    },
    "uuid": "26231afe-3887-11eb-820b-a8a15909c179",
    "content": "<div class=\"highlight\"><pre><span></span><a name=\"True-1\"></a><span class=\"err\">get_paste_by_id_as_list</span>\n</pre></div>\n",
    "inspiration_date": "2020-12-15T16:26:52.904"
  }
}
```

#### Create paste

```http
POST /api/v1/snippet/?api_token=...
```

Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `lexer_id` | `integer` | **Required**. Unique id of lexer |
| `code` | `string` | **Required**. Code for paste |
| `inspiration_date` | `integer` | **Optional**. Inspiration date of paste |


Success response example

```json
{
  "status": 201,
  "details": {
    "id": 18,
    "lex": "1",
    "uuid": "2e336924-3972-11eb-be0a-a8a15909c179",
    "content": "print('HELLO, WORLD!')",
    "inspiration_date": "2020-12-15T16:26:52.904"
  }
}
```