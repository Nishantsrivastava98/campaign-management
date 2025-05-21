# Colca Assignment: Campaign Management & Lead Processing

## Overview
This project is a FastAPI application for managing marketing campaigns, uploading and processing leads via CSV, and simulating email scheduling. It uses PostgreSQL for data storage and can be containerized with Docker Compose. MinIO is optionally supported for local S3 mocking.

## Features
- Pre-seeded Client model (no CRUD)
- Campaign management APIs (create/list)
- CSV upload API (to S3/MinIO/local)
- Scheduled job for CSV processing and lead insertion
- UploadLog for tracking uploads
- List leads by campaign
- Email scheduling logic (simulated, not real sending)
- Containerized with Docker, Docker Compose, PostgreSQL, and optional MinIO

## Quick Start
1. Clone the repo and navigate to the project directory.
2. Build and start services:
   ```sh
   docker-compose up --build
   ```
3. The FastAPI app will be available at `http://localhost:8000`.
4. API docs: `http://localhost:8000/docs`

## Environment Variables
- Configure DB and S3/MinIO credentials in `.env` (to be created).

## Development
- Python 3.10+
- FastAPI
- SQLAlchemy
- APScheduler
- Docker, Docker Compose
- PostgreSQL
- (Optional) MinIO for S3 mocking

## License
MIT
