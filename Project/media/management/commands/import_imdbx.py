from django.core.management.base import BaseCommand, CommandError
from functools import cache
from media.models import Media, MediaType, TagGroup, Tag


class Command(BaseCommand):
    help = "Download IMDB Database"

    def add_arguments(self, parser):
        # optional arguments for assuming a fresh import
        parser.add_argument("--fresh", action="store_true", help="Assume database is empty. so insert instead of update.")
        
    def handle(self, *args, **options):
        import os, csv
        from django.conf import settings
        from tqdm.auto import tqdm
        import pandas as pd
        from project.utils import get_file_lines_count

        fresh = True if options["fresh"] else False
        
        # We create titles dataframe to store the imdb_id and database ids of items.
        titles = pd.DataFrame(columns=['id'], dtype='int32')
        titles.index.name = 'imdb_index'
        titles.index = titles.index.astype(str)
        
        # Usefull if basic_import is not called
        movie, created = MediaType.objects.get_or_create(name="Movie")
        movie_explicit, created = TagGroup.objects.get_or_create(name="Explicit", media_type=movie)
        adult_tag, created = Tag.objects.get_or_create(name="Adult", group=movie_explicit)
        
        file_path = os.path.join(settings.BASE_DIR, "../Datasets/imdb/title.basics.tsv")
        rows_per_chunk = 500
        
        print("Getting dataset lenght...")
        lines = get_file_lines_count(file_path)

        with tqdm(total=lines) as pbar:
            for chunk in pd.read_csv(file_path, dtype={4:pd.Int8Dtype(), 5:pd.Int16Dtype(), 6:pd.Int16Dtype(),7:pd.Int32Dtype()}, sep='\t', encoding="utf-8", na_values=['\\N'], chunksize=rows_per_chunk, quoting=csv.QUOTE_NONE):
                for index, row in chunk.iterrows():
                    # if the database is fresh, it's best to avoid `get` function as it slows down the process.
                    def create_fresh_media(row):
                        media = Media(name=row['titleType'], year=row['startYear']) if pd.notnull(row['startYear']) else Media(name=row['titleType'])
                        media.data = {}
                        media.data['id'] = {}
                        media.data['id']['imdb'] = row['tconst']
                        return media

                    if fresh:
                        media = create_fresh_media(row)
                    else:
                        try:
                            media = Media.objects.get(data__id__imdb=row[0]) # if media exists, then update it
                        except Media.DoesNotExist:
                            media = create_fresh_media(row)
                    
                    media.media_type = self.get_media_type_object(row['titleType'])
                    media.name = row['primaryTitle']
                    if media.data is None: media.data = {}
                    if 'titles' not in media.data: media.data['titles'] = {}
                    media.data['titles']['original'] = row['originalTitle']
                    if pd.notnull(row['startYear']): media.year = row['startYear']
                    if 'dates' not in media.data: media.data['dates'] = {}
                    if pd.notnull(row['startYear']): media.data['dates']['start_year'] = row['startYear']
                    if pd.notnull(row['endYear']): media.data['dates']['end_year'] = row['endYear']
                    if pd.notnull(row['runtimeMinutes']): media.data['dates']['run_time_min'] = row['runtimeMinutes']
                    media.save()
                    
                    # used as a cache to map imdb and database ids
                    titles.loc[row['tconst']] = media.id
                     
                    if row['isAdult']==1:
                        media.tags.add(adult_tag)
                    if pd.notnull(row['genres']):
                        for tag in row['genres'].split(','):
                            tag_obj = self.get_media_tag(tag, media.media_type)
                            media.tags.add(tag_obj)

                    pbar.update(1)
                
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
    def get_media_tag(self, key, media_type):
        genre_group, created = TagGroup.objects.get_or_create(name="Genre", media_type=media_type)
        genre, created = Tag.objects.get_or_create(name=key, group=genre_group)
        return genre