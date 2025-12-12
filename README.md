# The-Wedding-Compamy-Assignment-PREJAN-RAJA-S---RA2211047010019
# Wedding Organization Management Service

A backend service built using **FastAPI** and **MongoDB** that supports **multi-tenant organization management**.  
Each organization has its own dynamically created collection while global metadata is stored in a master database.

This project is implemented as part of a **Backend Intern Assignment**.

---

##  Tech Stack

- **FastAPI** – Backend framework
- **MongoDB Atlas** – Database
- **Motor** – Async MongoDB driver
- **JWT (JSON Web Token)** – Authentication
- **bcrypt** – Password hashing
- **Pydantic** – Data validation

---

##  Architecture Overview

- **Master Database (`master_db`)**
  - Stores organization metadata
  - Stores admin credentials
- **Dynamic Collections**
  - Each organization gets its own collection: `org_<organization_name>`
- **JWT-based Authentication**
  - Admin login returns JWT
  - UPDATE and DELETE operations are protected

---

##  Project Structure
``` bash
wedding_org_service/
│── app/
│ ├── main.py
│ ├── config.py
│ ├── database.py
│ ├── utils.py
│ ├── auth.py
│ ├── models/
│ │ ├── organization.py
│ │ ├── user.py
│ │ └── responses.py
│ ├── routers/
│ │ ├── org_router.py
│ │ └── admin_router.py
│── .env
│── requirements.txt
│── README.md
```

---

##  Environment Setup

Create a `.env` file in the root directory:

```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
JWT_SECRET=supersecretkey
```

Install Dependencies
``` bash
pip install -r requirements.txt
```
Run the Application
``` bash
uvicorn app.main:app --reload
```
API Base URL: http://127.0.0.1:8000
Authentication Flow

- Create an organization (admin is created automatically)

- Login using admin credentials

- Receive JWT token

- Use token to access protected endpoints (UPDATE, DELETE)

API Endpoints
``` bash
ORGANIZATION API
| Method | Endpoint      | Description                        |
| ------ | ------------- | ---------------------------------- |
| POST   | `/org/create` | Create organization                |
| GET    | `/org/get`    | Get organization by name           |
| PUT    | `/org/update` | Update organization (JWT required) |
| DELETE | `/org/delete` | Delete organization (JWT required) |
```
``` bash
  ADMIN API
| Method | Endpoint       | Description |
| ------ | -------------- | ----------- |
| POST   | `/admin/login` | Admin login |
```
Example Requests
Create Organization
``` bash
{
  "organization_name": "WeddingCo",
  "email": "admin@wedding.com",
  "password": "Pass@123"
}

```
Admin Organization
``` bash
{
  "email": "admin@wedding.com",
  "password": "Pass@123"
}
```
Design Choices

- Single Master DB for scalability

- Dynamic collections for tenant isolation

- JWT-based stateless authentication

- Async MongoDB operations for performance

Scalability & Trade-offs
Pros

Easy tenant isolation

Horizontally scalable

Stateless authentication

Trade-offs

Large number of collections can increase DB management complexity

Cross-tenant analytics need aggregation at master DB level

Conclusion

This architecture is clean, scalable, and production-ready, making it suitable for multi-tenant SaaS-style applications.

