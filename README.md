# business-license-api
API for querying business license information using FastAPI

## Database Setup & Seeding

Before running the application, you need to create the database tables and seed initial data.

### 1. Install dependencies

```sh
pip install -r requirements.txt
```

### 2. Create the database tables

```sh
python -m app.create_db
```

### 3. Seed the database with initial data

```sh
python -m app.seed
```

### 4. Run the application

```sh
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

---

**Note:**  
If you are using Docker, these steps are handled automatically in the Docker build process.