# Generated for JobLink - terceiro trimestre.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notificacao",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=120)),
                ("mensagem", models.TextField()),
                ("lida", models.BooleanField(default=False)),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                ("link", models.CharField(blank=True, max_length=255)),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notificacoes", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Notificação",
                "verbose_name_plural": "Notificações",
                "ordering": ["-criada_em"],
            },
        ),
    ]
