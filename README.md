# Xplor Translation Services

This project provides translation services for the Xplor App. It is built using FastAPI and includes features such as translation and health check endpoints.

## Getting Started

1. Clone the repository:

2. Navigate to the project directory:
```sh
cd xplor-ai-services
```

3. Activate the virtual environment:
```sh
source myvenv/Scripts/activate
```
4. Install the required Python packages:
```sh
pip install -r requirements.txt
```
5. Run the application:
```sh
uvicorn src.app:app --reload
```

## Project Structure

The main application is in the [src/app.py]() file. The translation functionality is implemented in the [src/py/translation.py]() file. Unit tests are located in the [src/tests]() directory.

## API Endpoints

- `/healthcheck`: Verifies the status of the application.
- `/datecheck`: Verifies the status of the application.
- `/translate`: Translates the provided text from the source language to the target language.

## Testing

To run the tests, use the following command:
```sh
pytest -p no:warnings
```

## Tech Stack

[FastAPI](https://fastapi.tiangolo.com/) - The web framework used

[Python](https://www.python.org/) - Programming Language

[ArgosTranslate](https://github.com/argosopentech/argos-translate) - Open Source Translation Library

[PyTest](https://docs.pytest.org/en/8.0.x/contents.html)- Testing framework for Python that allows you to write simple and scalable tests.

## Authors

[WITSLAB](https://www.thewitslab.com/)


## License

Pending Discussion
