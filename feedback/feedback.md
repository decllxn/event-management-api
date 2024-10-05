# Feedback App Documentation

## Overview

The **Feedback App** allows users to provide feedback for events, including ratings and comments. Event organizers can view the feedback and receive notifications when new feedback is submitted. Users can also submit feedback anonymously and edit or delete their feedback. The app ensures user-friendly interaction with robust notification features for event organizers.

## Features

1. **Submit Feedback**: 
   - Authenticated users can submit feedback for specific events.
   - Feedback includes a comment and a rating (on a scale of 1 to 5).
   - Users can choose to submit feedback anonymously.

2. **View Event Feedback**:
   - Users and event organizers can view all feedback for a particular event.
   - Feedback is displayed with associated user information (or marked as "Anonymous").

3. **Edit Feedback**:
   - Users can edit the feedback they have previously submitted.
   - Allows changes to both comment and rating.
   
4. **Delete Feedback**:
   - Users have the option to delete their submitted feedback.

5. **Anonymous Feedback**:
   - Users can submit feedback anonymously, hiding their identity from the event organizer and other users.

6. **Feedback Notifications**:
   - Event organizers are notified whenever feedback is submitted for their event.
   - Notifications are marked as unread by default, and organizers can manage these notifications through a dedicated view.
   
7. **Event Rating Aggregation**:
   - The average rating of an event is calculated based on user feedback.
   - Event organizers can view the aggregated rating score for their event, providing a quick overview of how the event is perceived.

## API Endpoints

- **Submit Feedback**: 
  - Endpoint: `/feedback/submit/<event_id>/`
  - Method: `POST`
  - Request Body: 
    ```json
    {
      "comment": "Great event!",
      "rating": 5,
      "anonymous": false
    }
    ```

- **View Feedback for an Event**: 
  - Endpoint: `/feedback/event/<event_id>/feedbacks/`
  - Method: `GET`
  - Description: Retrieves all feedback for a specific event, including both anonymous and non-anonymous comments.

- **Edit Feedback**:
  - Endpoint: `/feedback/edit/<feedback_id>/`
  - Method: `PUT`
  - Description: Allows users to edit their previously submitted feedback.

- **Delete Feedback**:
  - Endpoint: `/feedback/delete/<feedback_id>/`
  - Method: `DELETE`
  - Description: Allows users to delete their feedback.

- **View Feedback Notifications**:
  - Endpoint: `/feedback/notifications/`
  - Method: `GET`
  - Description: Retrieves unread feedback notifications for event organizers, helping them keep track of new feedback.

## Models

- **Feedback**: Stores feedback comments and ratings submitted by users.
  - Fields: `user`, `event`, `comment`, `rating`, `anonymous`, `created_at`, `updated_at`.

- **FeedbackNotification**: Tracks feedback notifications sent to event organizers when new feedback is submitted.
  - Fields: `event`, `organizer`, `feedback`, `is_read`, `created_at`.

## Feedback Notification System

- When a user submits feedback, the event organizer automatically receives a notification.
- Notifications are created with an "unread" status and can be viewed by the event organizer.
- The organizer can mark notifications as read once they have been acknowledged.

## Anonymous Feedback

- If a user chooses to submit feedback anonymously, their identity will not be revealed to other users or the event organizer. Instead, the feedback will be labeled as from "Anonymous."

## User Permissions

- **Authenticated Users**: Can submit, edit, and delete their own feedback.
- **Event Organizers**: Can view all feedback for their events and receive notifications for new feedback.
- **Anonymous Users**: Feedback submission is restricted to authenticated users. Anonymous feedback refers to hiding user identity, not allowing unauthenticated submissions.

## Aggregate Event Rating

- An event's rating is calculated as the average of all feedback ratings submitted.
- The aggregate score provides event organizers with insights into how their event is being received by attendees.

## Testing the Feedback API

1. **Submit Feedback**:
   - Send a POST request to `/feedback/submit/<event_id>/` with the feedback details (comment, rating, and anonymous status).
   
2. **View Feedback**:
   - Use the GET request at `/feedback/event/<event_id>/feedbacks/` to retrieve all feedback for a given event.

3. **Edit Feedback**:
   - Update feedback using the PUT request at `/feedback/edit/<feedback_id>/` with new comment or rating details.

4. **Delete Feedback**:
   - Remove feedback using the DELETE request at `/feedback/delete/<feedback_id>/`.

5. **Check Notifications**:
   - Event organizers can check their feedback notifications by sending a GET request to `/feedback/notifications/`.

---

## Future Enhancements

- **Feedback Search**: Implement a search feature to filter feedback by keywords or rating.
- **Feedback Analytics**: Provide organizers with insights and statistics based on event feedback, such as most common keywords, satisfaction trends, etc.
- **Public Feedback Display**: Allow organizers to make feedback publicly visible to encourage new participants to join future events.