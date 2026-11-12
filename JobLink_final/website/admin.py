from django.contrib import admin
from .models import Empresa, Candidato, Vaga, Candidatura, Notificacao


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome", "setor", "cidade", "usuario")
    search_fields = ("nome", "setor", "cidade")


@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ("nome", "titulo_profissional", "cidade", "usuario")
    search_fields = ("nome", "titulo_profissional", "cidade")


@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "empresa", "modalidade", "tipo_contrato", "ativa", "publicada_em")
    list_filter = ("ativa", "modalidade", "tipo_contrato")
    search_fields = ("titulo", "empresa__nome")


@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ("vaga", "candidato", "status", "candidata_em")
    list_filter = ("status",)
    search_fields = ("vaga__titulo", "candidato__nome")


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "lida", "criada_em")
    list_filter = ("lida", "criada_em")
    search_fields = ("titulo", "mensagem", "usuario__username")
