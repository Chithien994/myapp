import os
import shutil

from io import BytesIO
from random import randint

import xhtml2pdf.pisa as pisa
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template

def generate_pdf(html, context):
    file_name = "report-{0}-{1}.pdf".format(
        context['phone_number'], randint(1, 1000000))
    file_path = os.path.join(settings.STATIC_ROOT, file_name)
    with open(file_path, 'wb') as pdf:
        pisa.pisaDocument(BytesIO(html.encode('utf-8')),
                          pdf, encoding='utf-8')
    return file_path

def send_report(template_src='polls/pdf.html', context={}):
    template = get_template(template_src)
    html = template.render(context)
    file_path = generate_pdf(html, context)

    send_mail(file_path, context['email_address'])
    remove_file(file_path)

    response = BytesIO()
    pisa.pisaDocument(BytesIO(html.encode(
        'UTF-8')), response, path=settings.PROJECT_ROOT, encoding='UTF-8')
    return HttpResponse(response.getvalue(), content_type='application/pdf')


def get_data_for_pdf(administrator, question, email_address):
    context = {
        'email_address': email_address,
        'phone_number': administrator.phone_number,
        'questions': question
    }
    return context

def remove_file(file_path):
    try:
        shutil.rmtree(file_path)
    except:
        pass
    try:
        os.remove(file_path)
    except Exception as e:
        raise

def send_mail(file_path, to_email):
    from django.core.mail import EmailMessage

    message = EmailMessage(
        'Your report for all questions',
        'Your report for all questions',
        settings.DEFAULT_FROM_EMAIL,
        [to_email]
    )
    message.attach_file(file_path)
    message.send()