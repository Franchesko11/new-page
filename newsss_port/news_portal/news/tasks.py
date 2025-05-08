from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Subscription, Article
from datetime import timedelta
from django.utils import timezone


@shared_task
def send_weekly_digest():

    now = timezone.now()
    last_week = now - timedelta(days=7)


    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        user = subscription.user
        category = subscription.category

        new_articles = Article.objects.filter(
            category=category,
            created_at__gte=last_week,
            created_at__lte=now
        )
        if new_articles and user.email:
            subject = f'Еженедельный дайджест: Новые статьи в {category.name}'
            text_content = f'Привет, {user.username}!\n\nВот новые статьи в "{category.name}" за последнюю неделю:\n\n'
            html_content = f'Привет, {user.username}! <br><br>Вот новые статьи в "{category.name}" за последнюю неделю:<br><br>'
            for article in new_articles:
                article_url = f"{settings.SITE_URL}/article/{article.pk}/"
                text_content += f'- {article.title}: {article.content[:100]}... Читать дальше: {article_url}\n'
                html_content += f'- <a href="{article_url}">{article.title}</a>: {article.content[:100]}...<br>'
            text_content += '\nС уважением,\nКоманда новостей'
            html_content += '<br><br>С уважением,<br>Команда новостей'
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=None,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
                print(f"Weekly digest sent to {user.email} for category {category.name}")
            except Exception as e:
                print(f"Failed to send weekly digest to {user.email}: {str(e)}")