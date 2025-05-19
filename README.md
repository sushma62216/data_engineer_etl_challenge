#  Data Engineer Technical Challenge: ETL Pipeline (PostgreSQL + SQL Server)

This project implements an end-to-end ETL (Extract, Transform, Load) data pipeline using Python, PostgreSQL (for staging), and Microsoft SQL Server (for the final data warehouse). The application is containerized with Docker Compose for easy orchestration.

---

## 🛠️ Setup Instructions

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- Basic understanding of Python and SQL.

# Step-by-Step

1. **Clone the Repository**
   ```bash
   git clone <your_repo_url>
   cd data_engineer_challenge
2. **Start the Environment**
   ```bash
   docker-compose up -d --build 
   ```
   This will:
   - Start PostgreSQL (staging)

    - Start SQL Server (warehouse)

3. Install Python Dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Run the ETL Pipeline
   ``` bash
   python main.py
   ```
# Pipeline and Architecture
   - Extract: Fetches users and posts 

   - Transform: Joins posts with their respective users and selects required fields.

   - Load: 
        - Raw data is staged in PostgreSQL.

        - Transformed data is loaded into SQL Server.
# Database Schemas

### PostgreSQL (Staging)
- **staging_users**: `id`, `name`, `username`, `email`
- **staging_posts**: `id`, `user_id`, `title`, `body`

### SQL Server (Warehouse)
- **user_posts**: `PostID`, `PostTitle`, `PostBody`, `UserName`, `UserEmail`


# Design Decisions

### Idempotency
- CREATE TABLE IF NOT EXISTS ensures table creation is safe to rerun.

- Staging tables are truncated before each run to prevent duplicates.

### Modularity
- Modular structure with etl/extract.py, etl/load.py, and etl/transform.py.

- Clear separation of concerns for extraction, loading, and transformation.

### Containerization
- Docker Compose orchestrates PostgreSQL, SQL Server.
 
### Data Validation
- Posts are only loaded if their corresponding user ID exists in the staging_users table.

# Example
```bash
# If running on host system
python main.py

# If running inside the conatiner
docker exec -it etl_app python main.py
```