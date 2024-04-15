from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField
from sorl.thumbnail import ImageField


def get_media_photo_path(instance, filename):
    return "media_photos/{0}/{1}".format(instance.media.slug)

class Language(models.Model):
    native_name = models.CharField(max_length=256)  # native
    en_name = models.CharField(max_length=256)  # in english
    # 2 letter alpha-2 code
    alpha2 = models.CharField(max_length=2, null=True, blank=True, unique=True)
    # 3 letter alpha-3 bibliographic code. it's standard language identifier at the moment.
    alpha3b = models.CharField(max_length=3, null=True, blank=True, unique=True)
    # 3 letter alpha-3 terminologic code
    alpha3t = models.CharField(max_length=3, null=True, blank=True, unique=True)
    data = models.JSONField(
        default=dict, blank=True
    )  # data such as it's translation in other languages

    def __str__(self):
        return self.get_title()

    def get_title(self):
        if self.en_name and self.native_name:
            return f"{self.en_name}({self.alpha3b}) - {self.native_name}"
        elif self.en_name:
            return f"{self.en_name}({self.alpha3b})"
        else:
            return f"{self.native_name}({self.alpha3b})"

# Tagging group name, such as genres, tags, ...
# Tags can have parents. E.g. Blues -> Chicago blues, Blues rock
class TagGroup(models.Model):
    name = models.CharField(max_length=255)
    #TODO: media type should be many to many. also "Explicit" tag group must be assigned to all media types.
    media_type = models.ForeignKey("MediaType", on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        index_together = [
            ("slug", "media_type"),
        ]

# E.g Media genres, source, etc
class Tag(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(TagGroup, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)
    slug = AutoSlugField(populate_from=['name', 'group__slug'])
    
    class Meta:
        index_together = [
            ("slug", "group"),
        ]

    def __str__(self):
        return self.name
    

# Media or Program awards
class Award(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

# Media type. E.g. Book, Movie, TV searies(or season), Music, ...
class MediaType(models.Model):
    name = models.CharField(max_length=511)
    schema = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"<MediaType>({self.name})"
    
# Base model for common information
class Media(models.Model):
    name = models.CharField(max_length=511)
    year = models.SmallIntegerField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    media_type = models.ForeignKey(MediaType, on_delete=models.SET_NULL, blank=True, null=True)
    groups = models.ManyToManyField('Group', through='MediaGroup', related_name='media_item')
    slug = AutoSlugField(populate_from=['name', 'year'])
    tags = models.ManyToManyField(Tag)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, blank=True, null=True)
    poster_image = ImageField(upload_to=get_media_photo_path, blank=True, null=True)
    awards = models.ManyToManyField(Award)
    data = models.JSONField(default=dict, blank=True, null=True)
    
    def __str__(self):
        return "{} ({})".format(self.name, self.year)

# User Rating Model
class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.SET_NULL, blank=True, null=True)
    score = models.PositiveSmallIntegerField(default=0)
    review = models.ForeignKey("Review", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - Rating: {}".format(self.media.title, self.score)


# Review Model
class Review(models.Model):
    media = models.ForeignKey(Media, on_delete=models.SET_NULL, related_name='reviews', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=511, null=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Review by {}".format(self.user.username)


# Person model (actor, director, etc.)
class Person(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


# Positions/Categories (e.g., Director, Writer)
class Position(models.Model):
    title = models.CharField(max_length=255)
    media_type = models.ForeignKey(MediaType, on_delete=models.SET_NULL, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.title


# Role in a media (e.g., Actor, Director)
class Role(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=255, null=True, blank=True)
    data = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.person.name + " as " + self.position.title


# Book series, movie universes, music albums
class GroupType(models.Model):
    name = models.CharField(max_length=255)


# E.g. "Season 2" of "The Simpsons". It's `group_type` is episod, it has a `parent` which is "The Simpsons(TV series)" 
class Group(models.Model):
    name = models.CharField(max_length=2048, unique=True)
    group_type = models.ForeignKey(GroupType, on_delete=models.SET_NULL, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)


class MediaGroup(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        unique_together = ('group', 'media')
        
    def __str__(self):
        return f'{self.order}. {self.media.name}({self.group.name})'


class RelationType(models.Model):
    name = models.CharField(max_length=2048, unique=True)
    description = models.TextField(default="")
    # relation type using descriptor and reverse_descriptor:
    # descriptor:            <media:X(Movie)>       "is an adoptation"   <media:Y(Book)>
    # reverse_descriptor:    <media:Y(Book)>    "is the basis for"    <media:X(Movie)>
    # `descriptor` is always added, `reverse_descriptor` is only used on `Directed` relationships
    DIRECTIONS = [
        ("u", "Undirected"),
        ("d", "Directed"),
    ]
    direction_type = models.CharField(max_length=1, choices=DIRECTIONS, default='u',null=True, blank=True)
    descriptor = models.CharField(max_length=2048)
    reverse_descriptor = models.CharField(max_length=2048, unique=False, blank=True)



class Relation(models.Model):
    from_media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="relation_to")
    to_media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="relation_from")
    relation_type = models.ForeignKey(RelationType, on_delete=models.CASCADE)
    