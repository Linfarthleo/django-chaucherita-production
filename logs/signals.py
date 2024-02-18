from django.utils import timezone
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import SessionLog

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    session_log = SessionLog.objects.using('logsdb').create(user_id=user.id, user_username=user.username)
    session_log.save()

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    last_session_log = SessionLog.objects.using('logsdb').filter(user_id=user.id).latest('login_time')
    last_session_log.logout_time = timezone.now()
    last_session_log.save()
