from django.shortcuts import render, get_object_or_404
from .models import Media, UserRating, Review, Person

# View for listing all media
def media_list(request):
    media_list = Media.objects.all()
    context = {
        'media_list': media_list
    }
    return render(request, 'media/media_list.html', context)

# View for detailed Media page by slug
def media_detail(request, slug):
    media = get_object_or_404(Media, slug=slug)
    context = {
        'media_list': media_list
    }
    return render(request, 'media/media_detail.html', {'media': media})

# View for adding a User Rating
def add_user_rating(request, media_id):
    user = request.user
    media = get_object_or_404(Media, pk=media_id)
    
    if request.method == 'POST':
        score = request.POST.get('score')
        review_text = request.POST.get('review', '')
        review = None

        if review_text:
            review = Review.objects.create(
                media=media,
                user=user,
                title='Review for {}'.format(media.title),
                body=review_text
            )

        UserRating.objects.create(
            user=user,
            media=media,
            score=score,
            review=review
        )

        return render(request, 'media/user_rating_added.html', {'media': media})
    context = {
        'media_list': media_list
    }
    return render(request, 'media/add_user_rating.html', {'media': media})

# View for listing all reviews for a media item
def media_reviews(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    reviews = media.reviews.all()
    context = {
        'media_list': media_list
    }
    return render(request, 'media/media_reviews.html', {'media': media, 'reviews': reviews})

# View for detailed Person page
def person_detail(request, pk):
    person = get_object_or_404(Person, pk=pk)
    context = {
        'media_list': media_list
    }
    return render(request, 'media/person_detail.html', {'person': person})

# Other views (such as Media creation, Person edit, etc.) go here

