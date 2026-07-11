'''
1. Draw or describe (in comments inside a new file notes.py) the journey of a GET /api/courses/ request 
through a Django application: URL router → View → Model (DB query) → Response.

Request-Response cycle in Django:
i) The client accesses the URL /api/courses/ 
ii) Request is sent to Django server
iii) Django checks the requested URL against the URL patterns defined in urls.py
iv) The corresponding view function defined in views.py is called.
v) The view interacts with the model defined in models.py to query the database.
vi) The view formats the data and returns an HTTP response or JSON response to the client

'''

'''
2. Identify where middleware sits in this cycle. Name two built-in Django middleware classes and 
describe what each does.

Middleware interacts between the browser and the view, it processes request before it reaches view and processes 
response before it reaches the client browser.

Built-in Django middleware classes:
 
i) SecurityMiddleware: Adds security features to protect django application. 
It force HTTPS instead of HTTP, 
prevents common web attacks and 
makes application secure with minimal configurations

ii) SessionMiddleware: Session stores data about a user across multiple requests. 
The session ID is usually stored in a cookie in the user's browser,
while the session data is stored on the server.
'''

'''
3. Explain the difference between WSGI and ASGI in comments. State which one Django uses by default 
and when you would switch to ASGI.

These are two different ways django communicates with web servers.

WSGI (Web Server Gateway Interface) handles requests synchronously. It processes one request at a time, 
making it suitable for traditional web applications that do not require real-time features.

ASGI (Asynchronous Server Gateway Interface) is a more modern specification that supports both synchronous and asynchronous communication. 
It is designed to handle real-time applications.

By default, Django uses WSGI. You would switch to ASGI when your application requires 
asynchronous features such as WebSockets, live chat, notifications, or other real-time communication.
'''

'''
4. Explain the MVC pattern, then map it to Django's MVT (Model-View-Template): what does each letter 
correspond to in Django?

The MVC (Model-View-Controller) pattern is an architectural pattern that separates an application into three interconnected components:
Model - interacts with the database and handles data logic
View - the user interface displayed to the user
Controller - handles user requests, communicates with the model and returns view to display

In Django's MVT (Model-View-Template) pattern:
Model - represents the data structure and interacts with the database defined in models.py file
View - corresponds to the logic that communicates between the model and the template defined in views.py file
Template - corresponds to the user interface defined in templates folder
'''

'''
Django Project - project is the whole application that contains settings, apps, database configurations and url configurations
Django App - app is one module of the project that contains models, views, templates and urls for that specific functionaility. 
A project can have multiple apps.
'''