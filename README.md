# Translator API

This repository contains a simple Flask-based API for text translation using TensorFlow and other libraries.

## Overview

This project provides an API endpoint that allows you to translate text from one language to another. It utilizes a pre-trained TensorFlow model for translation.

## Dependencies

* Python (version less than 12)
* TensorFlow
* Flask
* Pandas
* NumPy
* regex
* sentencepiece
* protobuf

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/manojsingh00963/Translator.git](https://www.google.com/search?q=https://github.com/manojsingh00963/Translator.git)
    cd Translator
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the dependencies:**

    ```bash
    pip install tensorflow flask pandas numpy regex sentencepiece protobuf
    ```

## Usage

1.  **Run the Flask application:**

    ```bash
    python app.py
    ```

    The API will start running on `http://127.0.0.1:5000/`.

2.  **Make a POST request to the `/translate` endpoint:**

    You can use tools like `curl` or Postman to send a POST request.

    **Example using `curl`:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"text": "Hello, how are you?", "target_lang": "es"}' [http://127.0.0.1:5000/translate](https://www.google.com/search?q=http://127.0.0.1:5000/translate)
    ```

    **Request Body:**

    ```json
    {
      "text": "Text to translate",
      "target_lang": "Target language code (e.g., 'es' for Spanish, 'fr' for French)"
    }
    ```

    **Response:**

    ```json
    {
      "translation": "Translated text"
    }
    ```

## Notes

* Ensure you have a stable internet connection for the initial download of the TensorFlow model.
* The model used in this example may have limitations in translation accuracy.
* The code is designed to use a pre-trained translation model. If you would like to use a different model, you will need to modify the code.
* The Language code must be ISO 639-1 two letter code.
* The python version should be less then 12.

## File Structure
