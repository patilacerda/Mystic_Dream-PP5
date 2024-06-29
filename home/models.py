from django.db import models


class Contact(models.Model):
    """
    Represents a contact form submission in the system.
    """
    SUBJECT_OPTIONS = (
        ('Order Inquiry', 'Order Inquiry'),
        ('Feedback', 'Feedback'),
        ('Other', 'Other'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    subject = models.CharField(
        max_length=50,
        choices=SUBJECT_OPTIONS,
        default='Other'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
