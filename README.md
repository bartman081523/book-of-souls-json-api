# Book of Souls JSON API 📖⚡

This API provides access to Equidistant Letter Sequences (ELS) calculations based on the Torah (Hebrew Bible).  It uses Gematria to determine the jump width for the ELS search, based on a given date and a name or topic.

## API Endpoint

**Base URL:** `https://book-of-souls-json-api.onrender.com`

**Endpoint:** `/els_search`

**Method:** `POST`

**Request Body:**

```json
{
  "date": "2024-08-06",
  "name_or_topic": "Hans Albert Einstein"
}
```

**Example Request:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"date": "2024-08-06", "name_or_topic": "Hans Albert Einstein"}' https://book-of-souls-json-api.onrender.com/els_search 
```

**Response:**

The API returns a JSON object containing the configuration used for the ELS search and the resulting sequences found:

```json
{
    "Configuration": {
        "Start Book": 1,
        "End Book": 39,
        "Step": 5174,
        "Rounds": "1,-1",
        "Length": 0,
        "Target Language": "english",
        "Strip Spaces": true,
        "Strip Text in Braces": true,
        "Strip Diacritics": true,
        "Search Phrase": "sixth August two thousand twenty-four Hans Albert Einstein"
    },
    "Results": [
        {
            "Result Number": 1,
            "book": 1,
            "title": "Genesis",
            "els_result_text": "תחיןעימדהיורהולרםדתוילאאהותאשא",
            "els_result_gematria": 3469,
            "translated_text": "You'll get up and go"
        },,
        // ... more results ...
    ]
}
```

## OpenAPI Specification

The API documentation is available in OpenAPI format in the `openapi.yaml` file. You can use tools like [Swagger UI](https://swagger.io/tools/swagger-ui/) or [Redoc](https://redocly.com/redoc/) to visualize and interact with the API documentation.

## Project Structure

- `app.py`: Main Flask application file.
- `utils.py`: Utility functions, including date-to-words conversion.
- `requirements.txt`: Project dependencies.
- `Procfile`: Instructions for starting the application (if using Gunicorn).
- `Dockerfile`: Docker configuration.

## Deployment

This API is currently deployed on [Render](https://render.com). You can find the live API at [https://book-of-souls-json-api.onrender.com](https://book-of-souls-json-api.onrender.com).

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or pull request if you have any suggestions or improvements.

## Acknowledgments

This project utilizes the following libraries:

- [Flask](https://flask.palletsprojects.com/)
- [Gunicorn](https://gunicorn.org/)