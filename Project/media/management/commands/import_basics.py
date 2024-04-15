from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Import IMDB Database"

    def handle(self, *args, **options):
        import os
        from django.conf import settings

        import json
        import pandas as pd
        from tqdm.auto import tqdm
        from media.models import MediaType, TagGroup, Tag, Language, Position, GroupType
        
        #TODO: for now data is stored in code, move them to raw text files and read from file
        
        # Set initial Media Types
        book, created = MediaType.objects.get_or_create(name="Book")
        magazine, created = MediaType.objects.get_or_create(name="Magazine")
        music, created = MediaType.objects.get_or_create(name="Music")
        music_video, created = MediaType.objects.get_or_create(name="Music Video")
        movie, created = MediaType.objects.get_or_create(name="Movie")
        movie_short, created = MediaType.objects.get_or_create(name="Short Movie")
        series, created = MediaType.objects.get_or_create(name="Series")
        mini_series, created = MediaType.objects.get_or_create(name="Mini Series")
        tv_short, created = MediaType.objects.get_or_create(name="TV Short")
        episode, created = MediaType.objects.get_or_create(name="Episode")
        tv_special, created = MediaType.objects.get_or_create(name="TV Special")
        series_pilot, created = MediaType.objects.get_or_create(name="Series Pilot")
        video, created = MediaType.objects.get_or_create(name="Video")
        video_game, created = MediaType.objects.get_or_create(name="Video Game")
        
        
        
        def add_positions(media_type, position_list, desc=""):        
            for item in tqdm(position_list, total=len(position_list), desc=desc):
                position, created = Position.objects.get_or_create(title=item, media_type=media_type)

        # Setup positions
        book_positions = ["Author", "Editor", "Literary Agent", "Publisher", "Acquisitions Editor", "Developmental Editor", "Copy Editor", "Proofreader", "Book Designer", "Cover Designer", "Illustrator", "Transcriber", "Ghostwriter", "Publicist", "Marketing Manager", "Sales Representative", "Distributor", "Printer", "Typesetter", "Indexer", "Copyright Specialist", "Permissions Editor", "Ebook Producer", "Audio Book Producer", "Literary Scout", "Translator", "Reviewers/Critics", "Content Strategist", "Digital Marketing Specialist", "Metadata Specialist", "Foreign Rights Manager", "Production Coordinator", "Literary Publicist", "Narrator", "Audio Recording Engineer"]
        add_positions(book, book_positions, desc="Importing Book Positions")

        magazine_positions = ["Editor-in-Chief", "Managing Editor", "Associate Editor", "Assistant Editor", "Content Editor", "Art Director", "Graphic Designer", "Photo Editor", "Layout Designer", "Copy Editor", "Proofreader", "Production Manager", "Circulation Manager", "Advertising Manager", "Marketing Manager", "Public Relations Manager", "Web Editor", "Social Media Manager", "Contributing Writer", "Freelance Photographer", "Illustrator", "Researcher", "Magazine Publisher", "Print Production Manager", "Digital Production Manager", "Subscription Manager", "Media Buyer", "Creative Director", "Brand Manager", "Events Coordinator", "Sponsorship Coordinator", "Distribution Manager", "Advertising Sales Representative", "Publications Coordinator", "Digital Content Manager", "Print and Digital Circulation Coordinator", "Editorial Assistant", "Feature Writer", "Columnist", "Photojournalist", "Web Content Editor", "Video Editor", "Printing Specialist", "Subscription Administrator", "Social Media Coordinator", "Brand Marketing Manager", "Events Marketing Manager", "Content Strategist", "Email Marketing Coordinator", "Market Research Analyst", "Production Artist", "Magazine Distributor", "Media Planner", "Magazine Accountant", "Magazine Archivist", "Magazine Librarian", "Online Community Manager", "SEO Specialist", "E-commerce Manager"]
        add_positions(magazine, magazine_positions, desc="Importing Magazine Positions")
        
        music_positions = ["Music Producer", "Recording Engineer", "Mixing Engineer", "Mastering Engineer", "Songwriter", "Composer", "Arranger", "Session Musician", "Vocalist", "Beat Maker", "Sound Designer", "Studio Manager", "Music Director", "A&R (Artist and Repertoire) Coordinator", "Music Supervisor", "Music Editor", "Scoring Mixer", "Foley Artist", "Music Copyist", "Music Contractor", "Music Business Manager", "Music Publisher", "Publicist", "Booking Agent", "Concert Promoter", "Merchandise Manager" "Stage Manager", "Orchestrator", "Instrument Technician", "Location Sound Recordist", "Remix Artist", "Synthesizer Programmer", "Backing Vocalist", "Hip-Hop Producer", "Classical Music Producer", "Electronic Music Producer", "Social Media Manager", "Digital Marketing Specialist", "Music Video Director", "Music Video Producer", "Tour Manager", "Concert Sound Engineer", "Concert Lighting Designer", "Concert Stage Crew", "Music Retail Manager", "Music Photographer", "Voice Coach"]
        add_positions(music, music_positions, desc="Importing Music Positions")
        
        movie_positions = ["Director", "Producer", "Screenwriter", "Cinematographer", "Production Designer", "Costume Designer", "Film Editor", "Composer", "Sound Designer", "Visual Effects Supervisor", "Art Director", "Set Decorator", "Assistant Director", "Script Supervisor", "Location Manager", "Casting Director", "Stunt Coordinator", "Makeup Artist", "Gaffer", "Key Grip", "Production Assistant", "Unit Production Manager", "Sound Mixer", "Boom Operator", "Special Effects Supervisor", "Storyboard Artist", "Choreographer", "Fight Choreographer", "Dialogue Coach", "Animal Wrangler", "Colorist", "Dialect Coach", "Foley Artist", "Location Scout", "Post-production Supervisor", "Production Sound Mixer", "Visual Effects Artist", "Weapons Master", "Craft Service", "Digital Imaging Technician", "Production Accountant", "Key Hair Stylist", "Key Makeup Artist", "Rigging Gaffer", "Rigging Grip", "Scenic Artist", "Second Unit Director", "Sound Re-recording Mixer", "VFX Editor", "Assistant Costume Designer", "Animal Trainer", "Carpenter", "Dialogue Editor", "Dolly Grip", "Graphic Designer", "Hairstylist", "Key Production Assistant", "Negative Cutter", "Property Master", "Set Designer", "Special Effects Coordinator", "Stand-in", "Title Designer", "Unit Publicist", "Wardrobe Supervisor", "Assistant Art Director", "Assistant Location Manager", "Digital Intermediate Colorist", "Greensman", "Leadman", "Loader", "Picture Car Coordinator", "Production Coordinator", "Scenic Artist", "Set Dresser", "Silent Playback Operator"]
        add_positions(movie, movie_positions, desc="Importing Movie Positions")
        
        series_positions = ["Showrunner", "Producer", "Executive Producer", "Co-Producer", "Associate Producer", "Production Coordinator", "Production Manager", "Script Supervisor", "Writer", "Director", "Assistant Director", "Cinematographer", "Camera Operator", "Gaffer", "Key Grip", "Sound Mixer", "Boom Operator", "Costume Designer", "Makeup Artist", "Hair Stylist", "Production Designer", "Art Director", "Set Decorator", "Props Master", "Special Effects Supervisor", "Visual Effects Supervisor", "Editor", "Composer", "Post-production Supervisor", "Colorist", "Casting Director", "Location Manager", "Stunt Coordinator", "Unit Production Manager", "Publicist", "Assistant Editor", "VFX Artist", "Storyboard Artist", "Choreographer", "Fight Choreographer", "Dialogue Coach", "Dialect Coach", "Animal Coordinator", "Title Designer", "Graphic Designer", "Studio Teacher", "Script Coordinator", "Production Accountant", "Set Medic", "Craft Service", "Script Reader", "Assistant Location Manager", "Foley Artist", "Sound Designer", "ADR Mixer", "Music Supervisor", "Sound Effects Editor", "Re-recording Mixer", "ADR Mixer", "ADR Editor", "Sound Recordist", "Carpenter", "Painter", "Key Scenic Artist", "Dresser", "Makeup Effects Artist", "Set Dresser", "On-Set Dresser", "Leadman", "Greensman", "Construction Coordinator", "Construction Foreman", "Rigging Grip", "Best Boy Grip", "Digital Imaging Technician", "Script Department Coordinator", "Transportation Coordinator", "Location Scout", "Assistant Location Manager", "Production Assistant", "Assistant Production Coordinator", "Production Secretary", "Office Production Assistant", "Travel Coordinator", "Key Set Production Assistant", "Set Production Assistant", "Camera Production Assistant", "Art Department Production Assistant", "Post-Production Assistant", "Script Coordinator", "Assistant Script Coordinator", "Assistant to Executive Producer", "Extras Casting Assistant", "Security Coordinator"]
        add_positions(series, movie_positions, desc="Importing Series Positions")
        
        #TODO: add prodicals such as newspapers and journals, with tag types such as field of interest, and location
        # Set initial Tag Groups
        tag, created = TagGroup.objects.get_or_create(name="Tag", media_type=book)
        book_genre, created = TagGroup.objects.get_or_create(name="Genre", media_type=book)
        book_type, created = TagGroup.objects.get_or_create(name="Type", media_type=book) # book, comics, webnovels, ...
        
        tag, created = TagGroup.objects.get_or_create(name="Tag", media_type=magazine)
        magazine_genre, created = TagGroup.objects.get_or_create(name="Genre", media_type=magazine)
        magazine_type, created = TagGroup.objects.get_or_create(name="Type", media_type=magazine) # book, comics, webnovels, ...
        magazine_periodical, created = TagGroup.objects.get_or_create(name="Periodical", media_type=magazine) # book, comics, webnovels, ...
        
        tag, created = TagGroup.objects.get_or_create(name="Tag", media_type=movie)
        movie_genre, created = TagGroup.objects.get_or_create(name="Genre", media_type=movie)
        movie_explicit, created = TagGroup.objects.get_or_create(name="Explicit", media_type=movie)

        tag, created = TagGroup.objects.get_or_create(name="Tag", media_type=music)
        music_genre, created = TagGroup.objects.get_or_create(name="Genre", media_type=music)
        tag, created = TagGroup.objects.get_or_create(name="Song Language", media_type=music)
        tag, created = TagGroup.objects.get_or_create(name="Style", media_type=music)

        tag, created = TagGroup.objects.get_or_create(name="Tag", media_type=series)
        series_genre, created = TagGroup.objects.get_or_create(name="Genre", media_type=series)
        tag, created = TagGroup.objects.get_or_create(name="Tag", media_type=episode)
        
        # Add group types
        group_type = ["Shared Universe", "Expanded Universe/Extended Universe", "Cinematic Universe", "Franchise", "Adaptations", "Trilogies", "Movie Series", "Book Series", "Discography", "Anthology Series", "Spin-offs", "Crossover Events", "Collaborative Projects", "Reboots/Revivals", "Shared Themes or Motifs", "Coordinated Releases "]
        group_List = [GroupType(name=val) for val in group_type]
        GroupType.objects.bulk_create(group_List)

        # Add tag types and common tags
        def add_tags(tag_group, item_list, desc=""):
            for item in tqdm(item_list, total=len(item_list), desc=desc):
                tag, created = Tag.objects.get_or_create(name=item, group=tag_group)
                
        # Book genres & Types
        book_genre_list = ["Science Fiction", "Fantasy", "Mystery", "Thriller", "Romance", "Historical Fiction", "Literary Fiction", "Young Adult", "Children's", "Horror", "Nonfiction", "Biography", "Autobiography", "Self-help", "Cookbooks", "Travel", "Science", "Poetry", "Drama", "Satire", "Action and Adventure", "Short Stories", "Fairy Tales", "Western", "Dystopian", "Crime", "Humor", "Health", "Fitness", "Spirituality", "Religion", "Philosophy", "Art", "Photography", "Music", "History", "Politics", "Economics", "Business", "Finance", "Computer Science", "Technology", "Engineering", "Mathematics", "Psychology", "Sociology", "Anthropology", "Educational", "Reference", "DIY", "Crafts", "Gardening", "Sports", "Outdoor", "Cooking", "Baking", "Diet", "Nutrition", "Parenting", "Family", "Relationships", "Pets", "Games", "Puzzles", "Hobbies", "Futurism", "Urban Fantasy"]
        book_types_list = ["Graphic Novel", "Comic Book", "Manga", "AudioBook"]
        add_tags(book_genre, book_genre_list, desc="Importing Book Genres")
        add_tags(book_type, book_types_list, desc="Importing Book Types")

        # Magazines
        magazine_genres = ["Fashion", "Lifestyle", "News", "Entertainment", "Home and Garden", "Health and Fitness", "Travel", "Technology", "Science", "Automotive", "Sports", "Business", "Finance", "Cooking and Food", "Crafts and Hobbies", "Art and Design", "Parenting", "Men's Interest", "Women's Interest", "Teen", "Nature and Outdoors", "Photography", "Gaming", "Literary", "Music", "Political", "Educational", "Cultural", "Religious", "Opinion"]
        magazine_types = ["Print Magazines", "Digital Magazines", "Consumer Magazines", "Trade Magazines", "Special Interest Magazines", "Newspaper Magazines", "Custom Magazines", "Newsletter Magazines", "Scholarly and Academic Journals", "Sensational Magazines", "E-zines (Online Magazines)"]
        magazine_periodicals = ["daily", "Weekly", "Monthly", "Quarterly", "annually"]
        add_tags(magazine_genre, magazine_genres, desc="Importing Magazine Genres")
        add_tags(magazine_type, magazine_types, desc="Importing Magazine Types")
        add_tags(magazine_periodical, magazine_periodicals, desc="Importing Magazine Periodicals")
        
        # Movie  
        movie_genres = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Thriller", "Animation", "Biography", "Crime", "Documentary", "Family", "History", "Music", "Musical", "Romance", "Sci-Fi", "Sport", "War", "Western"]
        movie_explicit_list = ["Adult", "Profanity", "Gore"]
        add_tags(movie_genre, movie_genres, desc="Importing Movie Genres")
        add_tags(movie_explicit, movie_explicit_list, desc="Importing Movie Explicit Tags")
        
        movie_explicit
        # TV Series
        tv_series_genres = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Thriller", "Science Fiction", "Crime", "Historical", "Romance", "Animation", "Documentary", "Musical", "Supernatural", "Family", "Reality", "Suspense", "Western", "War", "Superhero", "Medical", "Legal", "Espionage", "Spy", "Teen", "Sitcom"]
        add_tags(series_genre, tv_series_genres, desc="Importing Series Genres")

        # Music genres and sub-genres - JSON variable
        music_genres_json = '''
        {
        "Avant-garde & Experimental": ["Crossover music", "Danger music", "Drone music", "Electroacoustic", "Industrial music", "Instrumental", "Lo-fi", "Musical improvisation", "Musique concrète", "Noise", "Outsider music", "PC Music", "Progressive music", "Psychedelic music", "Underground music"],
        "Blues": ["African blues", "Blues rock", "Blues shouter", "British blues", "Canadian blues", "Chicago blues", "Classic female blues", "Contemporary R&B", "Country blues", "Delta blues", "Desert blues", "Detroit blues", "Electric blues", "Gospel blues", "Hill country blues", "Hokum blues", "Honky Tonk Blues", "Jump blues", "Kansas City blues", "Louisiana blues", "Memphis blues", "New Orleans blues", "Piedmont blues", "Punk blues", "Rhythm and blues", "Soul blues", "St. Louis blues", "Swamp blues", "Talking blues", "Texas blues", "West Coast blues"],
        "Country": ["Alternative country", "Americana", "Australian country", "Bakersfield sound", "Bluegrass", "Classic country", "Country blues", "Country pop", "Country rap", "Country rock", "Cajun", "Christian country", "Close harmony", "Dansband", "Gothic country", "Hokum", "Honky-tonk country", "Instrumental country", "Nashville sound", "Neotraditional country", "New Mexico music", "Outlaw country", "Progressive country", "Red dirt", "Rockabilly", "Sertanejo", "Tejano", "Texas country", "Traditional country music", "Truck-driving country", "Western (Cowboy)", "Western swing", "Zydeco"],
        "Easy Listening": ["Adult contemporary music", "Adult standards", "Background music", "Barococo", "Beautiful music", "Chill-out", "Downtempo", "Furniture music", "Light music", "Lounge music", "Middle of the road", "New-age music", "Soft rock"],
        "Electronic": ["Ambient", "Bass music", "Breakbeat", "Chill-out", "Chopped and screwed", "Disco", "Drum and bass", "Dub", "Electroacoustic music", "Electronic dance music", "Electronic rock", "Electronica", "Ethnic electronica / regional EDM", "Funk fusion genres", "Jungle", "Hardcore", "Hardstyle", "Hauntology", "Hip hop fusion genres", "House music", "Industrial / post-industrial", "Intelligent dance music (IDM)", "Neo soulNightcoreNoise music", "Plunderphonics", "Techno", "Tecno bregaTrance music", "UK garage", "Video game music"],
        "Folk": ["American folk revival", "Americana", "Anti-folk", "British folk revival", "Cajun music", "Celtic music", "Chalga", "Corrido", "Creole music", "Filk", "Folk noir", "Folk rock", "Folktronica", "Freak folk", "Indie folk", "Industrial folk", "Mariachi", "Neofolk", "New Weird America", "Progressive folk", "Protest song", "Psychedelic folk", "Singer-songwriter", "Skiffle", "Sung poetry", "Tarantella/Pizzica", "Traditional blues verses"],
        "Hip Hop": ["Alternative hip hop" , "Beatboxing" , "Boom bap" , "Bounce" , "British hip hop" , "Chopped and screwed" , "Chopper" , "Classic hip hop" , "Cloud rap" , "Comedy hip hop" , "Crunk" , "Country rap" , "East Coast hip hop" , "Emo rap" , "Freestyle rap" , "G-funk" , "Hardcore hip hop" , "Hip hop soul" , "Hyphy" , "Industrial hip hop" , "Instrumental hip hop" , "Jazz rap" , "Latin hip hop" , "Lofi hip hop" , "Miami bass" , "Mumble rap" , "Nerdcore" , "New jack swing" , "Political hip hop" , "Pop rap" , "Progressive rap" , "Punk rap" , "Rap opera" , "Rap rock" , "Christian hip hop" , "Jewish hip hop" , "Snap" , "Southern hip hop" , "Trap" , "Turntablism" , "Underground hip hop" , "West Coast hip hop" ],
        "Jazz": ["Acid jazz", "Afro-Cuban jazz", "Alt-jazz", "Avant-garde jazz", "Bebop", "Big band", "Boogie-woogie", "Bossa nova", "Brazilian Jazz", "British dance band", "Cape jazz", "Chamber jazz", "Continental jazz", "Cool jazz", "Crossover jazz", "Dixieland", "Ethno jazz", "European free jazz", "Free funk", "Free improvisation", "Free jazz", "Gypsy jazz", "Hard bop", "Jazz blues", "Jazz-funk", "Jazz fusion", "Jazz noir", "Jazz rap", "Jazz rock", "Jazztronica", "Kansas City jazz", "Latin jazz", "Livetronica", "M-base", "Mainstream jazz", "Modal jazz", "Neo-bop jazz", "Neo-swing", "Nu jazz", "Orchestral jazz", "Post-bop", "Progressive jazz", "Punk jazz", "Samba-jazz", "Shibuya-kei", "Ska jazz", "Smooth jazz", "Soul jazz", "Straight-ahead jazz", "Stride jazz", "Swing", "Trad jazz", "Third stream", "Vocal jazz", "West Coast jazz"],
        "Pop": ["Adultcontemporary", "Adulthits", "Ambientpop", "Arabicpopmusic", "Artpop", "Avant-pop", "Baroquepop", "Beachmusic", "Bedroompop", "Brillbuilding", "Britpop", "Bubblegumpop", "C-pop", "Canción", "Canzone", "Chalga", "Chamberpop", "Chanson", "Christianpop", "Classichits", "Classicalcrossover", "Contemporaryhitradio", "Countrypop", "Cringepop", "Dance-pop", "Darkpop", "Discopolo", "Electropop", "Europop", "Fado", "Folkpop", "Hyperpop", "Indiepop", "Indianpop", "Iranianpop", "J-pop", "Janglepop", "Jazzpop", "K-pop", "Latinballad", "Latinpop", "NewPop", "NewRomantic", "Rhythmicoldies", "Operaticpop", "OPM", "Poprap", "Poprock", "Popsoul", "Progressivepop", "Psychedelicpop", "Rebetiko", "Rhythmicadultcontemporary", "Rhythmiccontemporary", "Schlager", "Sophisti-pop", "Spaceagepop", "Sunshinepop", "Swamppop", "Synth-pop", "Teenpop", "Traditionalpop", "Turbo-folk", "Turkishpop", "Urbanadultcontemporary", "Urbancontemporarymusic", "Vispop", "Wonkypop", "Worldbeat", "Yé-yé"],
        "R&B & Soul": ["Alternative R&B" , "Contemporary R&B" , "Disco" , "Freestyle" , "Funk" , "Gospel music" , "New jack swing" , "Post-disco" , "Rhythm and blues" , "Soul"],
        "Rock": ["Active rock", "Adult album alternative", "Adult-oriented rock", "Afro rock", "Album oriented rock", "Alternative rock", "American rock", "Anatolian rock", "Arabic rock", "Arena rock", "Beat", "Blues rock", "Brazilian rock", "British rhythm and blues", "British rock music", "Chamber pop", "Chinese rock", "Christian rock", "Classic alternative", "Classic rock", "Comedy rock", "Country rock", "Dark cabaret", "Death 'n' roll", "Deathrock", "Desert rock", "Electronic rock", "Emo", "Experimental rock", "Folk rock", "Funk rock", "Garage rock", "Geek rock", "Glam rock", "Gothic rock", "Hard rock", "Heartland rock", "Heavy metal music", "Indian rock", "Iranian rock", "Instrumental rock", "Japanese rock", "Jazz fusion", "Korean rock", "Latin rock", "Mainstream rock", "Mangue bit", "Modern rock", "Occult rock", "Paisley Underground", "Pop rock", "Progressive rock", "Psychedelic rock", "Pub rock (Australia)", "Pub rock (United Kingdom)", "Punk rock", "Rap rock", "Reggae rock", "Rock and roll", "Rock music in France", "Rock opera", "Roots rock", "Southern rock", "Stoner rock", "Swamp rock", "Sufi rock", "Surf rock", "Tropical rock", "Viking rock", "Visual kei", "Wizard rock", "Worldbeat", "World fusion"],
        "Metal": ["Alternative metal", "Avant-garde metal", "Black metal", "Christian metal", "Death metal", "Doom metal", "Extreme metal", "Folk metal", "Glam metal", "Gothic metal", "Industrial metal", "Kawaii metal", "Latin metal", "Math metal", "Metalcore", "Neoclassical metal", "Neue Deutsche Härte", "New wave of American heavy metal", "New wave of British heavy metal", "Nintendocore", "Pirate metal", "Pop metal", "Power metal", "Progressive metal", "Sludge metal", "Speed metal", "Symphonic metal", "Thrash metal"],
        "Punk": ["Afro-punk", "Anarcho punk", "Art punk", "Avant punk", "Christian punk", "Crust punk", "Deathpunk", "Deathrock", "Electropunk", "Folk punk", "Garage punk", "German punk", "Glam punk", "Gothic punk", "Grindcore", "Hardcore punk", "Horror punk", "Latino punk", "Nazi punk", "Oi!", "Pop punk", "Post-punk", "Proto-punk", "Psychobilly", "Punk blues", "Punk jazz", "Punk pathetique", "Punk rap", "Punk rock", "Reggae punk", "Riot grrrl", "Ska punk", "Skate punk", "Street punk", "Surf punk", "Trallpunk"],
        "Regional": ["Latin music", "Reggae", "Celtic music"],
        "Religious": ["Sikh music", "Buddhist music", "Christian music", "Islamic music", "Modern pagan music", "Music of ancient Greece", "New-age music", "Shamanic music"],
        "Traditional Folk": ["American patriotic music", "Christmas music", "Fado", "Fingerstyle guitar", "Huayno", "Pastorale", "Polka", "Son mexicano", "Música criolla"]
        }
        '''
        music_genres = json.loads(music_genres_json)
        for item_genre, sub_categories in tqdm(music_genres.items(), total=len(music_genres), desc="Importing Music Genres"):
            # Create Tag for the genre
            genre_tag, created = Tag.objects.get_or_create(name=item_genre, group=music_genre)
            for sub_category in sub_categories:
                # Create Tag for the sub-category with a parent reference to the genre
                sub_category_tag, created = Tag.objects.get_or_create(name=sub_category, parent=genre_tag, group=music_genre)


        # Import Language
                # Importing Languages.
        # import alpha2, alpha3b, en_name
        lang_file = os.path.join(
            settings.BASE_DIR,
            "../Datasets/languages/language-codes/archive/language-codes-3b2.csv",
        )
        df = pd.read_csv(lang_file, encoding="utf-8", sep=",")

        for row in tqdm(df.iterrows(), total=len(df), desc="Importing Languages"):
            language, created = Language.objects.get_or_create(alpha2=row[1]["alpha2"])
            language.alpha3b = row[1]["alpha3-b"]
            language.en_name = row[1]["English"]
            language.save()

        # import alpha3t and less used languages
        lang_file = os.path.join(
            settings.BASE_DIR,
            "../Datasets/languages/language-codes/archive/language-codes-full.csv",
        )
        df = pd.read_csv(lang_file, encoding="utf-8", sep=",")
        df.fillna("", inplace=True)
        
        from django.db import IntegrityError
        for row in tqdm(df.iterrows(), total=len(df), desc="Importing Languages"):
            try:
                if row[1]["alpha2"] != "":
                    language = Language.objects.get(alpha2=row[1]["alpha2"])
                    if row[1]["alpha3-t"] != "":
                        language.alpha3t = row[1]["alpha3-t"]
                        language.save()
                else:
                    language = Language(alpha3b=row[1]["alpha3-b"], en_name=row[1]["English"])
                    language.save()
            except IntegrityError as e: 
                pass # Running this import multiple times causes this issues. passing the error is faster than cheking.
            except Exception as e:
                tqdm.write(f"Error {e} in importing row: {row[1]}")

        self.stdout.write(self.style.SUCCESS("Task Finished."))