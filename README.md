---

# 🧠 Research Project Backend (FastAPI + MongoDB)

This repository contains the **FastAPI backend** for the research project.
It provides REST APIs built with **FastAPI** and **MongoDB**, designed to support a Flutter mobile application.

---

## 🚀 Tech Stack

* **Python 3.10+**
* **FastAPI**
* **Uvicorn**
* **MongoDB**
* **Motor (Async MongoDB driver)**
* **Pydantic**

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── database/
│   │   └── mongo.py         # MongoDB connection
│   ├── models/              # DB models (optional)
│   ├── schemas/             # Pydantic schemas
│   ├── routes/              # API routes
│   ├── services/            # Business logic / AI calls
│   └── core/                # Config / settings
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Prerequisites

Install the following:

* **Python 3.10+**
* **Git**
* **MongoDB**

  * Local MongoDB **or**
  * MongoDB Atlas (cloud – free tier)

Check:

```bash
python --version
git --version
```

---

## 🧩 Step-by-Step Setup (After Cloning)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SLIIT-Y4-Research-Group/Research_Project_Backend.git
cd Research_Project_Backend/backend
```

---

### 2️⃣ Create Virtual Environment

#### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the `backend/` folder:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=research_db
```

👉 For MongoDB Atlas:

```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/
MONGO_DB_NAME=research_db
```

---

### 5️⃣ Run MongoDB

#### Local MongoDB

Make sure MongoDB is running:

```bash
mongod
```

Or via **MongoDB Compass**

---

### 6️⃣ Run the FastAPI Server

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 📚 API Documentation

FastAPI provides auto-generated docs:

* Swagger UI:

```
http://127.0.0.1:8000/docs
```

* Redoc:

```
http://127.0.0.1:8000/redoc
```

---

## 🧪 Testing APIs

You can test APIs using:

* Swagger UI (`/docs`)
* Postman
* Curl

Example POST request body:

```json
{
  "child_id": 1,
  "mood": "happy",
  "note": "Feeling good today"
}
```

---

## 🗄 MongoDB Details

* Database name: `research_db`
* Collections are created **automatically**
* No migrations required

Mongo connection file:

```
app/database/mongo.py
```

---

## 🛑 Common Issues & Fixes

### ❌ `ModuleNotFoundError: No module named 'app'`

✅ Run `uvicorn` **inside the backend folder**

---

### ❌ MongoDB connection error

✅ Check:

* MongoDB is running
* `MONGO_URI` is correct
* IP whitelist enabled (MongoDB Atlas)

---

### ❌ `uvicorn` not recognized

✅ Run:

```bash
pip install uvicorn
```

and activate virtual environment.

---

## 🌐 Free Deployment Options (MongoDB Compatible)

You can deploy this backend for free using:

| Platform       | Notes                |
| -------------- | -------------------- |
| **Render**     | Best option          |
| **Railway**    | Easy MongoDB support |
| **Deta Space** | Lightweight APIs     |

Deployment command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 🔐 Security Notes

* Do **NOT** commit `.env` file
* Use environment variables in production
* Enable MongoDB Atlas IP restrictions

---
## Deployment (AWS EC2 + S3)

See `docs/DEPLOYMENT_EC2_S3.md` for a full pipeline setup, EC2 provisioning steps, and S3-based model delivery.

---


## 👨‍💻 Author

**Dhanuka Navodya**

---

## 📄 License

This project is for **research and educational purposes only**.

---

If you want, I can also:

* Add **Docker + MongoDB**
* Prepare **Render / Railway deployment configs**
* Optimize MongoDB schema
* Connect **Flutter app APIs**

Just say the word 🚀

