# Generated manually for the JobLink project.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Candidato",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120)),
                ("titulo_profissional", models.CharField(blank=True, max_length=120)),
                ("resumo", models.TextField(blank=True)),
                ("telefone", models.CharField(blank=True, max_length=20)),
                ("cidade", models.CharField(blank=True, max_length=80)),
                ("linkedin", models.URLField(blank=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                ("cadastrado_em", models.DateTimeField(auto_now_add=True)),
                ("usuario", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="candidato", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Empresa",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120)),
                ("descricao", models.TextField(blank=True)),
                ("setor", models.CharField(blank=True, max_length=80)),
                ("cidade", models.CharField(blank=True, max_length=80)),
                ("site", models.URLField(blank=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                ("cadastrado_em", models.DateTimeField(auto_now_add=True)),
                ("usuario", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="empresa", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Vaga",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=150)),
                ("descricao", models.TextField()),
                ("requisitos", models.TextField()),
                ("salario", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("tipo_contrato", models.CharField(choices=[("CLT", "CLT"), ("PJ", "PJ"), ("ESTAGIO", "Estágio"), ("TEMPORARIO", "Temporário")], max_length=20)),
                ("modalidade", models.CharField(choices=[("PRESENCIAL", "Presencial"), ("HIBRIDO", "Híbrido"), ("REMOTO", "Remoto")], max_length=20)),
                ("localizacao", models.CharField(blank=True, max_length=120)),
                ("ativa", models.BooleanField(default=True)),
                ("publicada_em", models.DateTimeField(auto_now_add=True)),
                ("atualizada_em", models.DateTimeField(auto_now=True)),
                ("prazo_inscricao", models.DateField(blank=True, null=True)),
                ("empresa", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="vagas", to="website.empresa")),
            ],
        ),
        migrations.CreateModel(
            name="Candidatura",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("mensagem", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("ENVIADA", "Enviada"), ("EM_ANALISE", "Em análise"), ("ENTREVISTA", "Entrevista"), ("APROVADA", "Aprovada"), ("RECUSADA", "Recusada")], default="ENVIADA", max_length=20)),
                ("candidata_em", models.DateTimeField(auto_now_add=True)),
                ("atualizada_em", models.DateTimeField(auto_now=True)),
                ("candidato", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="candidaturas", to="website.candidato")),
                ("vaga", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="candidaturas", to="website.vaga")),
            ],
            options={
                "ordering": ["-candidata_em"],
            },
        ),
        migrations.AddConstraint(
            model_name="candidatura",
            constraint=models.UniqueConstraint(fields=("candidato", "vaga"), name="candidatura_unica_por_vaga"),
        ),
    ]
