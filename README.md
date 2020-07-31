# Chat-Application
Chat Application built while ensuring easy integration of it in other projects

### Current Features:
This is a basic light-weight chat application implemented in django using django channels which serves real time chatting between two users

It uses reconnecting websockets to communicate between the front-end and backend. 
A custom authentication system is not in place so django's admin site will have to be used to create users

Currently the /chat path displays all users, but this can be easily changed to only display users which satisfy a given criteria using the ORM
The chat messages are always saved to the database, and also loaded in the template when a chat is opened.

### Future updates:
The loading is to be done dynamically which means the entire chat history between two users should not be sent at once (as doing so could be very slow and inefficient)

Instead, we will send chunks of messages (say of size 15 messages) to the template at a time using AJAX calls [psudo-code already created for this]
