# Book Exchange Platform : Book Barter

## Overview

This project is a Book Exchange Platform that allows users to securely register, log in, and manage their accounts. Users can list books they want to exchange or lend, and search for books based on various criteria.

## Features

1. **User Authentication:**
   - User registration with email verification.
   - Secure password storage using hashing and salting.
   - JWT-based authentication for login.
   - Password recovery via email verification.
   - User logout to invalidate JWT tokens.

2. **Book Listing:**
   - Add, edit, and delete book listings.
   - Each book listing includes details such as title, author, genre, condition, availability status, and unique ID associated with the user.

3. **Book Search:**
   - Search for books based on title, author, genre, and location.
   - Filter search results by availability status, genre, and location.
   - View detailed information about a book from the search results.
   - Paginated search results to handle large datasets.

## Project Structure

```
project_root/
├── auth_app/
│   ├── app.py
│   ├── models.py
│   ├── resources/
│   │   ├── user.py
│   ├── serializers.py
│   └── ...
├── books_app/
│   ├── app.py
│   ├── models.py
│   ├── resources/
│   │   ├── book.py
│   ├── serializers.py
│   └── ...
├── common/
│   ├── config.py
│   ├── mq_utils.py
│   └── ...
└── ...
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:MohanKantamsetti/FSADAssignment.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd FSADAssignment
   ```

3. **Create a virtual environment:**

   ```bash
   python -m venv flask_env
   ```

4. **Activate the virtual environment:**

   - On Windows:
     ```bash
     flask_env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source flask_env/bin/activate
     ```

5. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Applications
### Prerequisites

1. **MongoDB:**
   - Ensure that MongoDB is installed and running locally on port 27017. This is the default port for MongoDB, and it's where the application will connect to store and retrieve data.
   - You can download and install MongoDB from the [official MongoDB website](https://www.mongodb.com/try/download/community).
   - Start the MongoDB server using the command:
     ```bash
     mongod
     ```
2. **Python and Flask:**
   - Make sure Python is installed on your machine. You can download it from the [official Python website](https://www.python.org/).
   - Install Flask and other dependencies using pip:
     ```bash
     pip install -r requirements.txt
     ```

### Application Configuration

- **Unique Users:**
  - The application ensures that each user has a unique email address. This is enforced by the database schema, which sets the email field to be unique.
  - If you are manually managing the MongoDB collections, ensure that the `users` collection has a unique index on the `email` field. You can create this index using the MongoDB shell or a GUI tool like MongoDB Compass:
    ```javascript
    db.users.createIndex({ email: 1 }, { unique: true });
    ```

### auth_app

1. **Navigate to `auth_app` directory:**

   ```bash
   cd auth_app
   ```

2. **Run the Flask application:**

   ```bash
   python app.py
   ```

### books_app

1. **Navigate to `books_app` directory:**

   ```bash
   cd books_app
   ```

2. **Run the Flask application:**

   ```bash
   python app.py
   ```

## API Endpoints

### User Authentication (auth_app)

- **Register:**
  ```
  POST /api/user/register/
  ```

- **Login:**
  ```
  POST /api/user/login/
  ```

- **Logout:**
  ```
  POST /api/user/logout/
  ```

- **Protected Route Example:**
  ```
  GET /api/user/protected/
  ```

### Book Listing and Search (books_app)

- **Add Book:**
  ```
  POST /books
  ```

- **Get All Books by User:**
  ```
  GET /user_books?user_id=<user_id>&page=<page>&size=<size>
  ```

- **Search Books:**
  ```
  GET /books/search?query=<search_query>&page=<page>&size=<size>
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
