# RAG-Based-LLM-Chatbot

This web app queries a database of League of Legends champion lore content and produces answers with the help of an LLM (Large Language Model). It leverages the Retrieval-Augmented Generation (RAG) approach to provide contextually relevant and informative responses.

## Overview

This project demonstrates how to build a RAG-based LLM application for querying a specific knowledge domain. It combines a vector database, an LLM, and a user-friendly web interface to provide an interactive experience.

![Overview](./imgs/Landing%20Page.png)

## Features

-   **RAG-Based Question Answering:** Uses a vector database and LLM to answer questions about League of Legends champion lore.
-   **Web Interface:** Provides a user-friendly interface for interacting with the chatbot.
-   **Customizable:** Easily adaptable to other knowledge domains by changing the data source.

## Prerequisites

Before you begin, ensure you have met the following requirements:

-   Python 3.7+
-   Pip package manager
-   A suitable LLM API key (e.g., OpenAI, Cohere)

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/Reno0213/RAG-Based-LLM-Chatbot.git
    cd RAG-Based-LLM-Chatbot
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate.bat  # On Windows
    ```

3.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Set up your environment variables:

    -   Create a `.env` file in the root directory.
    -   Add your LLM API key:

        ```
        OPENAI_API_KEY=YOUR_OPENAI_API_KEY
        ```

## Usage

1.  Prepare the data:

    -   Place your League of Legends champion lore data in the `data/` directory.
    -   Ensure the data is in a suitable format (e.g., text files, JSON).

2.  Run the application:

    ```bash
    python app/rag.py
    ```

3.  Access the web interface:

    -   Open your web browser and navigate to the address provided by the application (typically `http://localhost:5000`).

4.  Start chatting:

    -   Enter your questions in the chat interface and receive answers based on the champion lore data.

## Project Structure

The project structure is organized as follows:

```
RAG-Based-LLM-Chatbot/
├── app/                # Contains the main application logic
│   └── rag.py          # RAG implementation and web app
├── data/               # Data source for champion lore
├── frontend/           # Frontend files (HTML, CSS, JavaScript)
├── img/                # Images for the README and web app
├── setup/              # Setup scripts and configuration files
├── README.md           # This README file
└── requirements.txt    # Python dependencies
```

## Contributing

Contributions are welcome! Here's how you can contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and ensure they are well-documented.
4.  Submit a pull request.

## License

This project does not have a license file. Please add a license file to specify how the project can be used.

## Acknowledgements

-   [Anyscale's guide for production](https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1#chunk-data) - Inspiration for the RAG implementation.

## Try the Web Application

[Try the final web application here]()

Still in production.