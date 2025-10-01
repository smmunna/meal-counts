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

# 📌 Meal Management API Documentation

---

## 👤 **Members**

### ➕ Create Member

**POST** `/members/`
**Body:**

```json
{
  "name": "John Doe"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "John Doe"
}
```

---

### ✏️ Update Member

**PUT** `/members/{member_id}`
**Body:**

```json
{
  "name": "John Updated"
}
```

**Response:**

```json
{
  "message": "Member updated",
  "member": { "id": 1, "name": "John Updated" }
}
```

---

### ❌ Delete Member

**DELETE** `/members/{member_id}`

Deletes member and all related deposits, meals, bazar.

**Response:**

```json
{
  "message": "Member ID 1 and all related records deleted"
}
```

---

## 💰 **Deposits**

### ➕ Add Deposit

**POST** `/deposit/`
**Body:**

```json
{
  "member_id": 1,
  "amount": 200
}
```

**Response:**

```json
{
  "id": 1,
  "member_id": 1,
  "amount": 200
}
```

---

### ✏️ Update Deposit

**PUT** `/deposit/{deposit_id}`
**Body:**

```json
{
  "amount": 500
}
```

---

### ❌ Delete Deposit

**DELETE** `/deposit/{deposit_id}`

---

## 🍽️ **Meals**

### ➕ Add Meal

**POST** `/meal/`
**Body:**

```json
{
  "member_id": 1,
  "meals": 2.5
}
```

---

### ✏️ Update Meal

**PUT** `/meal/{meal_id}`
**Body:**

```json
{
  "meals": 3.0
}
```

---

### ❌ Delete Meal

**DELETE** `/meal/{meal_id}`

---

## 🛒 **Bazar (Expenses)**

### ➕ Add Bazar

**POST** `/bazar/`
**Body:**

```json
{
  "member_id": 1,
  "amount": 1000,
  "description": "Vegetables and rice"
}
```

---

### ✏️ Update Bazar

**PUT** `/bazar/{bazar_id}`
**Body:**

```json
{
  "amount": 1200,
  "description": "Updated expense"
}
```

---

### ❌ Delete Bazar

**DELETE** `/bazar/{bazar_id}`

---

## 📊 **Statistics**

### 🔍 Get Meal Stats

**GET** `/meal-stats/`

**Response Example:**

```json
{
  "total_bazar": 3000,
  "total_deposit": 3200,
  "total_meals": 60,
  "total_meal_cost": 3000,
  "meal_rate": 50.0,
  "overall_in_hand": 200,
  "members": [
    {
      "name": "John Doe",
      "deposit": 1200,
      "meals": 25,
      "meal_cost": 1250,
      "in_hand": -50
    },
    {
      "name": "Jane Doe",
      "deposit": 1000,
      "meals": 20,
      "meal_cost": 1000,
      "in_hand": 0
    }
  ]
}
```

---

## 🗑️ **Utility APIs**

### ❌ Clear Entire Table

**DELETE** `/clear-table/{table_name}`

Example:

```
DELETE /clear-table/members
```

**Valid table names:** `members`, `deposits`, `meals`, `bazar`

---

✅ This list should cover **everything you need** for your frontend.
You can use it to build:

* A **dashboard** (meal stats, overall balance)
* A **member management UI** (add/update/delete members)
* Deposit/Meal/Bazar tracking forms
* A reset/clear system

---
