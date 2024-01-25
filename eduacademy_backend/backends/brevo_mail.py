from django.core.mail.backends.base import BaseEmailBackend
from accounts.models import User

import sib_api_v3_sdk

import os
from dotenv import load_dotenv
load_dotenv()

class EmailBackend(BaseEmailBackend):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    sender = {"name": "EDUAcademy", "email": "no-reply@eduacademy.com"}
    template_mapper = {
        'Please Confirm Your Email Address': 2,
        'Password Reset Email': 4,
    }

    def map_params_to_subject(self, email):
        subject = email.subject

        links1 = email.body.split(' ')
        links = list()
        for i in links1:
            links.extend(i.split('\n'))
        for i in links:
            if i.startswith('http://') or i.startswith('https://'):
                link = i
                break

        params = {
            "FNAME": User.objects.get(email=email.recipients()[0]).first_name,
            "link": link,
        }

        to_return = None
        for key, value in self.template_mapper.items():
            if key in subject:
                to_return = (value, params)
                break
        return to_return

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        for email in email_messages:
            try: template_id, params = self.map_params_to_subject(email)
            except: return {"message": "No Emails were sent."}
            
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{'email': r} for r in email.recipients()],
                sender=self.sender,
                template_id=template_id,
                params=params,
            )

            self.api_instance.send_transac_email(send_smtp_email)
        return {"message": "Emails sent successfully!"}