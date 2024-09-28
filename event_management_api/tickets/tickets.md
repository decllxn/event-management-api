# Tickets App Documentation

## Overview

The **Tickets App** is designed to handle all aspects of ticket management for events in the Event Management API. It includes functionalities for ticket creation, booking, reservation management, validation, and payment integration. This app enables both event organizers and participants to effectively manage event tickets, providing a smooth and robust experience.

---

## Features

### 1. **Create Tickets**
   - **Description**: Event organizers can create multiple types of tickets for their events (e.g., Regular, VIP, Early Bird).
   - **Implementation**: 
     - Model: `Ticket`
     - Fields: `event`, `type`, `price`, `quantity`, `sold`, `available_from`, `available_until`
     - API Endpoint: `/tickets/create/`
     - Permissions: Only event organizers can create tickets for their events.
     - View: `TicketCreateView`
     - Method: `POST`

---

### 2. **List Available Tickets**
   - **Description**: Users can view all available tickets for a specific event.
   - **Implementation**:
     - API Endpoint: `/tickets/list/<int:event_id>/`
     - View: `TicketListView`
     - Method: `GET`
     - Displays only tickets that are available for booking and not sold out.

---

### 3. **Book/Reserve Tickets**
   - **Description**: Users can reserve or purchase tickets for an event.
   - **Implementation**:
     - API Endpoint: `/tickets/book/<int:ticket_id>/`
     - View: `TicketBookingView`
     - Method: `POST`
     - Logic: Reduces available ticket count upon successful booking, checks for availability, and raises error if sold out.

---

### 4. **Cancel Ticket Reservation**
   - **Description**: Users can cancel their reserved tickets before the event.
   - **Implementation**:
     - API Endpoint: `/tickets/cancel/<int:booking_id>/`
     - View: `TicketCancelView`
     - Method: `DELETE`
     - Logic: Increases the ticket count when a reservation is canceled.

---

### 5. **View My Tickets**
   - **Description**: Users can view all the events for which they have booked tickets.
   - **Implementation**:
     - API Endpoint: `/tickets/my-tickets/`
     - View: `UserTicketsView`
     - Method: `GET`
     - Shows a list of tickets the user has reserved for upcoming events.

---

### 6. **Event Organizer's View for Booked Tickets**
   - **Description**: Organizers can view a list of tickets booked for their events.
   - **Implementation**:
     - API Endpoint: `/tickets/organizer/booked-tickets/<int:event_id>/`
     - View: `OrganizerBookedTicketsView`
     - Method: `GET`
     - Displays the list of users who have booked tickets.

---

### 7. **Ticket Validation**
   - **Description**: Event organizers can validate the tickets at the event entry, typically by scanning a QR code.
   - **Implementation**:
     - Model: `TicketValidation`
     - API Endpoint: `/tickets/validate/<int:ticket_id>/`
     - View: `TicketValidationView`
     - Method: `POST`
     - Logic: Once validated, the ticket is marked as used to prevent multiple entries.

---

### 8. **Notifications for Ticket Purchase and Cancellation**
   - **Description**: Users receive notifications when they successfully purchase or cancel a ticket.
   - **Implementation**:
     - Sends both in-app and email notifications upon successful booking and cancellation.
     - Logic is integrated into the booking and cancellation views.

---

### 9. **Waiting List for Fully Booked Events**
   - **Description**: Users can join a waiting list if all tickets for an event are sold out.
   - **Implementation**:
     - Model: `WaitingList`
     - API Endpoint: `/tickets/waitlist/<int:event_id>/`
     - View: `WaitingListView`
     - Method: `POST`
     - Logic: If tickets become available, users on the waiting list are notified.

---

