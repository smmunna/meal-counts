# Meal Counts Backend Integration

A **FastAPI-based meal management system** for tracking members, daily meals, deposits, bazar, and session-wise monthly reports.

This project supports **daily operations** while keeping previous months intact. You can generate **session-wise stats** anytime.

---

## **Project Structure**

```text
meal_project/
│── main.py
│── database.py
│── models.py
│── schemas.py
│── routers/
│   ├── members.py
│   ├── deposits.py
│   ├── meals.py
│   ├── bazars.py
│   └── sessions.py
```

---

## **API List with Example Requests**

### **1️⃣ Sessions APIs (Monthly meal sessions)**

| Method | Endpoint     | Example Body                                                                                            | Description                          |
| ------ | ------------ | ------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| POST   | `/sessions/` | `json {"name": "July 2025", "manager": "Munna", "start_date": "2025-07-01", "end_date": "2025-07-31"} ` | Create a new meal session (monthly). |
| GET    | `/sessions/` | —                                                                                                       | Get all sessions.                    |

---

### **2️⃣ Members APIs (Create / Update / Delete members)**

| Method | Endpoint               | Example Body                      | Description                                            |
| ------ | ---------------------- | --------------------------------- | ------------------------------------------------------ |
| POST   | `/members/`            | `json {"name": "Alice"} `         | Create a new member.                                   |
| PUT    | `/members/{member_id}` | `json {"name": "Alice Updated"} ` | Update member info.                                    |
| DELETE | `/members/{member_id}` | —                                 | Delete member and all related deposits, meals, bazars. |

---

### **3️⃣ Deposits APIs (Daily deposits by members)**

| Method | Endpoint                 | Example Body                                                                   | Description                                 |
| ------ | ------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------- |
| POST   | `/deposits/`             | `json {"member_id":1, "session_id":1, "amount":200, "dep_date":"2025-07-01"} ` | Add deposit for a member on a specific day. |
| PUT    | `/deposits/{deposit_id}` | `json {"amount":300, "dep_date":"2025-07-02"} `                                | Update a deposit.                           |
| DELETE | `/deposits/{deposit_id}` | —                                                                              | Delete a deposit record.                    |

---

### **4️⃣ Meals APIs (Daily meal counts)**

| Method | Endpoint           | Example Body                                                                   | Description              |
| ------ | ------------------ | ------------------------------------------------------------------------------ | ------------------------ |
| POST   | `/meals/`          | `json {"member_id":1, "session_id":1, "meals":2.5, "meal_date":"2025-07-01"} ` | Add daily meal count.    |
| PUT    | `/meals/{meal_id}` | `json {"meals":3, "meal_date":"2025-07-02"} `                                  | Update daily meal count. |
| DELETE | `/meals/{meal_id}` | —                                                                              | Delete a meal record.    |

---

### **5️⃣ Bazar APIs (Daily purchases)**

| Method | Endpoint            | Example Body                                                                                                 | Description                |
| ------ | ------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------- |
| POST   | `/bazar/`           | `json {"member_id":1, "session_id":1, "amount":500, "description":"Vegetables", "bazar_date":"2025-07-01"} ` | Add a daily bazar expense. |
| PUT    | `/bazar/{bazar_id}` | `json {"amount":600, "description":"Full Bazar", "bazar_date":"2025-07-02"} `                                | Update bazar record.       |
| DELETE | `/bazar/{bazar_id}` | —                                                                                                            | Delete a bazar record.     |

---

### **6️⃣ Stats API (Session-based calculations)**

| Method | Endpoint                         | Example Request       | Description                                                                                     |
| ------ | -------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------- |
| GET    | `/stats/meal-stats/{session_id}` | `/stats/meal-stats/1` | Get total deposits, meals, bazar, meal rate, in-hand per member, overall in-hand for a session. |

---

### **7️⃣ Optional: Clear table APIs**

| Method | Endpoint                    | Example Request                   | Description                                                                  |
| ------ | --------------------------- | --------------------------------- | ---------------------------------------------------------------------------- |
| DELETE | `/clear-table/{table_name}` | `/clear-table/meals?session_id=1` | Delete all records in a table. Can filter deposits, meals, bazar by session. |

**`table_name` values:** `"members"`, `"deposits"`, `"meals"`, `"bazar"`

---

### **8️⃣ Reset Full Database (Optional / Development)**

| Method | Endpoint                 | Description                                                  |
| ------ | ------------------------ | ------------------------------------------------------------ |
| DELETE | `/admin/reset-database/` | Drops all tables and recreates them. ⚠️ All data is deleted! |

---

## **Recommended Workflow / Sequence**

1. **Create a session** → `/sessions/`

2. **Add members** → `/members/`

3. **Daily operations**:

   * Add deposits → `/deposits/`
   * Add meals → `/meals/`
   * Add bazar → `/bazar/`

4. **Update / Delete if needed** → respective PUT/DELETE APIs

5. **Check session stats** → `/stats/meal-stats/{session_id}`

6. **Next month** → create a new session and repeat the workflow

---

## **Notes**

* All deposits, meals, and bazars are **tracked by session and date**.

* **Renamed date fields in JSON** to avoid conflicts:

  * Deposits → `dep_date`
  * Meals → `meal_date`
  * Bazar → `bazar_date`

* This ensures **monthly isolation**, previous months won’t interfere with current calculations.

* Fully compatible for **frontend integration**; you can generate daily and monthly reports per session.

---
