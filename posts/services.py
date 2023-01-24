from common.services import send_email
from posts.models import Post


def send_post_like_email(liked_by, post):
    subject = "You got a new Like !"
    message = f"Hey {post.user.full_name}!, You got a new like on your post from {liked_by.full_name}. \n\nPost - {post.content}"
    send_email(subject, message, to_email=[post.user.email])


def like_post(user, post):
    if Post.objects.filter(id=post.id, liked_by__id=user.id).exists():
        return

    post.liked_by.add(user)
    post.likes_count += 1
    post.save()

    # send email to post owner
    # todo: make it async
    send_post_like_email(liked_by=user, post=post)


def unlike_post(user, post):
    if Post.objects.filter(id=post.id, liked_by__id=user.id).exists():
        post.liked_by.remove(user)
        post.likes_count -= 1
        post.save()