### 10. **Discount Codes**
   - **Description**: Organizers can create and apply discount codes to reduce ticket prices.
   - **Implementation**:
     - Model: `DiscountCode`
     - Fields: `code`, `discount_percentage`, `valid_from`, `valid_until`, `event`
     - API Endpoint: `/tickets/discount/apply/`
     - View: `ApplyDiscountCodeView`
     - Method: `POST`
     - Logic: The discount is applied to the ticket price when purchasing.

---

### 11. **Refunds for Canceled Events or Tickets**
   - **Description**: Users can request refunds if the event is canceled or they cancel their ticket reservation.
   - **Implementation**:
     - Model: `RefundRequest`
     - API Endpoint: `/tickets/refund/<int:ticket_id>/`
     - View: `TicketRefundView`
     - Method: `POST`
     - Logic: Refund requests are approved or denied by the event organizer.

---

### 12. **Ticket QR Code Generation**
   - **Description**: Generate QR codes for each booked ticket to allow easy validation.
   - **Implementation**:
     - Library: `qrcode`
     - QR Code is generated upon successful booking.
     - Logic: Users can download or view the QR code in their ticket details.
     - API Endpoint: `/tickets/qr-code/<int:ticket_id>/`
     - View: `GenerateQRCodeView`
     - Method: `GET`

---

### 13. **Ticket PDF Download**
   - **Description**: Users can download their tickets as PDFs, which include ticket details and the QR code.
   - **Implementation**:
     - Library: `reportlab` for generating PDFs.
     - API Endpoint: `/tickets/download/<int:ticket_id>/`
     - View: `DownloadTicketPDFView`
     - Method: `GET`
     - Logic: The ticket PDF contains user info, event details, and the QR code for validation.

---

## Models

### 1. **Ticket**
   - `event`: ForeignKey to the Event
   - `type`: Type of ticket (Regular, VIP, etc.)
   - `price`: Price of the ticket
   - `quantity`: Total number of tickets available
   - `sold`: Number of tickets sold
   - `available_from`: Date when tickets are available
   - `available_until`: Date when ticket sales close

### 2. **Booking**
   - `ticket`: ForeignKey to Ticket
   - `user`: ForeignKey to User
   - `quantity`: Number of tickets booked
   - `status`: Status of booking (Reserved, Canceled)

### 3. **DiscountCode**
   - `event`: ForeignKey to Event
   - `code`: Discount code string
   - `discount_percentage`: Percentage discount applied
   - `valid_from`: Date when the discount code becomes valid
   - `valid_until`: Date when the discount code expires

### 4. **WaitingList**
   - `user`: ForeignKey to User
   - `event`: ForeignKey to Event

### 5. **RefundRequest**
   - `booking`: ForeignKey to Booking
   - `status`: Status of the refund request (Pending, Approved, Rejected)

---

## API Endpoints

- **Create Ticket**: `/tickets/create/` (POST)
- **List Available Tickets**: `/tickets/list/<int:event_id>/` (GET)
- **Book Ticket**: `/tickets/book/<int:ticket_id>/` (POST)
- **Cancel Ticket Reservation**: `/tickets/cancel/<int:booking_id>/` (DELETE)
- **View My Tickets**: `/tickets/my-tickets/` (GET)
- **Organizer View for Booked Tickets**: `/tickets/organizer/booked-tickets/<int:event_id>/` (GET)
- **Ticket Validation**: `/tickets/validate/<int:ticket_id>/` (POST)
- **Apply Discount Code**: `/tickets/discount/apply/` (POST)
- **Request Refund**: `/tickets/refund/<int:ticket_id>/` (POST)
- **Generate QR Code**: `/tickets/qr-code/<int:ticket_id>/` (GET)
- **Download Ticket PDF**: `/tickets/download/<int:ticket_id>/` (GET)
- **Join Waiting List**: `/tickets/waitlist/<int:event_id>/` (POST)

---

## Conclusion

The **Tickets App** provides a comprehensive and flexible ticketing solution for events. It allows organizers to manage ticket sales, discount codes, and booking details while offering users the ability to reserve, manage, and download tickets easily.
