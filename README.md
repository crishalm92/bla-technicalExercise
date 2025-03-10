
# Task Managment Challenge

This project is the implementation of the challenge shared. Creates a FastAPI instance using PostgreSQL for handle the tasks endpoints.



## API Reference

#### authentication
```http
  GET /auth/login
```
This endpoints returns a Bearer token using the OAuth2PasswordBearer schema from FastAPI
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Your username |
| `password` | `string` | **Required**. Your password |

#### Create user

```http
  POST /users
```
Creates a new user in the database. Retrieves user's username and email. Also, hashes the password in the DB.
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required** |
| `email`      | `string` | **Required**.  |
| `password`      | `string` | **Required**. |



#### Get all tasks created by the auth user
```http
  GET /task/all
```
Returns all the tasks associated


#### Create task

```http
  POST /tasks/create
```
Creates a new task. The auth user will be the task creator.

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | **Required** |
| `description`      | `string` | **Required**.  |
| `due_date`      | `datetime` | **Required**. |
| `assigned_to`      | `string` | **Optional**. user's username|


#### Update task

```http
  PUT /tasks/{task_code}
```
Updates a task

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `task_code`      | `string` `path_parameter`| **Required** |
| `title`      | `string` | **Optional**.  |
| `description`      | `string` | **Optional**. |
| `due_date`      | `datetime` | **Optional**. |
| `assigned_to`      | `string` | **Optional**. |
| `status`      | `string` | **Optional**. |


#### Delete task

```http
  DELETE /tasks/{task_code}
```
This endpoint deletes a task, only if the auth user is the creator

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `task_code`      | `string` `path_parameter`| **Required** |


#### Read task

```http
  GET /tasks/task/{task_code}
```
Retrieve task information

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `task_code`      | `string` `path_parameter`| **Required** |


#### Mark task as completed

```http
  PUT /tasks/complete/{task_code}
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `task_code`      | `string` `path_parameter`| **Required** |


#### Filter task

```http
  GET /tasks/complete/{task_code}
```
Retrieves a list of task by filters and pagination

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `status`      | `string` `query_parameter`| **Required** new, in_progess, completed|
| `date_from`      | `date` `query_parameter`| **Required** |
| `date_to`      | `date` `query_parameter`| **Required** |
| `page`      | `int` `query_parameter`| **Required** page number|
| `size`      | `int` `query_parameter`| **Required** number of task per page|



## Run Locally

Create local environment using conda.

Create env:

```bash
  conda env create --file environment.yml
```

Create a .env file with the following configs:
```bash
SECRET_KEY = YOURKEY
ALGORITH = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_NAME = dbname
DATABASE_USER = test
DATABASE_PASSWORD = test
DATABASE_HOST = host:5432
# The next value represents the database engine. Can be switch to sqlite
DATABASE_ENGINE = postgres / sqlite
```

Start the server

```bash
  conda activate blatest
  uvicorn app.api.main:app --host 0.0.0.0 --port 8080
```


## Running Tests

To run tests, run the following command

```bash
  pytest app/api
```



## Next steps

Due to time range, I could add some features that I'll like to.
For next iterations, I'll like to add:

* Create an exceptions package and create custom classes. For example: ElementNotFound, CustomValueError, etc. With these exceptions, I'll create a new middleware that maps the exceptions with specific HTTP codes.

* Remove some logic from routers view and add to the specific service implementations. Such as the exception mentionated.

* Create a rate limit middleware for fastapi. The middleware will handle the amount of request per user and prevent the endpoint usage.

* Create more detailed unit tests with more complex scenarios.

* Config the auth schema in swagger for all the endpoints.

