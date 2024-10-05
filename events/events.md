# Event Management API - Events App Documentation

This document outlines the development process and endpoints for the `events` app in the Event Management API.

## Features Implemented
1. **Event Creation**
2. **Event Registration**
3. **Event Listing**
4. **Event Detail**
5. **Event Update**
6. **Event Deletion**
7. **Participant Management**
8. **Event Categorization**
9. **Event Search**
10. **Event Cancellation**
11. **Past Events Listing**
12. **Upcoming Events Listing**
13. **User-Created Events Listing**
14. **Event Participant Management**

## URLs Defined

### Event Endpoints

- **Create Event**  
  **URL**: `/events/create/`  
  **Method**: `POST`  
  **Description**: Allows users to create new events.
  
- **List Events**  
  **URL**: `/events/list/`  
  **Method**: `GET`  
  **Description**: Provides a list of all available events.

- **Event Details**  
  **URL**: `/events/detail/<int:pk>/`  
  **Method**: `GET`  
  **Description**: Fetches details for a specific event using the event's ID.

- **Update Event**  
  **URL**: `/events/update/<int:pk>/`  
  **Method**: `PUT`  
  **Description**: Updates the details of a specific event.

- **Delete Event**  
  **URL**: `/events/delete/<int:pk>/`  
  **Method**: `DELETE`  
  **Description**: Deletes a specific event by its ID.

- **Register for Event**  
  **URL**: `/events/register/<int:pk>`  
  **Method**: `POST`  
  **Description**: Registers a user for the event.

### Participant and Category Management

- **List Event Participants**  
  **URL**: `/events/<int:pk>/participants/`  
  **Method**: `GET`  
  **Description**: Retrieves a list of participants for a specific event.

- **Manage Event Participants**  
  **URL**: `/events/manage-participants/<int:pk>/`  
  **Method**: `POST`, `DELETE`  
  **Description**: Allows the organizer to manage participants (add/remove).

- **List Event Categories**  
  **URL**: `/events/categories/`  
  **Method**: `GET`  
  **Description**: Lists all available event categories.

- **Filter Events by Category**  
  **URL**: `/events/category/<int:category_id>/`  
  **Method**: `GET`  
  **Description**: Lists events filtered by the specified category.

### Search and Event Status

- **Search Events**  
  **URL**: `/events/search/`  
  **Method**: `GET`  
  **Description**: Allows searching of events based on different criteria.

- **Cancel Event**  
  **URL**: `/events/cancel/<int:pk>/`  
  **Method**: `POST`  
  **Description**: Allows an organizer to cancel an event.

- **Past Events**  
  **URL**: `/events/past-events/`  
  **Method**: `GET`  
  **Description**: Lists past events that have already occurred.

- **Upcoming Events**  
  **URL**: `/events/upcoming-events/`  
  **Method**: `GET`  
  **Description**: Lists upcoming events.

### User-Specific Views

- **List User's Created Events**  
  **URL**: `/events/my-events/`  
  **Method**: `GET`  
  **Description**: Lists events created by the currently authenticated user.

## Code Overview

### 1. **Event Model**
- The Event model was extended to include fields like title, description, date, time, location, etc., as well as a foreign key linking it to the user who created the event.

### 2. **Views**:
- Implemented views using Django's `GenericAPIView` classes and custom logic for handling event creation, listing, updating, and more.

### 3. **Serializers**:
- Custom serializers were defined to handle the data structure of events, ensuring that all fields are validated properly.

### 4. **Permissions**:
- Custom permissions were used to ensure only event organizers can update or delete events, while regular users can register for events and view event details.

### Testing

- All endpoints have been tested using **Postman** to ensure correct functionality.
- The following status codes were confirmed during testing:
  - `200 OK`: For successful `GET` and `PUT` requests.
  - `201 Created`: For successful `POST` requests like creating an event or registering.
  - `204 No Content`: For successful deletion of events.
  - `404 Not Found`: For invalid event ID requests.
  - `403 Forbidden`: For restricted access to unauthorized users.

---