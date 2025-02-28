# RAG LLM FastAPI Demo

This repository demonstrates a Retrieval-Augmented Generation (RAG) approach using FastAPI, FAISS for vector search, and OpenAI's language model. The app retrieves context from a dataset of Amazon reviews and uses an LLM to answer queries based on the retrieved context.

## Features

- **FastAPI-based REST API:** Provides endpoints for querying and user authentication.
- **Vector Database:** Uses FAISS and Sentence Transformers to index and retrieve relevant context from a CSV of Amazon reviews.
- **LLM Integration:** Leverages OpenAI’s API to generate answers using retrieved context.
- **User Authentication:** Implements JWT-based authentication with endpoints for login, registration, and user management.
- **Automatic Admin Creation:** Creates a default admin user on startup if one doesn’t exist.


## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/EnesGokceDS/FastAPI-Portfolio-Demo-App.git
   cd your-repository
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   Run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. **Run the Application:**
   ```bash
   uvicorn main:app --reload
   ```
   The server will start at [http://0.0.0.0:8000](http://0.0.0.0:8000).

2. **API Documentation:**
   Visit [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) to interact with the API using the automatically generated Swagger UI.

3. **Frontend:**
   The root URL (`/`) serves a basic HTML interface from the `templates` directory.

## API Endpoints

- **Query Endpoint:**  
  `GET /api/query?q=your_query`  
  - Retrieves context from the vector database.
  - Generates an answer using the LLM.
  - Logs the query and response.  
  *Requires authentication.*

- **Authentication Endpoints:**
  - `POST /auth/token`: Obtain a JWT token by providing your username and password.
  - `POST /auth/register`: Public endpoint to register a new user.
  - `POST /auth/users`: Create a new user (admin-only).

- **Set API Key:**  
  `POST /set_api_key`  
  - Dynamically sets the OpenAI API key.

## Authentication

The application uses JWT tokens for securing endpoints.  
**Default Admin User:**  
- **Username:** admin  
- **Password:** admin123  

Use the `/auth/token` endpoint to get your access token, then include it in your requests with the Bearer schema.

## Configuration

- **Database:**  
  The app uses SQLite by default (`app.db`). To change the database, modify the connection string in `services/database.py`.

- **Vector Database:**  
  The FAISS index is built from the `data/amazon_50k_reviews.csv` file. If the index file (`faiss_index.index`) exists, it will be loaded; otherwise, a new index is created.

- **OpenAI API Key:**  
  Provided via environment variables, a `.env` file, or Streamlit secrets (if using Streamlit).

## License

Distributed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Contact

Your Name – [enesgokce@gmail.com](enesgokce@gmail.com)  
Project Link: [https://github.com/EnesGokceDS/FastAPI-Portfolio-Demo-App](https://github.com/EnesGokceDS/FastAPI-Portfolio-Demo-App)

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI](https://openai.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
