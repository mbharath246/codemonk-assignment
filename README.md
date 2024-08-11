# Paragraph Tokenization and Storage API

## Introduction
This project implements a RESTful API for indexing paragraphs and allowing word-based searches. The API is built with Django REST Framework and PostgreSQL, using Docker for containerization. The API allows users to authenticate, input paragraphs of text, and retrieve paragraphs that contain specific words.

## Features

- **User Authentication**: Secure login for users to access API functionalities.
- **Paragraph Storage**: Stores paragraphs of text with unique identifiers in a PostgreSQL database.
- **Word Indexing**: Tokenizes and indexes words against their respective paragraphs.
- **Search Functionality**: Retrieves the top 10 paragraphs containing a specific word.

## Prerequisites

- Python 3.8+
- Django 5.0.7+
- Django-Rest_framework 3.15.2
- PostgreSQL
- Docker

### Setting Up Locally
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mbharath246/codemonk-assignment.git
   cd codemonk-assignment
   ```
2. **Create and activate a virtual environment:**
    ```bash
    python -m venv env
    env\Scripts\activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    Optional: ( install docker : https://docs.docker.com/engine/install/ubuntu/)
    ```
4. **Set up for the project:**
    ```bash
    for windows setup database settings according to your postgres database. else won't run use docker.
    Windows:
    python manage.py makemigrations
    python manage.py migrate
    
   `create superuser`
    python manage.py createsuperuser
    enter basic details and submit
    
    python manage.py runserver 
    
    Docker : docker compose up
    create superuser in docker
    steps: 1. docker ps (to see containers)
           2. docker exec -it <containerid of django> /bin/bash
           3. python manage.py createsuperuser
           4. exit
    ```
5. **Run the development server:**

    ```bash
    http://127.0.0.1:8000/swagger
    ```
6. **Additional Steps**
    - Create User
    - User Login to get Token
    - Authorize Token
    - Now you can use all apis.
  
# Images

## all apis

![image](https://github.com/user-attachments/assets/82c94926-cd66-4fd0-b968-89f1cb10cc91)


1. **Login**
   ![image](https://github.com/user-attachments/assets/bde39f2a-1b84-49d2-9ed5-2e72e053749b)


2. **Authorize**
   
   ![image](https://github.com/user-attachments/assets/2f8177ed-1c10-45c2-bb1a-b41b5300fa5b)

3.  **Create paragraphs to create paragraphs the format to separate paras with two \n\n example format:**
   ```
  {
  "text": "The `register` API allows new ushpplication, such as adding or searching paragraphs. \n\n The `add-paragraphs` API The `search-paragraph`on both powerful and user-friendly."
  }
```
  ![image](https://github.com/user-attachments/assets/94179103-a64c-41ce-a0d1-78ffc0a4ede3)
  ![image](https://github.com/user-attachments/assets/2966e9da-1401-4c7e-aebf-03ea970f676f)

4. **Paragraphs Data**
   
   ![image](https://github.com/user-attachments/assets/05ff8dbb-8657-4121-85db-f277a82caad0)

5. **search api**

   ![image](https://github.com/user-attachments/assets/a5f63819-c3e5-44be-98b2-01a0d6980244)

6. **indexed words**

   ![image](https://github.com/user-attachments/assets/3db664e6-622f-4dc9-99d1-c798694ad45d)
