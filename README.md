# Overview
Little backend app written with python3.10 and fastapi to extract date data from PDF files.

## Running the app
Just build and run `Dockerfile` at the top of the repository with port binding.
Note: Dockerfile exposes 8080 port.

### API
App has the following routes:

| URL                        |                               Description                                |
|----------------------------|:------------------------------------------------------------------------:|
| /_healthz                  | Health check route. Mark that application has been successfully started. |
| /files/{file_id}           |                         Download PDF file by id.                         |
| /files/{file_id}/extracted |             Get all extracted data from PDF file by file id.             |
| /uploadfile/               |                  Upload PDF file to extract date data.                   |


### Ideas to improve
(Besides implementing frontend)

* Improve PDF text scanner to group text into logical sentences for easier context extraction
* Test coverage of PDFReader
* Use repository pattern instead of accessing data from SA models
* More logging
