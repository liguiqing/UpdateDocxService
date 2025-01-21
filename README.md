# UpdateDocxService

This project implements an HTTP RESTful API service for updating the table of contents in DOCX files. It is designed to handle multiple file uploads asynchronously, ensuring efficient processing.

## Project Structure

```
UpdateDocxService
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── services
│   │   ├── __init__.py
│   │   └── toc_updater.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── docx_routes.py
│   └── utils
│       ├── __init__.py
│       └── file_handler.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Features

- Upload DOCX files to update their table of contents.
- Asynchronous processing to handle up to 30 files per minute.
- Temporary files are deleted after processing.
- Returns the updated DOCX file to the client.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd UpdateDocxService
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python src/main.py
   ```

## API Endpoints

- **POST /upload**: Upload a DOCX file to update its table of contents.
  - Request: Multipart form data with the DOCX file.
  - Response: Updated DOCX file.

- **GET /status/{uuid}**: Check the status of the DOCX processing.
  - Request: UUID of the processing request.
  - Response: Status of the processing.

## Usage Example

To upload a DOCX file, use a tool like `curl`:

```
curl -X POST -F "file=@path/to/your/file.docx" http://localhost:8000/upload
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.