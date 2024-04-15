from django.core.management.base import BaseCommand, CommandError
from media.models import Media


class Command(BaseCommand):
    help = "Download IMDB Database"

    def handle(self, *args, **options):
        import os, csv
        from django.conf import settings
        from tqdm.auto import tqdm
        
        # Download & Extract dataset if it doens't exist
        def get_dataset(url, dir_path, file):
            import gzip, shutil
            from project.utils import download, get_or_create_dir
            
            file_path = os.path.join(dir_path, file)
            extracted_file, extracted_file_path = file[:-3], file_path[:-3]
            # Setup Dataset Directory
            if not os.path.exists(dir_path):
                    get_or_create_dir(dir_path)
            # Download compressed
            if not os.path.isfile(file_path):
                if os.path.exists(extracted_file_path):
                    print(f"Extracted version of file(`{extracted_file}`) already exists, skipping to next download.")
                else:
                    download(url, file_path)
            else:
                print(f"file `{file}` already exists, skipping to next download.")
            # Extract Compressed
            if not os.path.isfile(extracted_file_path):
                print(f"Extracting `{file}` into `{extracted_file}.")
                with gzip.open(file_path, 'rb') as f_in:
                    with open(extracted_file_path, 'wb') as f_out: # -4 removes `.gz` from end of file
                        shutil.copyfileobj(f_in, f_out)
            else:
                print(f"file `{extracted_file_path}` already exists, skipping to next.")

                
        
        url = "https://datasets.imdbws.com/"
        dir_path = os.path.abspath(os.path.join(settings.BASE_DIR, "../Datasets/IMDB/"))
        files = ["title.ratings.tsv.gz", "title.basics.tsv.gz", "name.basics.tsv.gz", "title.akas.tsv.gz", "title.crew.tsv.gz", "title.episode.tsv.gz", "title.principals.tsv.gz"]
        for file in files:
            get_dataset(f"{url}{file}", dir_path, file)
