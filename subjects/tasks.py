from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_rq import job
from markdown import markdown
from weasyprint import HTML

from main.settings import CERTIFICATE_DIR, EMAIL_DEFAULT_FROM, EMAIL_HOST_USER


@job
def deliver_certificate(base_url, student):
    path_to_cert = f'{CERTIFICATE_DIR}/{student.username}_grade_certificate.pdf'
    render = render_to_string('certificates/certificate.html', {'student': student})
    HTML(string=render, base_url=base_url).write_pdf(path_to_cert)

    render = render_to_string('certificates/mail_cert.md')
    mail = markdown(render)

    email = EmailMessage(
        subject='Your certificate is ready!',
        body=mail,
        to=[student.email],
        from_email=EMAIL_HOST_USER,
        reply_to=[EMAIL_DEFAULT_FROM],
    )
    email.attach_file(path_to_cert)
    email.send()
