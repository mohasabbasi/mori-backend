# Mori Product Search Backend

This is the backend application for the Product Search Engine. It uses FastAPI to provide endpoints for searching products and managing the database.

## Features

- Text-based product search using CLIP model
- Integration with Qdrant for vector storage
- Filter results by category and shop

## Technologies Used

- Python
- FastAPI
- Qdrant
- CLIP model by OpenAI
- Docker

## Setup and Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mohasabbasi/mori-backend.git
    cd mori-backend
    ```

2. Build and start the Docker containers.

3. The API will be available at `http://0.0.0.0:8000`.

## API Endpoints

### Search Products

- **URL:** `/search/`
- **Method:** `POST`
- **Payload:**
  ```json
  {
      "text": "search term",
      "category_name": "comma,separated,categories",
      "shop_name": "comma,separated,shops"
  }
