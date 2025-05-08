from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Article, Subscription

@receiver(post_save, sender=Article)
def send_article_notification(sender, instance, created, **kwargs):
    if created:
        article = instance
        category = article.category
        subscriptions = Subscription.objects.filter(category=category)
        for subscription in subscriptions:
            user = subscription.user
            if user.email:
                article_url = f"{settings.SITE_URL}/article/{article.pk}/"
                subject = f'Новая статья в {category.name}'
                text_content = (
                    f'Привет, {user.username}!\n\n'
                    f'Новая статья добавлена в категорию "{category.name}":\n'
                    f'Заголовок: {article.title}\n'
                    f'Краткое содержание: {article.content[:200]}...\n\n'
                    f'Читать дальше: {article_url}\n\n'
                    f'С уважением,\nКоманда новостей'
                )
                html_content = (
                    f'Привет, {user.username}! <br><br>'
                    f'Новая статья добавлена в категорию "{category.name}":<br>'
                    f'Заголовок: {article.title}<br>'
                    f'Краткое содержание: {article.content[:200]}...<br><br>'
                    f'Читать дальше: <a href="{article_url}">Статья</a><br><br>'
                    f'С уважением,<br>Команда новостей'
                )
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=None,
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                try:
                    msg.send()
                    print(f"Notification sent to {user.email} about article {article.title}")
                except Exception as e:
                    print(f"Failed to send notification to {user.email}: {str(e)}")