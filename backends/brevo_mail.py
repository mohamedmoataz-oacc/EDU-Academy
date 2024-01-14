from django.core.mail.backends.base import BaseEmailBackend
import sib_api_v3_sdk

import os
from dotenv import load_dotenv
load_dotenv()

class EmailBackend(BaseEmailBackend):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        sender = {"name": "EDUAcademy", "email": "no-reply@eduacademy.com"}

        for email in email_messages:
            subject = email.subject
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{'email': r} for r in email.recipients()],
                html_content=email.body,
                sender=sender,
                subject=subject
            )

            self.api_instance.send_transac_email(send_smtp_email)
        return {"message": "Emails sent successfully!"}