from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import escape
from .forms import ContactForm


def contact_view(request):
    """
    View for the contact page.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the message to database
            contact_message = form.save(commit=False)
            contact_message.save()

            safe_name = escape(contact_message.name)

            messages.success(
                request,
                f'Thank you {safe_name}! Your message has been sent successfully. '
                'We will get back to you soon.'
            )

            # Clear form by redirecting
            return redirect('contact')
        else:
            messages.error(
                request,
                'Please check your form. There are errors.'
            )
    else:
        form = ContactForm()

    # Render the contact page with form
    context = {
        'form': form,
    }
    return render(request, 'contact/contact.html', context)