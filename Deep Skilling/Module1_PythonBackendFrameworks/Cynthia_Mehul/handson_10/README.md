# Course Management Microservices

| Service              | Responsibility              | Endpoints          | Database         |
|----------------------|-----------------------------|--------------------|------------------|
| Student Service      | Student CRUD and enrollment | /api/students      | students.db      |
| Course Service       | Course CRUD                 | /api/courses       | courses.db       |
| Auth Service         | Registration, Login, JWT    |                    | auth.db          |
| Notification Service | Email notifications         | /api/notifications | notifications.db |


# Inter-Service Communication

## Synchronous Communication (HTTP)

In synchronous communication, one service sends an HTTP request to another service and waits for a response before continuing.

### Advantages

* Simple to implement.
* Immediate response.
* Easy to test.

### Disadvantages

* Services are tightly coupled.
* If one service is down, the request fails.

Example: Student Service calls Course Service to verify a course before enrollment.


## Asynchronous Communication (Message Queue)

In asynchronous communication, a service sends a message to a queue instead of directly calling another service. The receiving service processes it later.

### Advantages

* Services are loosely coupled.
* Better scalability and fault tolerance.

## Disadvantages

* More complex to set up.
* Response is not immediate.


## When to use RabbitMQ or Kafka?

Use RabbitMQ or Kafka when one service doesn't need an immediate response from another service. Instead of waiting, it sends a message and continues its work, while the other service processes the message later.

Examples:
* Sending email notifications
* Logging
* Processing background tasks
* Real-time event streaming (Kafka)

