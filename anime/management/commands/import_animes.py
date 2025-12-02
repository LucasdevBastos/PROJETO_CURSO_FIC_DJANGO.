import requests
from django.core.management.base import BaseCommand
from anime.models import Anime, Genero
import time


class Command(BaseCommand):
    help = 'Importa animes da API Jikan'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=25,
            help='Número máximo de animes a importar'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        base_url = "https://api.jikan.moe/v4/anime"
        
        self.stdout.write(self.style.SUCCESS(f'Iniciando importação de até {limit} animes...'))
        
        try:
            # Importar animes populares
            page = 1
            imported_count = 0
            
            while imported_count < limit:
                url = f"{base_url}?page={page}&limit=25&order_by=score&sort=desc&min_score=6.5"
                
                self.stdout.write(f'Buscando página {page}...')
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if not data.get('data'):
                    break
                
                for anime_data in data['data']:
                    if imported_count >= limit:
                        break
                    
                    try:
                        mal_id = anime_data.get('mal_id')
                        titulo = anime_data.get('title', '')
                        titulo_ingles = anime_data.get('title_english', '')
                        
                        # Verificar se já existe
                        if Anime.objects.filter(mal_id=mal_id).exists():
                            self.stdout.write(self.style.WARNING(f'⊘ {titulo} já existe'))
                            continue
                        
                        # Criar anime
                        anime = Anime.objects.create(
                            mal_id=mal_id,
                            titulo=titulo,
                            titulo_ingles=titulo_ingles,
                            sinopse=anime_data.get('synopsis', ''),
                            imagem_url=anime_data.get('images', {}).get('jpg', {}).get('image_url', ''),
                            nota_mal=anime_data.get('score', 0),
                            tipo=anime_data.get('type', ''),
                            status=anime_data.get('status', ''),
                        )
                        
                        # Adicionar gêneros
                        for genre_data in anime_data.get('genres', []):
                            genre_name = genre_data.get('name', '').lower()
                            if genre_name:
                                genre, _ = Genero.objects.get_or_create(nome=genre_name)
                                anime.generos.add(genre)
                        
                        self.stdout.write(self.style.SUCCESS(f'✓ {titulo}'))
                        imported_count += 1
                        
                        # Delay para não sobrecarregar a API
                        time.sleep(0.5)
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'✗ Erro ao importar: {str(e)}'))
                        continue
                
                page += 1
                
                # Delay entre páginas
                time.sleep(1)
            
            self.stdout.write(self.style.SUCCESS(f'\n✓ Importação concluída! {imported_count} animes importados.'))
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Erro na requisição: {str(e)}'))
