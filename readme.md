## Meal Counts
1. Project structure
```py
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
# Rest API list - Meal Counts App

 **full sequential API list** with the order in which you should call them when using this modular Meal Management project. This is essential for frontend integration and for inserting data **daily, session-wise, and monthly**.

---

## **1️⃣ Sessions APIs (Create & list meal sessions)**

| Method | Endpoint     | Body / Query                                                                                        | Description                          |
| ------ | ------------ | --------------------------------------------------------------------------------------------------- | ------------------------------------ |
| POST   | `/sessions/` | `{ "name": "July 2025", "manager": "Munna", "start_date": "2025-07-01", "end_date": "2025-07-31" }` | Create a new meal session (monthly). |
| GET    | `/sessions/` | —                                                                                                   | Get all sessions.                    |

---

## **2️⃣ Members APIs (Create / Update / Delete members)**

| Method | Endpoint               | Body                          | Description                                            |
| ------ | ---------------------- | ----------------------------- | ------------------------------------------------------ |
| POST   | `/members/`            | `{ "name": "Alice" }`         | Create a new member.                                   |
| PUT    | `/members/{member_id}` | `{ "name": "Alice Updated" }` | Update member info.                                    |
| DELETE | `/members/{member_id}` | —                             | Delete member and all related deposits, meals, bazars. |

---

## **3️⃣ Deposits APIs (Daily deposits by members)**

| Method | Endpoint                 | Body                                                                       | Description                                 |
| ------ | ------------------------ | -------------------------------------------------------------------------- | ------------------------------------------- |
| POST   | `/deposits/`             | `{ "member_id": 1, "session_id": 1, "amount": 200, "date": "2025-07-01" }` | Add deposit for a member on a specific day. |
| PUT    | `/deposits/{deposit_id}` | `{ "amount": 300, "date": "2025-07-02" }`                                  | Update a deposit.                           |
| DELETE | `/deposits/{deposit_id}` | —                                                                          | Delete a deposit record.                    |

---

## **4️⃣ Meals APIs (Daily meal counts)**

| Method | Endpoint           | Body                                                                      | Description              |
| ------ | ------------------ | ------------------------------------------------------------------------- | ------------------------ |
| POST   | `/meals/`          | `{ "member_id": 1, "session_id": 1, "meals": 2.5, "date": "2025-07-01" }` | Add daily meal count.    |
| PUT    | `/meals/{meal_id}` | `{ "meals": 3, "date": "2025-07-02" }`                                    | Update daily meal count. |
| DELETE | `/meals/{meal_id}` | —                                                                         | Delete a meal record.    |

---

## **5️⃣ Bazar APIs (Daily purchases)**

| Method | Endpoint            | Body                                                                                                    | Description                |
| ------ | ------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------- |
| POST   | `/bazar/`           | `{ "member_id": 1, "session_id": 1, "amount": 500, "description": "Vegetables", "date": "2025-07-01" }` | Add a daily bazar expense. |
| PUT    | `/bazar/{bazar_id}` | `{ "amount": 600, "description": "Full Bazar", "date": "2025-07-02" }`                                  | Update bazar record.       |
| DELETE | `/bazar/{bazar_id}` | —                                                                                                       | Delete a bazar record.     |

---

## **6️⃣ Stats API (Session-based calculations)**

| Method | Endpoint                         | Query / Params   | Description                                                                                     |
| ------ | -------------------------------- | ---------------- | ----------------------------------------------------------------------------------------------- |
| GET    | `/stats/meal-stats/{session_id}` | `session_id` = 1 | Get total deposits, meals, bazar, meal rate, in-hand per member, overall in-hand for a session. |

---

## **7️⃣ Optional: Clear table APIs**

| Method | Endpoint                    | Query                     | Description                                                                           |
| ------ | --------------------------- | ------------------------- | ------------------------------------------------------------------------------------- |
| DELETE | `/clear-table/{table_name}` | Optional: `?session_id=1` | Delete all records in a table. For deposits, meals, bazar, you can filter by session. |

**`table_name` values:** `"members"`, `"deposits"`, `"meals"`, `"bazar"`

* Example: `/clear-table/meals?session_id=1` → clears all meals in session 1.

---

### ✅ **Recommended Workflow / Sequence**

1. **Create a session** → `/sessions/`
2. **Add members** → `/members/`
3. **Daily operations**:

   * Add deposits → `/deposits/`
   * Add meals → `/meals/`
   * Add bazar → `/bazar/`
4. **Update / Delete if needed** → respective PUT/DELETE APIs
5. **Check monthly stats** → `/stats/meal-stats/{session_id}`
6. **Start next month** → create a new session, repeat workflow

---

This **sequence ensures no old data interferes**, daily deposits, meals, and bazar are tracked with dates, and monthly reports can be generated **at any time**.

---
