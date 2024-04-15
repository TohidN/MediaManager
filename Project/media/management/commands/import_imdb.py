from django.core.management.base import BaseCommand, CommandError
from functools import cache
from media.models import Media, MediaType, TagGroup, Tag

class Command(BaseCommand):
    help = "Download IMDB Database"

    def add_arguments(self, parser):
        # optional arguments for assuming a fresh import
        parser.add_argument("--fresh", action="store_true", help="Assume database is empty. so insert instead of upload.")

        
    def handle(self, *args, **options):
        import os, csv
        from django.conf import settings
        from tqdm.auto import tqdm
        from project.utils import get_file_lines_count

        fresh = True if options["fresh"] else False
                       
        file_path = os.path.join(settings.BASE_DIR, "../Datasets/imdb/title.basics.tsv")
        with open(file_path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter="\t", quoting=csv.QUOTE_NONE) # some titles start with quote marke which makes `primaryTitle` and `originalTitle` to be merged
            next(reader, None) # Skip header
            
            # Usefull if basic_import is not called
            movie, created = MediaType.objects.get_or_create(name="Movie")
            movie_explicit, created = TagGroup.objects.get_or_create(name="Explicit", media_type=movie)
            adult_tag, created = Tag.objects.get_or_create(name="Adult", group=movie_explicit)

            print("Getting dataset lenght...")
            lines = get_file_lines_count(file_path)
            for row in tqdm(reader, total=lines):
                # if the database is fresh, it's best to avoid `get` function as it slows down the process.
                def create_fresh_media(row):
                    media = Media(name=row[2], year=int(row[5]) if row[5]!='\\N' else None)
                    media.data = {}
                    media.data['id'] = {}
                    media.data['id']['imdb'] = row[0]
                    return media

                if fresh:
                    media = create_fresh_media(row)
                else:
                    try:
                        media = Media.objects.get(data__id__imdb=row[0]) # if media exists, then update it
                    except Media.DoesNotExist:
                        media = create_fresh_media(row)
                
                media.media_type = self.get_media_type_object(row[1])
                media.name = row[2]
                if media.data is None: media.data = {}
                if 'titles' not in media.data: media.data['titles'] = {}
                media.data['titles']['original'] = row[3]
                media.year = int(row[5]) if row[5]!='\\N' else None
                if 'dates' not in media.data: media.data['dates'] = {}
                if row[6] != "\\N": media.data['dates']['start_year'] = int(row[5])
                if row[6] != "\\N": media.data['dates']['end_year'] = int(row[6])
                if row[7] != "\\N": media.data['dates']['run_time_min'] = int(row[7])
                media.save()
                if row[4]=="1": media.tags.add(adult_tag)
                for tag in row[8].split(','):
                    tag_obj = self.get_media_tag(tag)
                    media.tags.add(tag_obj)
                
                
    @cache
    def get_media_type_object(self, key):
        media_type_data = {
            'short': 'Short Movie',
            'movie': 'Movie',
            'tvShort': 'TV Short',
            'tvMovie': 'Movie',
            'tvSeries': 'Series',
            'tvEpisode': 'Episode',
            'tvMiniSeries': 'Mini Series',
            'tvSpecial': 'TV Special',
            'video': 'Video',
            'videoGame': 'Video Game',
            'tvPilot': 'Series Pilot'
        }
        media_type_name = media_type_data[key] if key in media_type_data else key
        media_type, created = MediaType.objects.get_or_create(name=media_type_name)
        return media_type

    @cache
    def get_media_tag(self, key):
        movie, created = MediaType.objects.get_or_create(name="Movie")
        movie_genre_group, created = TagGroup.objects.get_or_create(name="Genre", media_type=movie)
        movie_genre, created = Tag.objects.get_or_create(name=key, group=movie_genre_group)
        return movie_genre