### Step 104 

Executed:

```bash
alembic current
```

Output:

```text
70ca072012ca (head)
```

Verified that the database is currently at the latest Alembic migration revision (`head`).

Executed: 

### Step 105

```bash
alembic downgrade -1
```

Output: 

```text
Running downgrade 70ca072012ca -> 0ab9a2fd066a, add course_schedule table
```

Verified that the database is currently at the previous Alembic migration revision. The created table "Course_Schedule" is dropped.

### Step 106

```bash
alembic downgrade base
```

Verified that the database rolled back all the performed migrations. Course_Schedule table is removed and is_active column in students table is also removed.

### Step 107

```bash
alembic upgrade head
```

Output:
```text
70ca072012ca (head)
```

Verified that the previous migrations are restored. Course_Schedule is added to the database and is_active column is added to students table again.