from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the message to database
            contact_message = form.save()
            
            # Send email notification to admin
            try:
                send_mail(
                    f'New Contact Message: {contact_message.subject}',
                    f"""
                    You have received a new message from {contact_message.name} ({contact_message.email}):
                    
                    Subject: {contact_message.subject}
                    Message: {contact_message.message}
                    
                    Received: {contact_message.created_on}
                    """,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],  # Send to yourself for now
                    fail_silently=True,  # Change to True to prevent errors if email fails
                )
                
                # Send confirmation email to user
                send_mail(
                    'Thank you for contacting AddisTalk',
                    f"""
                    Dear {contact_message.name},
                    
                    Thank you for contacting AddisTalk. We have received your message and will get back to you soon.
                    
                    Your message:
                    Subject: {contact_message.subject}
                    
                    We appreciate your feedback and will respond within 24-48 hours.
                    
                    Best regards,
                    AddisTalk Team
                    """,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_message.email],
                    fail_silently=True,
                )
                
                messages.success(request, 'Your message has been sent successfully! We will contact you soon.')
            except Exception as e:
                # Still save the message even if email fails
                messages.success(request, 'Your message has been received!')
            
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})


# Optional: Admin message list view
def message_list(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    messages_list = ContactMessage.objects.all().order_by('-created_on')
    return render(request, 'contact/message_list.html', {'messages': messages_list})