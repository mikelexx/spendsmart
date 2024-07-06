**SPENDSMART**

![intro-meme](/screenshots/intro-meme.png)

Lately, I've realized that I have a tendency to be a bit of a spendthrift. To better manage my finances, I decided to experiment by tracking my daily expenses. This way, I could request pocket money from my parents that would be sufficient to cover my monthly expenses. I needed a tool that would allow me to instantly record any purchase I made on the spot before I forgot about it. Additionally, I wanted to be transparent with my parents and accountable for every single coin I spent.

I envisioned a solution where I could divide the money I received into essential categories like food and school expenses, and allocate the remaining funds to entertainment. I needed a way to track how much I had left in each category at any given moment, from anywhere. This approach would help me spend my remaining funds wisely and avoid making random calls to my parents for money at unexpected times, especially when they might not have any to spare.

As a result, I developed a web application that enables me to monitor my spending and meet my budgets. This application not only helps me manage my finances better but also fosters accountability and transparency with my parents.


![help-you-meme](/screenshots/help-you.png)


I wrote a detailed blog post about the development of SpendSmart, covering the challenges I faced and the solutions I implemented. You can read it [here](my-blog-url).

 Connect with the authors via the links below:
- Michael Murithi  - [linkedIn profile](https://www.linkedin.com/in/murithimichael254/)

Below is the link to the deployed site
- [https://www.murithimichael.tech/spendsmart](https://www.murithimichael.tech/spendsmart)

---------------------------------
**TECH STACK I USED**

![web-architecture](/screenshots/spendsmart-architecture.png)

**Frontend**

**HTML, CSS, and JavaScript**: For structuring the content, styling the application, and adding interactivity.
**Flatpickr** Library: Chosen for date picking functionality due to its ease of use and integration with JavaScript, enhancing the user experience by providing a visually appealing and user-friendly date picker.

**Backend**

**Python**: Selected for its simplicity and readability, allowing for rapid development and ease of maintenance.

**Flask:** A lightweight web framework  to create the backend of the application. I chose it for its simplicity, flexibility, and fine-grained control over the application's components.

**SQLAlchemy:** An ORM (Object Relational Mapper) that allowed for easy interaction with the database using Python objects, reducing the complexity of writing raw SQL queries and improving code maintainability.

**Database Management**

**MySQL**: Chosen for its robustness, reliability, and widespread use. I prefered it owing to its efficiency in data storage and retrieval, ensuring the application can handle multiple transactions and queries efficiently.

**Deployment**

**Nginx**: Used it as a web server for serving the application, motivated by its reputation for  high performance, stability, and low resource consumption. Nginx is also played a crucial role for handling static files(html, css , jquery and images).

**Gunicorn**: Used as wsgi application server to run the Flask application, providing a robust and scalable way to serve the web application.
**HAProxy**: Employed for load balancing and SSL termination, and reverse proxying, ensuring high availability, reliability, and security of the application. 
--------------------------------------------
**Environment**

This project is interpreted/tested on Ubuntu 14.04 LTS using python3 (version 3.4.3)

**Installation**
---
- clone the repo
```
git clone https://github.com/mikelexx/spendsmart.git
```
Install the required libraries listed below:
- Flask
```
pip install Flask==3.0
```
- Flask-CORS
```
pip install Flask-CORS
```
- flask_login
```
pip install flask_login
```
- SqlAlchemy 
```
pip install SQLAlchemy
```
- Flatpickr
```
npm install flatpickr
```
- pkg-config (for building mysqlclient)
```
sudo apt-get update
sudo apt-get install pkg-config
```
- mysqlclient dev packages
```
sudo apt-get install default-libmysqlclient-dev
```
- mysqlclient
```
pip install mysqlclient
```
if installing mysqlclient fail, you might to install additional dependencies
```
sudo apt-get install build-essential python3-dev
```
***mysql database configuration***
- install mysql
```
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql.service
```
- create mysql database and user
```
CREATE DATABASE spendsmart_db;
CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON spendsmart_db.* TO 'test_user'@'localhost';
FLUSH PRIVILEGES;
```
- set environment variables
```
export SPENDSMART_MYSQL_USER=test_user
export SPENDSMART_MYSQL_PWD=your_password
export SPENDSMART_MYSQL_DB=spendsmart_db
export SPENDSMART_TYPE_STORAGE=db
export SPENDSMART_MYSQL_HOST=localhost
export SPENDSMART_SECRET_KEY=your_secret_key
export SPENDSMART_API_HOST=127.0.0.1
export SPENDSMART_API_PORT=5011
```
--------------------------------------------------------------
**Running application locally**

- ensure you have python3.x installed
```
cd spendsmart
```
while inside root directory `spendsmart`
	- run this to activate the api
```
python3 -m api.v1.app
```
	- activate the client side to serve pages 
```
python3 -m web_dynamic.app
```
**Usage**
---
Interacting with the program using APIs
---
**API Endpoints**
---
- all Api endpoints will return 404 reponse code with this message for resources not found:
```
{
  "error": "Not found"
}
```

**User**
---
**Get Users**
```
GET /api/v1/users
```
Retrieves all users.

**Response:**

200 OK with a list of users in JSON format

- json response format
```
[
{
  "__class__": "string",
  "collections": "list",
  "created_at": "string",
  "email": "string,
  "expenses": "list",
  "id": "string",
  "notifications": "list",
  "updated_at": "string",
  "username": "string"
}
]
```
***example***
```
adminpc@mike:~/spendsmart$ curl -X GET http://127.0.0.1:5011/api/v1/users
[
  {
    "__class__": "User",
    "collections": [],
    "created_at": "2024-07-03T19:55:25.000000",
    "email": "murithimichael254@gmail.com",
    "expenses": [],
    "id": "449ea967-4bf2-4972-9768-17cc96b18f4e",
    "notifications": [],
    "updated_at": "2024-07-03T19:55:25.000000",
    "username": null
  },
  {
    "__class__": "User",
    "collections": [],
    "created_at": "2024-07-05T03:02:30.000000",
    "email": "user@example.com",
    "expenses": [],
    "id": "ee95989a-20a1-41d9-bb18-131c649b91cc",
    "notifications": [
      {
        "__class__": "Notification",
        "collection_id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
        "created_at": "2024-07-05T14:07:04.000000",
        "id": "1d408af9-562b-4d8e-901a-1531ea0b127a",
        "is_read": false,
        "message": "you have exceeded the set limit of Miscellaneous",
        "notification_type": "alert",
        "updated_at": "2024-07-05T14:07:04.000000",
        "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
      }
    ],
    "updated_at": "2024-07-05T03:02:30.000000",
    "username": "newuser"
  }
]
```
**Create User**
```
POST /api/v1/users
```
Creates a new user.

**Parameters:**

JSON payload:
```
{
  "email": "string",
  "password": "string",
  "username": "string" (optional)
}
```
**Response:**

201 Created with the newly created user details
- json response payload
```
{
  "__class__": "string",
  "collections": "list",
  "created_at": "string",
  "email": "string,
  "expenses": "list",
  "id": "string",
  "notifications": "list",
  "updated_at": "string",
  "username": "string"
}

```
***example***
```
curl -X POST http://localhost:5011/api/v1/users \
-H "Content-Type: application/json" \
-d '{
  "email": "user@example.com",
  "password": "strongpassword",
  "username": "newuser"
}'
```
response json payload:
```
{
  "__class__": "User",
  "collections": [],
  "created_at": "2024-07-05T02:43:55.000000",
  "email": "user@example.com",
  "expenses": [],
  "id": "c4c05256-2dbb-405f-82f2-00d8983ca165",
  "notifications": [],
  "updated_at": "2024-07-05T02:43:55.000000",
  "username": "newuser"
}
```
**Delete User**
```
DELETE /api/v1/users/<user_id>
```
Deletes a user with a specific ID.

**Parameters:**

`user_id` (string): ID of the user
**Response:**

204 No Content if the user is successfully deleted
response json payload:
```
{
	"success": True
}
```
***example***
```
curl -X DELETE http://localhost:5011/api/v1/users/c4c05256-2dbb-405f-82f2-00d8983ca165
```
- if i now try to get the list of users present, user with id `c4c05256-2dbb-405f-82f2-00d8983ca165`  will not be among them:
***example***
- before delete user api call
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/users
[
  {
    "__class__": "User",
    "collections": [],
    "created_at": "2024-07-03T19:55:25.000000",
    "email": "murithimichael254@gmail.com",
    "expenses": [],
    "id": "449ea967-4bf2-4972-9768-17cc96b18f4e",
    "notifications": [],
    "updated_at": "2024-07-03T19:55:25.000000",
    "username": null
  },
  {
    "__class__": "User",
    "collections": [],
    "created_at": "2024-07-05T02:43:55.000000",
    "email": "user@example.com",
    "expenses": [],
    "id": "c4c05256-2dbb-405f-82f2-00d8983ca165",
    "notifications": [],
    "updated_at": "2024-07-05T02:43:55.000000",
    "username": "newuser"
  }
]
```
- calling delete user api
```
adminpc@mike:~/spendsmart$ curl -X DELETE http://localhost:5011/api/v1/users/c4c05256-2dbb-405f-82f2-00d8983ca165
{
  "success": true
}
```
- after delete user api success
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/users
[
  {
    "__class__": "User",
    "collections": [],
    "created_at": "2024-07-03T19:55:25.000000",
    "email": "murithimichael254@gmail.com",
    "expenses": [],
    "id": "449ea967-4bf2-4972-9768-17cc96b18f4e",
    "notifications": [],
    "updated_at": "2024-07-03T19:55:25.000000",
    "username": null
  }
]
adminpc@mike:~/spendsmart$
```
**Collections [budgets whose expenses are to be monitored]**
---
**Create Collection**
```
POST /api/v1/collections
```
Creates a new collection.

**Parameters:**

JSON payload:
```
{
  "name": "string",
  "start_date": "string",
  "end_date": "string",
  "limit": "number",
  "user_id": "string",
  "description": "string" (optional),
}
```
Response:

201 Created with the newly created collection details
response json format
```
{
  "__class__": "string",
  "amount_spent": "float",
  "created_at": "string",
  "description": "string",
  "end_date": "string",
  "expenses": "list",
  "id": "string",
  "limit": "float",
  "name": "string",
  "start_date": "string",
  "updated_at": "string",
  "user_id": "string"
}
```

***example***
```
adminpc@mike:~/spendsmart$ curl -X POST http://localhost:5011/api/v1/collections -H "Content-Type: application/json" -d '{
  "name": "Entertainment",
  "start_date": "2024-07-01T00:00:00.000000",
  "end_date": "2024-07-31T23:59:59.000000",
  "limit": 1000.00,
  "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
}'
{
  "__class__": "Collection",
  "amount_spent": 0.0,
  "created_at": "2024-07-05T03:04:54.431492",
  "description": null,
  "end_date": "2024-07-31T23:59:59.000000",
  "expenses": [],
  "id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
  "limit": 1000.0,
  "name": "Entertainment",
  "start_date": "2024-07-01T00:00:00.000000",
  "updated_at": "2024-07-05T03:04:54.431636",
  "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
}
```
***Get User Collections***
```
GET /api/v1/<user_id>/collections
```
Retrieves all collections belonging to a specific user.

Parameters:

`user_id` (string): ID of the user
`count` (optional, int): Limit the number of collections returned
**Response:**

200 OK with a list of collections in JSON format
response format
```
[
  {
    "__class__": "string",
    "amount_spent": "float",
    "created_at": "string",
    "description": "string",
    "end_date": "string",
    "expenses": "list",
    "id": "string",
    "limit": "float",
    "name": "string",
    "percentage_spent": "int",
    "remaining_amount": "float",
    "start_date": "string",
    "total_spent": "float",
    "updated_at": "string",
    "user_id": "string"
  }
]
```
***example***
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/collections
[
  {
    "__class__": "Collection",
    "amount_spent": "0.00",
    "created_at": "2024-07-05T03:04:54.000000",
    "description": null,
    "end_date": "2024-07-31T23:59:59.000000",
    "expenses": [],
    "id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
    "limit": "1000.00",
    "name": "Entertainment",
    "percentage_spent": 0,
    "remaining_amount": 1000.0,
    "start_date": "2024-07-01T00:00:00.000000",
    "total_spent": "0.00",
    "updated_at": "2024-07-05T03:04:54.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  }
]
```
**Get User Collection Expenses**
```
GET /api/v1/<user_id>/collections/<collection_id>/expenses
```
Retrieves all expenses associated with a specific collection for a user.

**Parameters:**
`user_id` (string): ID of the user
`collection_id` (string): ID of the collection
**Response:**

200 OK with a list of expenses in JSON format
- json response format
```
[
  {
    "__class__": "string",
    "collection_id": "string",
    "created_at": "float",
    "id": "string",
    "name": "string",
    "price": "float",
    "purchase_date": "string",
    "updated_at": "string",
    "user_id": "string"
  }
]
```
***example***
- suppose i post some expenses under collection ID `c8384cd4-f32b-4f36-91fb-d3aecff9899c` and user ID `ee95989a-20a1-41d9-bb18-131c649b91cc`
```
adminpc@mike:~/spendsmart$ curl -X POST http://localhost:5011/api/v1/expenses -H "Content-Type: application/json" -d '{
  "name": "Movie Night",
  "purchase_date": "2024-07-02T10:00:00.000000",
  "price": 100.00,
  "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc",
  "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c"
}'
adminpc@mike:~/spendsmart$ curl -X POST http://localhost:5011/api/v1/expenses -H "Content-Type: application/json" -d '{
  "name": "Concert Tickets",
  "purchase_date": "2024-07-02T10:00:00.000000",
  "price": 50.00,
  "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc",
  "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c"
}'
```
- to get expenses belonging to collection ID `c8384cd4-f32b-4f36-91fb-d3aecff9899c` of user ID `ee95989a-20a1-41d9-bb18-131c649b91cc`;
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/collections/c8384cd4-f32b-4f36-91fb-d3aecff9899c/expenses
[
  {
    "__class__": "Expense",
    "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
    "created_at": "2024-07-05T03:28:01.000000",
    "id": "469c3cfc-e310-435b-bbcd-a9d7c7742430",
    "name": "Movie Night",
    "price": "100.00",
    "purchase_date": "2024-07-02T10:00:00.000000",
    "updated_at": "2024-07-05T03:28:01.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  },
  {
    "__class__": "Expense",
    "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
    "created_at": "2024-07-05T03:26:40.000000",
    "id": "981acf46-9e26-45bc-932d-8b7b24eaa111",
    "name": "Concert Tickets",
    "price": "50.00",
    "purchase_date": "2024-07-02T10:00:00.000000",
    "updated_at": "2024-07-05T03:26:41.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  }
]
```
**Delete Collection**
```
DELETE /api/v1/<user_id>/collections/<collection_id>
```
Deletes a collection and all associated expenses; 
**Parameters:**
`user_id` (string): ID of the user
`collection_id` (string): ID of the collection
**Response:**
204 No Content if the collection is successfully deleted
***example***
 - collections and their expenses before deleting
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/collections
[
  {
    "__class__": "Collection",
    "amount_spent": "1350.00",
    "created_at": "2024-07-05T04:00:42.000000",
    "description": null,
    "end_date": "2024-07-31T23:59:59.000000",
    "expenses": [
      {
        "__class__": "Expense",
        "collection_id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
        "created_at": "2024-07-05T03:28:01.000000",
        "id": "469c3cfc-e310-435b-bbcd-a9d7c7742430",
        "name": "Movie Night",
        "price": "100.00",
        "purchase_date": "2024-07-02T10:00:00.000000",
        "updated_at": "2024-07-05T04:09:30.000000",
        "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
      },
      {
        "__class__": "Expense",
        "collection_id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
        "created_at": "2024-07-05T13:50:05.000000",
        "id": "aea49d4a-43f2-44d6-837f-1796073614c0",
        "name": "1l of soda",
        "price": "1250.00",
        "purchase_date": "2024-07-02T10:00:00.000000",
        "updated_at": "2024-07-05T13:50:06.000000",
        "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
      }
    ],
    "id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
    "limit": "1000.00",
    "name": "Miscellaneous",
    "percentage_spent": 100,
    "remaining_amount": -350.0,
    "start_date": "2024-07-01T00:00:00.000000",
    "total_spent": "1350.00",
    "updated_at": "2024-07-05T13:50:06.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  }
]
```
- deleting using api:
```
adminpc@mike:~/spendsmart$ curl -X DELETE http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/collections/5b751d95-3618-45bf-aa00-7c881e7861c6
```
- after deleting
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/collections
[]
```

**Expenses**
---

**Create Expense**
```
POST /api/v1/expenses
```
Creates a new expense.

**Parameters:**

JSON payload:
```
{
  "name": "string",
  "purchase_date": "string",
  "price": "number",
  "user_id": "string",
  "collection_id": "string"
}
```
Response:

201 Created with the newly created expense details
json response format
```
{
  "__class__": "string",
  "collection_id": "string",
  "created_at": "string",
  "id": "string",
  "name": "string",
  "price": "float",
  "purchase_date": "string",
  "updated_at": "string",
  "user_id": "string"
}
```
***example***
```
adminpc@mike:~/spendsmart$ curl -X POST http://localhost:5011/api/v1/expenses -H "Content-Type: application/json" -d '{
  "name": "Movie Night",
  "purchase_date": "2024-07-02T10:00:00.000000",
  "price": 100.00,
  "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc",
  "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c"
}'
{
  "__class__": "Expense",
  "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
  "created_at": "2024-07-05T03:28:00.677132",
  "id": "469c3cfc-e310-435b-bbcd-a9d7c7742430",
  "name": "Movie Night",
  "price": 100.0,
  "purchase_date": "2024-07-02T10:00:00.000000",
  "updated_at": "2024-07-05T03:28:00.713115",
  "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
}
```
**Get User Expenses**
```
GET /api/v1/<user_id>/expenses
```
Retrieves all expenses for a specific user.

**Parameters:**

`user_id` (string): ID of the user
`count` (optional, int): Limit the number of expenses returned
**Response:**

200 OK with a list of expenses in JSON format
json response format
```
[
  {
    "__class__": "string",
    "collection_id": "string",
    "created_at": "string",
    "id": "string",
    "name": "string",
    "price": "string",
    "purchase_date": "string",
    "updated_at": "string",
    "user_id": "string"
  }
]

```
***example***
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/collections/c8384cd4-f32b-4f36-91fb-d3aecff9899c/expenses
[
  {
    "__class__": "Expense",
    "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
    "created_at": "2024-07-05T03:28:01.000000",
    "id": "469c3cfc-e310-435b-bbcd-a9d7c7742430",
    "name": "Movie Night",
    "price": "100.00",
    "purchase_date": "2024-07-02T10:00:00.000000",
    "updated_at": "2024-07-05T03:28:01.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  }
]
```
**Update Expense**
```
PUT /api/v1/<user_id>/expenses/<expense_id>
```
Updates the details of an expense.

**Parameters:**

`user_id` (string): ID of the user
`expense_id` (string): ID of the expense
JSON payload with updated fields
Response:

200 OK with the updated expense details
json response format
```
{
  "__class__": "string",
  "collection_id": "string",
  "created_at": "string",
  "id": "string",
  "name": "string",
  "price": "float",
  "purchase_date": "string",
  "updated_at": "string",
  "user_id": "string"
}
```
***example***
-suppose i have budget for `miscellaneuous` with no expenses, and `entertainment` with `Concert Tickets` and `Movie Night` expenses.
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/collections
[
  {
    "__class__": "Collection",
    "amount_spent": "0.00",
    "created_at": "2024-07-05T04:00:42.000000",
    "description": null,
    "end_date": "2024-07-31T23:59:59.000000",
    "expenses": [],
    "id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
    "limit": "1000.00",
    "name": "Miscellaneous",
    "percentage_spent": 0,
    "remaining_amount": 1000.0,
    "start_date": "2024-07-01T00:00:00.000000",
    "total_spent": "0.00",
    "updated_at": "2024-07-05T04:00:42.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  },
  {
    "__class__": "Collection",
    "amount_spent": "150.00",
    "created_at": "2024-07-05T03:04:54.000000",
    "description": null,
    "end_date": "2024-07-31T23:59:59.000000",
    "expenses": [
      {
        "__class__": "Expense",
        "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
        "created_at": "2024-07-05T03:28:01.000000",
        "id": "469c3cfc-e310-435b-bbcd-a9d7c7742430",
        "name": "Movie Night",
        "price": "100.00",
        "purchase_date": "2024-07-02T10:00:00.000000",
        "updated_at": "2024-07-05T03:28:01.000000",
        "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
      },
      {
        "__class__": "Expense",
        "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
        "created_at": "2024-07-05T03:26:40.000000",
        "id": "981acf46-9e26-45bc-932d-8b7b24eaa111",
        "name": "Concert Tickets",
        "price": "50.00",
        "purchase_date": "2024-07-02T10:00:00.000000",
        "updated_at": "2024-07-05T03:26:41.000000",
        "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
      }
    ],
    "id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
    "limit": "1000.00",
    "name": "Entertainment",
    "percentage_spent": 15,
    "remaining_amount": 850.0,
    "start_date": "2024-07-01T00:00:00.000000",
    "total_spent": "150.00",
    "updated_at": "2024-07-05T03:28:00.682548",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  }
]
```
From the response, we can see:
- "Movie Night" expense ID: `469c3cfc-e310-435b-bbcd-a9d7c7742430`
- "Entertainment" collection ID: `c8384cd4-f32b-4f36-91fb-d3aecff9899c`
- "Miscellaneous" collection ID: `5b751d95-3618-45bf-aa00-7c881e7861c6`
- User ID: `ee95989a-20a1-41d9-bb18-131c649b91cc`
- to transfer `Movie night` expense to `miscellaneus` budget:
```
adminpc@mike:~/spendsmart$ curl -X PUT http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/expenses/469c3cfc-e310-435b-bbcd-a9d7c7742430 -H "Content-Type: application/json" -d '{
  "collection_id": "5b751d95-3618-45bf-aa00-7c881e7861c6"
}'
{
  "__class__": "Expense",
  "collection_id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
  "created_at": "2024-07-05T03:28:01.000000",
  "id": "469c3cfc-e310-435b-bbcd-a9d7c7742430",
  "name": "Movie Night",
  "price": "100.00",
  "purchase_date": "2024-07-02T10:00:00.000000",
  "updated_at": "2024-07-05T04:09:29.536515",
  "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
}
```
- from the above oberve that the expense `collection_id` is now pointing to `Miscellaneus`
- Also, now if i list all collections with their expenses, `Movie Night` expense now should belong to `Miscellaneous` collection
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/collections
[
  {
    "__class__": "Collection",
    "amount_spent": "100.00",
    "created_at": "2024-07-05T04:00:42.000000",
    "description": null,
    "end_date": "2024-07-31T23:59:59.000000",
    "expenses": [
      {
        "__class__": "Expense",
        "collection_id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
        "created_at": "2024-07-05T03:28:01.000000",
        "id": "469c3cfc-e310-435b-bbcd-a9d7c7742430",
        "name": "Movie Night",
        "price": "100.00",
        "purchase_date": "2024-07-02T10:00:00.000000",
        "updated_at": "2024-07-05T04:09:30.000000",
        "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
      }
    ],
    "id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
    "limit": "1000.00",
    "name": "Miscellaneous",
    "percentage_spent": 10,
    "remaining_amount": 900.0,
    "start_date": "2024-07-01T00:00:00.000000",
    "total_spent": "100.00",
    "updated_at": "2024-07-05T04:09:30.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  },
  {
    "__class__": "Collection",
    "amount_spent": "50.00",
    "created_at": "2024-07-05T03:04:54.000000",
    "description": null,
    "end_date": "2024-07-31T23:59:59.000000",
    "expenses": [
      {
        "__class__": "Expense",
        "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
        "created_at": "2024-07-05T03:26:40.000000",
        "id": "981acf46-9e26-45bc-932d-8b7b24eaa111",
        "name": "Concert Tickets",
        "price": "50.00",
        "purchase_date": "2024-07-02T10:00:00.000000",
        "updated_at": "2024-07-05T03:26:41.000000",
        "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
      }
    ],
    "id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
    "limit": "1000.00",
    "name": "Entertainment",
    "percentage_spent": 5,
    "remaining_amount": 950.0,
    "start_date": "2024-07-01T00:00:00.000000",
    "total_spent": "50.00",
    "updated_at": "2024-07-05T04:09:29.579566",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  }
]
```
**Delete Expense**
```
DELETE /api/v1/<user_id>/expenses/<expense_id>
```
Deletes an expense belonging to a specific user.

Parameters:

`user_id` (string): ID of the user
`expense_id` (string): ID of the expense
Response:

204 No Content if the expense is successfully deleted

***example***
- existing expenses before deleting an expense
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/expenses
[
  {
    "__class__": "Expense",
    "collection_id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
    "created_at": "2024-07-05T03:28:01.000000",
    "id": "469c3cfc-e310-435b-bbcd-a9d7c7742430",
    "name": "Movie Night",
    "price": "100.00",
    "purchase_date": "2024-07-02T10:00:00.000000",
    "updated_at": "2024-07-05T04:09:30.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  },
  {
    "__class__": "Expense",
    "collection_id": "c8384cd4-f32b-4f36-91fb-d3aecff9899c",
    "created_at": "2024-07-05T03:26:40.000000",
    "id": "981acf46-9e26-45bc-932d-8b7b24eaa111",
    "name": "Concert Tickets",
    "price": "50.00",
    "purchase_date": "2024-07-02T10:00:00.000000",
    "updated_at": "2024-07-05T03:26:41.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  }
]
```
- deleting an expense
```
adminpc@mike:~/spendsmart$ curl -X DELETE http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/expenses/981acf46-9e26-45bc-932d-8b7b24eaa111
```
- after deleting an expense
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/expenses
[
  {
    "__class__": "Expense",
    "collection_id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
    "created_at": "2024-07-05T03:28:01.000000",
    "id": "469c3cfc-e310-435b-bbcd-a9d7c7742430",
    "name": "Movie Night",
    "price": "100.00",
    "purchase_date": "2024-07-02T10:00:00.000000",
    "updated_at": "2024-07-05T04:09:30.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  }
]
```
**Notifications**
---

**Get User Notifications**

```
GET /api/v1/<user_id>/notifications
```
Retrieves notifications for a specific user.

**Parameters**:

`user_id` (string): ID of the user
`sort` (optional, string): Sort order (e.g., "descending")
`read` (optional, boolean): Filter by read status
`type` (optional, string): Filter by notification type (can only be:  "alerts", "achievements" or "warning")
**Response**:

200 OK with a list of notifications in JSON format
- json response format
```
[
  {
    "__class__": "string",
    "collection_id": "string",
    "created_at": "string",
    "id": "string",
    "is_read": "Boolean",
    "message": "string",
    "notification_type": "string",
    "updated_at": "string",
    "user_id": "string"
  }
]
```
***example***
```
adminpc@mike:~/spendsmart$ curl -X GET http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/notifications
[
  {
    "__class__": "Notification",
    "collection_id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
    "created_at": "2024-07-05T13:50:05.000000",
    "id": "b5143289-773b-4473-a16e-202f06f211e6",
    "is_read": false,
    "message": "you have exceeded the set limit of Miscellaneous",
    "notification_type": "alert",
    "updated_at": "2024-07-05T13:50:05.000000",
    "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
  }
]
```
***Update Notification***
```
PUT /api/v1/<user_id>/notifications/<notification_id>
```
Updates the details of a notification.

**Parameters:**

`user_id` (string): ID of the user
`notification_id` (string): ID of the notification
JSON payload with updated fields
**Response:**

200 OK with the updated notification details
-json response format
```
{
  "__class__": "string",
  "collection_id": "string",
  "created_at": "string",
  "id": "string",
  "is_read": "Boolean",
  "message": "string",
  "notification_type": "string",
  "updated_at": "string",
  "user_id": "string"
}
```
***example***
```
adminpc@mike:~/spendsmart$ curl -X PUT http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/notifications/b5143289-773b-4473-a16e-202f06f211e6 -H "Content-Type: application/json" -d '{
  "is_read": true
}'
{
  "__class__": "Notification",
  "collection_id": "5b751d95-3618-45bf-aa00-7c881e7861c6",
  "created_at": "2024-07-05T13:50:05.000000",
  "id": "b5143289-773b-4473-a16e-202f06f211e6",
  "is_read": true,
  "message": "you have exceeded the set limit of Miscellaneous",
  "notification_type": "alert",
  "updated_at": "2024-07-05T13:59:23.663657",
  "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
}
```
**Delete Notification**
```
DELETE /api/v1/<user_id>/notifications/<notification_id>
```
Deletes a notification for a specific user.

***Parameters:***

`user_id` (string): ID of the user
`notification_id` (string): ID of the notification
**Response:**

204 No Content if the notification is successfully deleted
-json response format
```
{
  "success": true
}
adminpc@mike:~/spendsmart$

```
***example***
```
adminpc@mike:~/spendsmart$ curl -X DELETE http://localhost:5011/api/v1/ee95989a-20a1-41d9-bb18-131c649b91cc/notifications/b5143289-773b-4473-a16e-202f06f211e6
{
  "success": true
}
```
---
Using User Interface
---
Open  browser of your favourite choice e.g chrome
1. Landing Page:

- Navigate to the landing page at `http://localhost:5000/spendsmart` where you can find links to sign up or log in.
![Landing-page](/screenshots/landing-page-github.png)
2. Sign Up:

- Click on the "Sign Up" or "get started" button on the landing page or navigate to `http://localhost:5000/spendsmart/auth/signup` to create a new account.
![Signup-page](/screenshots/signup-github.png)

3. Log In:
- Click on the "Login" button on the landing page or navigate to `http://localhost:5000/spendsmart/auth/login` to log into your existing account.
![login-page](/screenshots/login-github.png)
4. Budget tracking & Expense monitoring:
- To do the following actions one must be signed in using the above two steps.
	- Set a budget monitor
		- this helps to differentiate categories to which the expenses to be logged belog and the duration to tracking.
		- click the "Set New monitor" button on the dashboard page or the "New monitor" button on the navigation bar.
		![monitor](/screenshots/new-monitor-github.png)
		- fill in the required credentials submit by clicking start monitoring.
		- On the dashboard, the budget to be monitored appears with 0% ready for tracking.
	- log an expense
		- click the "Log an expense" under recent purchases section if no expense has been loged so far or click the "Log expense" button on the navigation bar.
		![login-page](/screenshots/login-github.png)
		- fill in the required credentials and submit by clicking the "Log it!" button.
		- you can view the details of the logged expense on the recent purchases section on dashboard or:
			 - click on the 'receipt' looking image on the 'card' item named the budget name to which your expense is categorized as.
	- budget summary and financial standing:
		- click the "dashboard" button on the navigation bar
		- the card items shows the amount spent in percentage compared to the set limit indicated as 'Max limit' on the left side of each budget 'card' item.
		- click on the 'receipt' image on the top left of the budget name desired to get more details like amount remaining, duration remaining compared to  which the amount was expected to last and expenses bought for that budget.
		![dashboard](/screenshots/dashboard-github.png)
		- click 'Un-Track' button under the expanded budget card item to stop its tracking. Note that this will delete all the expenses that been purchased earlier under its name.

5. viewing and deleting  notifications:
	- click on "Notifications(`number of notifications present`)" button on the navbar to view current notifications, displayed as toasts.
	![notifications](/screenshots/notification-github.png)	
	- click on the `X` symbol on a notification to delete that notification.
6. Logout:
	- to logout, click the "Logout" button on the navigation bar, next time you visit the site, you'll be required to enter your credentials to get signed in.
7. Delete account
	![delete-account](/screenshots/account-github.png)
	- to delete your account, click the "Account" button on navigation bar and then the 'delete account' button under account management on the resulting page. This will delete all information related to you from the site.These includes your account credentials, expenses made, notifications and budgets being monitored.
	

8. View or edit recent purchases:
	![recent-purchases](/screenshots/dashboard-github.png)
	- to view recent purchaes, head over to the dashboard page by clicking the 'dashboard' button on navbar.
	- scroll the bottom section labeled 'Recent Purchases', recent purchases are displayed below that header as a rows in a table.
	- you can delete or move the recent purchase expenses ticking the checkbox on their side or clicking 'select all' , then click 'delete' for which they will be deleted from database, or 'move to' which will give you options for under which 'budget' you want the expense to be moved to, just select any of the desired budget name that suits you an you're done. checked expenses now belongs to that budget and all their information is transferred from the last budget to the latter.

**Contributing**
- Read this README entirely
- Fork the repo
- Play with it
- Check issues with the 'dev' tag

--------------------------------
**Related Projects**

[AirBnB_Clone_v4](https://github.com/mikelexx/AirBnB_clone_v4)

---------------------------------------
**License**
Public Domain. No copy write protection.
