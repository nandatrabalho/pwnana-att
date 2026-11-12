from django.db import models
from django.contrib.auth.models import User


class Empresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="empresa")
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    setor = models.CharField(max_length=80, blank=True)
    cidade = models.CharField(max_length=80, blank=True)
    site = models.URLField(blank=True)

    atualizado_em = models.DateTimeField(auto_now=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Candidato(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidato")
    nome = models.CharField(max_length=120)
    titulo_profissional = models.CharField(max_length=120, blank=True)
    resumo = models.TextField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    cidade = models.CharField(max_length=80, blank=True)
    linkedin = models.URLField(blank=True)

    atualizado_em = models.DateTimeField(auto_now=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Vaga(models.Model):
    TIPO_CHOICES = [
        ("CLT", "CLT"),
        ("PJ", "PJ"),
        ("ESTAGIO", "Estágio"),
        ("TEMPORARIO", "Temporário"),
    ]
    MODALIDADE_CHOICES = [
        ("PRESENCIAL", "Presencial"),
        ("HIBRIDO", "Híbrido"),
        ("REMOTO", "Remoto"),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="vagas")
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    requisitos = models.TextField()
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CHOICES)
    modalidade = models.CharField(max_length=20, choices=MODALIDADE_CHOICES)
    localizacao = models.CharField(max_length=120, blank=True)
    ativa = models.BooleanField(default=True)
    publicada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)
    prazo_inscricao = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.empresa.nome}"


class Candidatura(models.Model):
    STATUS_CHOICES = [
        ("ENVIADA", "Enviada"),
        ("EM_ANALISE", "Em análise"),
        ("ENTREVISTA", "Entrevista"),
        ("APROVADA", "Aprovada"),
        ("RECUSADA", "Recusada"),
    ]

    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name="candidaturas")
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name="candidaturas")
    mensagem = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ENVIADA")
    candidata_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["candidato", "vaga"], name="candidatura_unica_por_vaga")
        ]
        ordering = ["-candidata_em"]

    def __str__(self):
        return f"{self.candidato.nome} → {self.vaga.titulo}"



class Notificacao(models.Model):
    """Avisos privados enviados a um usuário do JobLink."""

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notificacoes"
    )
    titulo = models.CharField(max_length=120)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-criada_em"]
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
