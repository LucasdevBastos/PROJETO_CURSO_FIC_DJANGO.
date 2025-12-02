# anime/models.py
from django.db import models


class Temporada(models.Model):
    INVERNO = "INVERNO"
    PRIMAVERA = "PRIMAVERA"
    VERAO = "VERAO"
    OUTONO = "OUTONO"

    ESTACOES = [
        (INVERNO, "Inverno"),
        (PRIMAVERA, "Primavera"),
        (VERAO, "Verão"),
        (OUTONO, "Outono"),
    ]

    ano = models.IntegerField()
    estacao = models.CharField(max_length=10, choices=ESTACOES)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    is_atual = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Temporada"
        verbose_name_plural = "Temporadas"
        unique_together = ("ano", "estacao")
        ordering = ["-ano", "estacao"]

    def __str__(self):
        return f"{self.get_estacao_display()} {self.ano}"


class Genero(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Studio(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    site_oficial = models.URLField(blank=True)

    class Meta:
        verbose_name = "Estúdio"
        verbose_name_plural = "Estúdios"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Anime(models.Model):
    STATUS_EM_LANCAMENTO = "EM_LANCAMENTO"
    STATUS_FINALIZADO = "FINALIZADO"
    STATUS_PAUSADO = "PAUSADO"

    STATUS_CHOICES = [
        (STATUS_EM_LANCAMENTO, "Em lançamento"),
        (STATUS_FINALIZADO, "Finalizado"),
        (STATUS_PAUSADO, "Pausado"),
    ]

    TIPO_TV = "TV"
    TIPO_MOVIE = "MOVIE"
    TIPO_OVA = "OVA"
    TIPO_SPECIAL = "SPECIAL"

    TIPOS = [
        (TIPO_TV, "TV"),
        (TIPO_MOVIE, "Filme"),
        (TIPO_OVA, "OVA"),
        (TIPO_SPECIAL, "Especial"),
    ]

    mal_id = models.IntegerField("ID do MyAnimeList", unique=True)
    titulo = models.CharField(max_length=255)
    titulo_ingles = models.CharField(max_length=255, blank=True, null=True)
    sinopse = models.TextField(blank=True)
    imagem_url = models.URLField(blank=True)
    trailer_url = models.URLField(blank=True)

    tipo = models.CharField(max_length=20, choices=TIPOS, default=TIPO_TV)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_EM_LANCAMENTO,
    )

    episodios_total = models.IntegerField(null=True, blank=True)
    data_lancamento = models.DateField(null=True, blank=True)
    data_encerramento = models.DateField(null=True, blank=True)

    temporada = models.ForeignKey(
        Temporada,
        on_delete=models.SET_NULL,
        related_name="animes",
        null=True,
        blank=True,
    )

    generos = models.ManyToManyField(
        Genero,
        through="AnimeGenero",
        related_name="animes",
        blank=True,
    )
    studios = models.ManyToManyField(
        Studio,
        through="AnimeStudio",
        related_name="animes",
        blank=True,
    )

    nota_mal = models.FloatField(null=True, blank=True)
    popularidade_score = models.IntegerField(default=0)
    membros_mal = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Anime"
        verbose_name_plural = "Animes"
        ordering = ["-data_lancamento", "-nota_mal"]

    def __str__(self):
        return self.titulo


class AnimeGenero(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("anime", "genero")
        verbose_name = "Gênero do anime"
        verbose_name_plural = "Gêneros do anime"

    def __str__(self):
        return f"{self.anime} - {self.genero}"


class AnimeStudio(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("anime", "studio")
        verbose_name = "Estúdio do anime"
        verbose_name_plural = "Estúdios do anime"

    def __str__(self):
        return f"{self.anime} - {self.studio}"


class AnimeAiring(models.Model):
    """
    Datas de exibição (p/ calendário diário/mensal).
    Pode ser por episódio ou só datas chave.
    """
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        related_name="airings",
    )
    episodio = models.IntegerField(null=True, blank=True)
    data_exibicao = models.DateField()
    hora_exibicao = models.TimeField(null=True, blank=True)
    timezone = models.CharField(max_length=50, blank=True)
    observacao = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Exibição"
        verbose_name_plural = "Exibições"
        ordering = ["data_exibicao", "hora_exibicao"]

    def __str__(self):
        ep = f"Ep. {self.episodio}" if self.episodio else "Estreia"
        return f"{self.anime} - {ep} em {self.data_exibicao}"
