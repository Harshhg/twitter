from posts.models import Post


def like_post(user, post):
    if Post.objects.filter(id=post.id, liked_by__id=user.id).exists():
        return

    post.liked_by.add(user)
    post.likes_count += 1
    post.save()
