## Step 58 

### Version 1 – N+1 Query

- Executes **1 query** to retrieve all enrollment records.
- Executes **1 additional query for each enrollment** to retrieve the corresponding student's name.
- For 11 enrollment records:
  - 1 query to fetch enrollments
  - 11 queries to fetch student names
  - **Total Queries: 12**
- Multiple database round-trips increase execution time and reduce performance.

### Version 2 – JOIN Query

- Retrieves enrollment records and student names using a single JOIN query.
- For the same 11 enrollment records:
  - **Total Queries: 1**
- Only one database round-trip is required, making it significantly more efficient.

### Performance Observation

| Approach | Queries Executed | Database Round-Trips |
|-----------|-----------------:|---------------------:|
| N+1 Query | 12 | 12 |
| JOIN Query | 1 | 1 |

The JOIN approach performs better because all required data is fetched in a single SQL query, reducing unnecessary database communication.

---

## Step 59 

### What happens with 10,000 enrollment records?

### N+1 Version

- 1 query to retrieve all enrollment records.
- 10,000 additional queries to retrieve each student's information.
- **Total Queries = 10,001**

### Optimized JOIN Version

- Retrieves all enrollment records and student information using a single JOIN query.
- **Total Queries = 1**


The N+1 problem causes a large number of unnecessary database queries, leading to poor performance as the dataset grows.

