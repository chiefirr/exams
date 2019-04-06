# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from exams import settings
#
# User = get_user_model()
#
# @receiver(post_save, sender=User)
# def user_post_save(sender, **kwargs):
#     """
#     Create a Profile instance for all newly created User instances. We only
#     run on user creation to avoid having to check for existence on each call
#     to User.save.
#     """
#     user, created = kwargs["instance"], kwargs["created"]
#     if created and user.username != settings.ANONYMOUS_USER_NAME:
#         from import Profile
#         profile = Profile.objects.create(pk=user.pk, user=user, creator=user)
#         assign_perm("change_user", user, user)
#         assign_perm("change_profile", user, profile)
