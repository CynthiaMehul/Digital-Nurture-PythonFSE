# Hands-On 5: MongoDB – Document Modelling, CRUD & Aggregation

# Task 1: Create Collection and Insert Documents

## Step 62

```javascript
db.feedback.insertMany([
{
  student_id: 1,
  course_code: "CS101",
  semester: "2022-ODD",
  rating: 5,
  comments: "Excellent teaching. Would recommend.",
  tags: ["challenging", "well-structured", "good-examples"],
  submitted_at: ISODate("2022-11-30T10:15:00Z"),
  attachments: [
    { filename: "notes.pdf", size_kb: 240 }
  ]
},
{
  student_id: 2,
  course_code: "CS101",
  semester: "2022-ODD",
  rating: 4,
  comments: "Interesting course with practical examples.",
  tags: ["challenging", "interactive"],
  submitted_at: ISODate("2022-11-28T09:00:00Z"),
  attachments: [
    { filename: "assignment.pdf", size_kb: 180 }
  ]
},
{
  student_id: 3,
  course_code: "CS101",
  semester: "2022-EVEN",
  rating: 3,
  comments: "Good but needs more lab sessions.",
  tags: ["well-structured", "labs"],
  submitted_at: ISODate("2022-05-15T11:20:00Z"),
  attachments: [
    { filename: "feedback.docx", size_kb: 95 }
  ]
},
{
  student_id: 4,
  course_code: "CS102",
  semester: "2022-ODD",
  rating: 5,
  comments: "Loved the hands-on activities.",
  tags: ["practical", "good-examples"],
  submitted_at: ISODate("2022-11-29T08:30:00Z"),
  attachments: [
    { filename: "project.zip", size_kb: 520 }
  ]
},
{
  student_id: 5,
  course_code: "CS102",
  semester: "2021-EVEN",
  rating: 2,
  comments: "Too fast paced.",
  tags: ["difficult", "challenging"],
  submitted_at: ISODate("2021-12-10T14:00:00Z"),
  attachments: [
    { filename: "report.pdf", size_kb: 140 }
  ]
},
{
  student_id: 6,
  course_code: "CS103",
  semester: "2022-ODD",
  rating: 1,
  comments: "Needs better explanations.",
  tags: ["boring", "theory"],
  submitted_at: ISODate("2022-11-20T10:00:00Z"),
  attachments: [
    { filename: "complaint.pdf", size_kb: 120 }
  ]
},
{
  student_id: 7,
  course_code: "CS104",
  semester: "2022-EVEN",
  rating: 4,
  comments: "Very informative.",
  tags: ["interactive", "good-examples"],
  submitted_at: ISODate("2022-06-18T13:45:00Z"),
  attachments: [
    { filename: "notes.docx", size_kb: 200 }
  ]
},
{
  student_id: 8,
  course_code: "CS105",
  semester: "2021-EVEN",
  rating: 3,
  comments: "Average experience.",
  tags: ["theory", "well-structured"],
  submitted_at: ISODate("2021-11-15T15:20:00Z"),
  attachments: [
    { filename: "summary.pdf", size_kb: 170 }
  ]
},
{
  student_id: 9,
  course_code: "CS106",
  semester: "2022-ODD",
  rating: 5,
  comments: "Excellent course content.",
  tags: ["challenging", "practical"],
  submitted_at: ISODate("2022-11-25T16:00:00Z"),
  attachments: [
    { filename: "certificate.pdf", size_kb: 80 }
  ]
},
{
  student_id: 10,
  course_code: "CS107",
  semester: "2022-EVEN",
  rating: 2,
  comments: "Needs improvement.",
  tags: ["difficult", "theory"],
  submitted_at: ISODate("2022-07-12T12:10:00Z"),
  attachments: [
    { filename: "feedback.pdf", size_kb: 110 }
  ]
}
]);
```

---

## Step 63

```javascript
db.feedback.insertOne({
  student_id: 11,
  course_code: "CS101",
  semester: "2022-ODD",
  rating: 4,
  comments: "Well organized course with helpful faculty.",
  tags: ["well-structured", "interactive"],
  submitted_at: ISODate("2022-11-26T09:30:00Z")
});
```

---

## Step 64

```javascript
db.feedback.countDocuments();
```

---

# Task 2: CRUD Operations

## Step 65 

```javascript
db.feedback.find({
  rating: 5
});
```

---

## Step 66 

```javascript
db.feedback.find({
  course_code: "CS101",
  tags: "challenging"
});
```

Using `$elemMatch`:

```javascript
db.feedback.find({
  course_code: "CS101",
  tags: {
    $elemMatch: {
      $eq: "challenging"
    }
  }
});
```

---

## Step 67

```javascript
db.feedback.find(
  {},
  {
    student_id: 1,
    course_code: 1,
    rating: 1,
    _id: 0
  }
);
```

---

## Step 68

```javascript
db.feedback.updateMany(
  {
    rating: {
      $lt: 3
    }
  },
  {
    $set: {
      needs_review: true
    }
  }
);
```

---

## Step 69

```javascript
db.feedback.updateMany(
  {
    needs_review: true
  },
  {
    $push: {
      tags: "reviewed"
    }
  }
);
```

---

## Step 70

```javascript
db.feedback.deleteMany({
  semester: "2021-EVEN"
});
```

---

# Task 3: Aggregation Pipeline

## Step 71

```javascript
db.feedback.aggregate([
  {
    $match: {
      semester: "2022-ODD"
    }
  },
  {
    $group: {
      _id: "$course_code",
      avg_rating: {
        $avg: "$rating"
      },
      total_feedback: {
        $sum: 1
      }
    }
  },
  {
    $sort: {
      avg_rating: -1
    }
  }
]);
```

---

## Step 72

```javascript
db.feedback.aggregate([
  {
    $match: {
      semester: "2022-ODD"
    }
  },
  {
    $group: {
      _id: "$course_code",
      avg_rating: {
        $avg: "$rating"
      },
      total_feedback: {
        $sum: 1
      }
    }
  },
  {
    $sort: {
      avg_rating: -1
    }
  },
  {
    $project: {
      average_rating: {
        $round: ["$avg_rating", 1]
      },
      total_feedback: 1
    }
  }
]);
```

---

## Step 73 

```javascript
db.feedback.aggregate([
  {
    $unwind: "$tags"
  },
  {
    $group: {
      _id: "$tags",
      count: {
        $sum: 1
      }
    }
  },
  {
    $sort: {
      count: -1
    }
  }
]);
```

---

## Step 74 

```javascript
db.feedback.createIndex({
  course_code: 1
});
```

Verify the index:

```javascript
db.feedback.find({
  course_code: "CS101"
}).explain("executionStats");
```

- Created an ascending index on course_code.
- Verified index usage using explain("executionStats").
- The execution plan shows **IXSCAN**, confirming that MongoDB uses the index instead of performing a **COLLSCAN**.

---
