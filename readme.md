# API Documentation

**Common Notes**
1. Authentication:
  - All routes require session authentication via `db`, `username`, and `password`.
2. Error Handling:
  - Error responses provide an HTTP status code (e.g., `404` for missing records or `500` for server errors) along with a JSON body describing the issue.
3. Dependencies:
  - The `pydub` library is required for the audio batch processing endpoint. Ensure this is installed via `pip install pydub`.


## Prerequisites

- Make sure the user has valid Odoo credentials (username, password, and database name).
- The APIs require proper authentication, and the session will be initialized using `request.session.authenticate`.

---

## get

```http
GET /api/<model_name>/get/<object_id>
```

**Parameters:**

- `model_name` (string): The technical name of the model (e.g., `res.partner`, `audio.file`).
- `object_id` (integer): The ID of the record to retrieve.
- **Query String Parameters:**
  - `db` (string): The Odoo database name.
  - `username` (string): The username of an authorized Odoo user.
  - `password` (string): The user's password.

**Response:**
- **200 OK**: Returns the record's data in JSON format. For related fields:
  - `many2many`: Returns an array of related record IDs.
  - `many2one`: Returns the related record's ID or `null` if empty.
  - `datetime`/`date`: ISO 8601 formatted string.
- **404 Not Found**: The specified record does not exist.

**Example Request:**
```http
GET /api/res.partner/get/1?db=my_database&username=admin&password=admin_password
```

**Example Response:**

```json
{
    "respond": {
        "name": "Sample Partner",
        "email": "sample@example.com",
        "tag_ids": [1, 2, 3],
        "create_date": "2025-04-13T10:00:00"
    }
}
```

## set

```http
GET /api/<model_name>/set/<object_id>
```

**Parameters:**
- `model_name` (string): The technical name of the model (e.g., `res.partner`, `audio.file`).
- `object_id` (integer): The ID of the record to update.
- **Query String Parameters:**
  - `db` (string): The Odoo database name.
  - `username` (string): The username of an authorized Odoo user.
  - `password` (string): The user's password.
  - Additional parameters: Key-value pairs corresponding to the field names and their new values.

**Special Field Handling:**
- `many2one`: Pass the ID of the related record.
- `many2many`: Pass a comma-separated list of related record IDs (e.g., `1,2,3`).
- `datetime/date`: ISO 8601 formatted string (e.g., 2025-04-13T10:00:00).

**Response:**
- 200 OK: Returns fields that were successfully updated and skipped.
- 404 Not Found: The specified record does not exist.

**Example Request:**
```http
GET /api/res.partner/set/1?db=my_database&username=admin&password=admin_password&email=new_email@example.com&tag_ids=1,2
```

**Example Response:**

```json
{
    "updates": ["email", "tag_ids"],
    "passing": ["not updates fields"]
}
```

## audio file batch create

Batch create audio.file records by reading audio properties from files in the specified directory.

```http
GET /audio_file/batch
```

**Query String Parameters:**
- `db` (string): The Odoo database name.
- `username` (string): The username of an authorized Odoo user.
- `password` (string): The user's password.
- `path` (string): The file system path pattern (e.g., `/path/to/files/*.wav`).
- `tag_ids` (string): Comma-separated list of tag IDs to assign to the audio files. (e.g., `1,2,3`).

**Description:**

- The API uses pydub to process audio files.
- Each audio file generates a new audio.file record with metadata:
  - `path`: File path.
  - `rates`: Frame rate (audio sample rate).
  - `channels`: Number of channels.
  - `length`: Total number of audio samples.

**Response:**

- 200 OK: If all files were successfully processed and records were created.
- 500 Internal Server Error: If an error occurs during processing.

**Example Request:**
```http
GET /audio_file/batch?db=my_database&username=admin&password=admin_password&path=/audio/files/*.wav&tag_ids=1,2,3
```

**Example Response:**

```json
{
    "message": "done"
}
```
