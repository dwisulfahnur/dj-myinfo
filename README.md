# DJ MyInfo App


## Running the Django App using Docker Compose (recommended)

### Prerequisites

- Docker and Docker Compose installed

### Setup Steps

1. **Copy the environment file**

   ```sh
   cp .env.example .env
   ```

   Then, edit `.env` based on your environment settings.

   **Configure `.env` file:**
   - Open `.env` and set the required values before running the application.
   - Ensure all necessary variables are properly configured before proceeding.

2. **Build and start the services (database, cache, and web app)**

   ```sh
   docker-compose -f docker-compose.db.yml -f docker-compose.yml up --build -d
   ```

3. **Run database migrations** inside the `web` container:

   ```sh
   docker-compose -f docker-compose.db.yml -f docker-compose.yml exec web python manage.py migrate
   ```

4. **Access the app at** `http://localhost:3001/`

5. **Run tests inside the `web` container**

   ```sh
   docker-compose -f docker-compose.db.yml -f docker-compose.yml exec web python -m pytest
   ```

6. **To stop the containers**

   ```sh
   docker-compose down
   ```

---

## Running the App using Python Virtual Environment

### Prerequisites

- Python 3.11 installed
- Docker installed (for running PostgreSQL and Redis)

### Setup Steps

1. **Copy the environment file**

   ```sh
   cp .env.example .env
   ```

   Then, edit `.env` based on your environment settings.

   **Configure `.env` file:**
   - Open `.env` and set the required values before running the application.
   - Ensure all necessary variables are properly configured before proceeding.

2. **Start the database and cache services**

   ```sh
   docker-compose -f docker-compose.db.yml up -d
   ```

3. **Create and activate a virtual environment**

   ```sh
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

4. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

5. **Run database migrations**

   ```sh
   python manage.py migrate
   ```

6. **Run the server**

   ```sh
   python manage.py runserver
   ```

7. Access the app at `http://127.0.0.1:3001/`

8. **Run tests**

   ```sh
   python -m pytest
   ```
