from django.conf import settings
from contact_form.forms import AkismetContactForm

class CustomRecipientContactForm(AkismetContactForm):
    recipient_list = [mail_tuple[1] for mail_tuple in getattr(settings,"CONTACT_FORM_RECIPIENTS",settings.MANAGERS)]
