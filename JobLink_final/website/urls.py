from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class AuthenticatedPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    pass


urlpatterns = [
    path("", Index.as_view(), name="pagina_inicial"),
    path("sobre/", Sobre.as_view(), name="sobre"),
    path("contato/", Contato.as_view(), name="contato"),

    path("cadastro/", CadastroUsuarioView.as_view(), name="cadastro"),
    path("login/", LoginView.as_view(
        template_name="website/form.html",
        extra_context={"titulo": "Entrar", "botao": "Entrar"}
    ), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("recuperar-usuario/", RecuperarUsuarioView.as_view(), name="recuperar_usuario"),
    path("recuperar-senha/", PasswordResetView.as_view(
        template_name="website/form.html",
        email_template_name="registration/password_reset_email.html",
        subject_template_name="registration/password_reset_subject.txt",
        success_url=reverse_lazy("password_reset_done"),
        extra_context={"titulo": "Recuperar senha", "botao": "Enviar link por e-mail"},
    ), name="password_reset"),
    path("recuperar-senha/enviado/", PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ), name="password_reset_done"),
    path("recuperar-senha/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
        template_name="website/form.html",
        success_url=reverse_lazy("password_reset_complete"),
        extra_context={"titulo": "Definir nova senha", "botao": "Salvar nova senha"},
    ), name="password_reset_confirm"),
    path("recuperar-senha/concluido/", PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ), name="password_reset_complete"),
    path("alterar-senha/", AuthenticatedPasswordChangeView.as_view(
        template_name="website/form.html",
        extra_context={"titulo": "Alterar senha", "botao": "Alterar senha"}
    ), name="alterar_senha"),

    path("empresas/", EmpresaList.as_view(), name="empresa_list"),
    path("empresa/cadastrar/", EmpresaCreate.as_view(), name="empresa_create"),
    path("empresa/<int:pk>/", EmpresaDetail.as_view(), name="empresa_detail"),
    path("empresa/<int:pk>/editar/", EmpresaUpdate.as_view(), name="empresa_update"),
    path("empresa/<int:pk>/excluir/", EmpresaDelete.as_view(), name="empresa_delete"),

    path("candidatos/", CandidatoList.as_view(), name="candidato_list"),
    path("candidato/cadastrar/", CandidatoCreate.as_view(), name="candidato_create"),
    path("candidato/<int:pk>/", CandidatoDetail.as_view(), name="candidato_detail"),
    path("candidato/<int:pk>/editar/", CandidatoUpdate.as_view(), name="candidato_update"),
    path("candidato/<int:pk>/excluir/", CandidatoDelete.as_view(), name="candidato_delete"),

    path("vagas/", VagaList.as_view(), name="vaga_list"),
    path("vaga/cadastrar/", VagaCreate.as_view(), name="vaga_create"),
    path("vaga/<int:pk>/", VagaDetail.as_view(), name="vaga_detail"),
    path("vaga/<int:pk>/editar/", VagaUpdate.as_view(), name="vaga_update"),
    path("vaga/<int:pk>/excluir/", VagaDelete.as_view(), name="vaga_delete"),
    path("minhas-vagas/", MinhasVagas.as_view(), name="minhas_vagas"),

    path("candidaturas/", CandidaturaList.as_view(), name="minhas_candidaturas"),
    path("candidatura/vaga/<int:vaga_pk>/", CandidaturaCreate.as_view(), name="candidatura_create"),
    path("candidatura/<int:pk>/", CandidaturaDetail.as_view(), name="candidatura_detail"),
    path("candidatura/<int:pk>/editar/", CandidaturaUpdate.as_view(), name="candidatura_update"),
    path("candidatura/<int:pk>/excluir/", CandidaturaDelete.as_view(), name="candidatura_delete"),
    path("candidaturas/empresa/", CandidaturasDaEmpresa.as_view(), name="candidaturas_empresa"),

    path("notificacoes/", NotificacaoList.as_view(), name="notificacao_list"),
    path("notificacao/<int:pk>/", NotificacaoDetail.as_view(), name="notificacao_detail"),
    path("notificacao/<int:pk>/excluir/", NotificacaoDelete.as_view(), name="notificacao_delete"),
]
