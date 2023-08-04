# My Project README

## Introduction

dpdzero assignment

## 1. Choices of Framework

This project is built using the Django web framework. Django is a high-level Python web framework known for its simplicity, robustness, and scalability. It allows us to build web applications efficiently while following best practices and maintaining code quality.

## 2. DB Schema

The project uses a PostgreSQL database to store and manage data. The database schema includes two main entities:

**CustomUser**

- Fields:
  - ID (Primary Key)
  - Username
  - Email
  - Password (hashed)
  - Full_name
  - Age
  - Gender

**Data**

- Fields:
  - ID (Primary Key)
  - Key(unique)
  - Value
 
The CustomUser entity represents users of the application, while the Data entity stores key and value.

## 3. Instructions to Run the Code

To run this project, make sure you have Docker and Docker Compose installed on your system. Follow the steps below:

1. Clone the repository to your local machine:

   ```bash
   git clone <repository_url>
   cd <project_directory>

2. Create a .env file in the project root directory

   ```bash
   cp .env.example .env

3. Build and run the project using Docker Compose

    ```bash
    docker compose up -d --build

    This will build the necessary containers and start the project in detached mode. The application will be accessible at http://localhost:8000

4. Access the application:

    Open your web browser and go to http://localhost:8000 to access the Django application

5. Stop the project:

    ```bash
    docker compose down