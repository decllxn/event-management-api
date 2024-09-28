from django.db import models
from events.models import Event
from qr_code import qrcode
from io import BytesIO
from django.core.files import File
from reportlab.pdfgen import canvas
from users.models import User

class TicketType(models.Model):
    event = models.ForeignKey(Event, related_name='ticket_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.event.title}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='tickets')
    is_reserved = models.BooleanField(default=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    pdf_ticket = models.FileField(upload_to='pdf_tickets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = self.generate_qr_code()
        if not self.pdf_ticket:
            self.pdf_ticket = self.generate_pdf_ticket()
        super().save(*args, **kwargs)

    def generate_qr_code(self):
        qr_img = qrcode.make(f"Ticket-{self.pk}-{self.user.email}")
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        file_name = f"ticket_qr_{self.pk}.png"
        return File(buffer, name=file_name)
    
    def generate_pdf_ticket(self):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, f"Ticket for {self.event.title}")
        p.drawString(100, 730, f"Ticket Type: {self.ticket_type.name}")
        p.drawString(100, 710, f"User: {self.user.email}")
        p.drawString(100, 710, f"Price: {self.ticket_type.price}")
        p.drawImage(self.qr_code.path, 100, 670, width=100, height=100)
        p.showPage()
        p.save()
        buffer.seek(0)
        file_name = f"ticket_{self.pk}.pdf"
        return File(buffer, name=file_name)