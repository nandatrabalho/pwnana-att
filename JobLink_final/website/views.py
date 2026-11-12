from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView
from braces.views import GroupRequiredMixin

from django.core.mail import send_mail
from django.conf import settings
from .forms import CadastroUsuarioForm, EmpresaForm, CandidatoForm, CandidaturaForm, RecuperarUsuarioForm
from .filters import VagaFilter
from .models import Empresa, Candidato, Vaga, Candidatura, Notificacao




class MensagensCRUDMixin:
    """Feedback do Django Messages nas operações de cadastro, edição e exclusão."""
    mensagem_criacao = "Registro cadastrado com sucesso."
    mensagem_edicao = "Registro atualizado com sucesso."
    mensagem_exclusao = "Registro excluído com sucesso."

    def form_valid(self, form):
        response = super().form_valid(form)
        if isinstance(self, CreateView):
            messages.success(self.request, self.mensagem_criacao)
        elif isinstance(self, UpdateView):
            messages.success(self.request, self.mensagem_edicao)
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, self.mensagem_exclusao)
        return response


class RecuperarUsuarioView(TemplateView):
    template_name = "website/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"titulo": "Recuperar nome de usuário", "botao": "Enviar por e-mail", "form": RecuperarUsuarioForm()})
        return context

    def post(self, request, *args, **kwargs):
        form = RecuperarUsuarioForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            usuarios = User.objects.filter(email__iexact=email, is_active=True)
            if usuarios.exists():
                nomes = ", ".join(usuarios.values_list("username", flat=True))
                send_mail(
                    "Recuperação de nome de usuário - JobLink",
                    f"Olá! Seu(s) nome(s) de usuário no JobLink: {nomes}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            messages.success(request, "Se existir uma conta com esse e-mail, enviaremos as instruções.")
            return redirect("login")
        return render(request, self.template_name, {"form": form, "titulo": "Recuperar nome de usuário", "botao": "Enviar por e-mail"})


class Index(TemplateView):
    template_name = "website/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vagas"] = (
            Vaga.objects.filter(ativa=True)
            .select_related("empresa")
            .annotate(total_candidaturas=Count("candidaturas"))
            .order_by("-publicada_em")[:6]
        )
        context["total_vagas"] = Vaga.objects.filter(ativa=True).count()
        context["total_empresas"] = Empresa.objects.count()
        context["total_candidatos"] = Candidato.objects.count()
        return context


class Sobre(TemplateView):
    template_name = "website/sobre.html"


class Contato(TemplateView):
    template_name = "website/contato.html"


class CadastroUsuarioView(CreateView):
    form_class = CadastroUsuarioForm
    template_name = "website/form.html"
    success_url = reverse_lazy("pagina_inicial")
    extra_context = {"titulo": "Criar conta", "botao": "Criar conta"}

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Conta criada com sucesso!")
        tipo = form.cleaned_data["tipo"]
        grupo, _ = Group.objects.get_or_create(name="Empresa" if tipo == "empresa" else "Candidato")
        self.object.groups.add(grupo)
        login(self.request, self.object)

        if tipo == "empresa":
            Empresa.objects.create(
                usuario=self.object,
                nome=self.object.get_full_name() or self.object.username,
            )
        else:
            Candidato.objects.create(
                usuario=self.object,
                nome=self.object.get_full_name() or self.object.username,
            )
        return response


#################### Empresa ####################

class EmpresaCreate(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = ["Empresa"]
    model = Empresa
    form_class = EmpresaForm
    template_name = "website/form.html"
    success_url = reverse_lazy("empresa_list")
    extra_context = {"titulo": "Meu perfil de empresa", "botao": "Salvar"}

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, "empresa"):
            return redirect("empresa_update", pk=request.user.empresa.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class EmpresaUpdate(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_required = ["Empresa"]
    model = Empresa
    form_class = EmpresaForm
    template_name = "website/form.html"
    success_url = reverse_lazy("empresa_list")
    extra_context = {"titulo": "Editar perfil da empresa", "botao": "Salvar"}

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class EmpresaDelete(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    group_required = ["Empresa"]
    model = Empresa
    template_name = "website/form.html"
    success_url = reverse_lazy("pagina_inicial")
    extra_context = {"titulo": "Excluir empresa", "botao": "Excluir"}

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class EmpresaList(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = ["Empresa"]
    model = Empresa
    template_name = "website/listas/empresas.html"
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user).order_by("nome")


class EmpresaDetail(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_required = ["Empresa"]
    model = Empresa
    template_name = "website/ver/empresa.html"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user).prefetch_related("vagas")


#################### Candidato ####################

class CandidatoCreate(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = ["Candidato"]
    model = Candidato
    form_class = CandidatoForm
    template_name = "website/form.html"
    success_url = reverse_lazy("candidato_list")
    extra_context = {"titulo": "Meu perfil profissional", "botao": "Salvar"}

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, "candidato"):
            return redirect("candidato_update", pk=request.user.candidato.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class CandidatoUpdate(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_required = ["Candidato"]
    model = Candidato
    form_class = CandidatoForm
    template_name = "website/form.html"
    success_url = reverse_lazy("candidato_list")
    extra_context = {"titulo": "Editar perfil profissional", "botao": "Salvar"}

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class CandidatoDelete(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    group_required = ["Candidato"]
    model = Candidato
    template_name = "website/form.html"
    success_url = reverse_lazy("pagina_inicial")
    extra_context = {"titulo": "Excluir perfil", "botao": "Excluir"}

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class CandidatoList(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = ["Candidato"]
    model = Candidato
    template_name = "website/listas/candidatos.html"
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user).order_by("nome")


class CandidatoDetail(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_required = ["Candidato"]
    model = Candidato
    template_name = "website/ver/candidato.html"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user).select_related("usuario")


#################### Vagas ####################

class VagaCreate(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = ["Empresa"]
    model = Vaga
    fields = [
        "titulo", "descricao", "requisitos", "salario",
        "tipo_contrato", "modalidade", "localizacao", "ativa", "prazo_inscricao"
    ]
    template_name = "website/form.html"
    success_url = reverse_lazy("vaga_list")
    extra_context = {"titulo": "Publicar vaga", "botao": "Publicar vaga"}

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)


class VagaUpdate(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_required = ["Empresa"]
    model = Vaga
    fields = [
        "titulo", "descricao", "requisitos", "salario",
        "tipo_contrato", "modalidade", "localizacao", "ativa", "prazo_inscricao"
    ]
    template_name = "website/form.html"
    success_url = reverse_lazy("vaga_list")
    extra_context = {"titulo": "Editar vaga", "botao": "Salvar alterações"}

    def get_queryset(self):
        return super().get_queryset().filter(empresa__usuario=self.request.user)


class VagaDelete(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    group_required = ["Empresa"]
    model = Vaga
    template_name = "website/form.html"
    success_url = reverse_lazy("vaga_list")
    extra_context = {"titulo": "Excluir vaga", "botao": "Excluir"}

    def get_queryset(self):
        return super().get_queryset().filter(empresa__usuario=self.request.user)


class VagaList(ListView):
    model = Vaga
    template_name = "website/listas/vagas.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            Vaga.objects.filter(ativa=True)
            .select_related("empresa")
            .annotate(total_candidaturas=Count("candidaturas"))
            .order_by("-publicada_em")
        )
        self.filterset = VagaFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


class VagaDetail(DetailView):
    model = Vaga
    template_name = "website/ver/vaga.html"

    def get_queryset(self):
        return super().get_queryset().select_related("empresa").annotate(total_candidaturas=Count("candidaturas"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ja_candidatou"] = (
            self.request.user.is_authenticated
            and hasattr(self.request.user, "candidato")
            and Candidatura.objects.filter(vaga=self.object, candidato=self.request.user.candidato).exists()
        )
        return context


class MinhasVagas(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = ["Empresa"]
    model = Vaga
    template_name = "website/listas/minhas_vagas.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(empresa__usuario=self.request.user).annotate(total_candidaturas=Count("candidaturas")).order_by("-publicada_em")


#################### Candidaturas ####################

class CandidaturaCreate(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = ["Candidato"]
    model = Candidatura
    form_class = CandidaturaForm
    template_name = "website/form.html"
    success_url = reverse_lazy("minhas_candidaturas")
    extra_context = {"titulo": "Candidatar-se à vaga", "botao": "Enviar candidatura"}

    def dispatch(self, request, *args, **kwargs):
        self.vaga = Vaga.objects.select_related("empresa").filter(pk=kwargs["vaga_pk"], ativa=True).first()
        if not self.vaga:
            return redirect("vaga_list")
        if Candidatura.objects.filter(vaga=self.vaga, candidato__usuario=request.user).exists():
            messages.info(request, "Você já se candidatou a esta vaga.")
            return redirect("vaga_detail", pk=self.vaga.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.candidato = self.request.user.candidato
        form.instance.vaga = self.vaga
        response = super().form_valid(form)
        Notificacao.objects.create(
            usuario=self.vaga.empresa.usuario,
            titulo="Nova candidatura recebida",
            mensagem=f"{self.request.user.get_full_name() or self.request.user.username} candidatou-se à vaga {self.vaga.titulo}.",
            link=reverse_lazy("candidaturas_empresa"),
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vaga"] = self.vaga
        return context


class CandidaturaUpdate(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_required = ["Candidato"]
    model = Candidatura
    form_class = CandidaturaForm
    template_name = "website/form.html"
    success_url = reverse_lazy("minhas_candidaturas")
    extra_context = {"titulo": "Editar candidatura", "botao": "Salvar"}

    def get_queryset(self):
        return super().get_queryset().filter(candidato__usuario=self.request.user)


class CandidaturaDelete(MensagensCRUDMixin, LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    group_required = ["Candidato"]
    model = Candidatura
    template_name = "website/form.html"
    success_url = reverse_lazy("minhas_candidaturas")
    extra_context = {"titulo": "Cancelar candidatura", "botao": "Excluir"}

    def get_queryset(self):
        return super().get_queryset().filter(candidato__usuario=self.request.user)


class CandidaturaList(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = ["Candidato"]
    model = Candidatura
    template_name = "website/listas/candidaturas.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(candidato__usuario=self.request.user).select_related("vaga__empresa")


class CandidaturaDetail(LoginRequiredMixin, DetailView):
    model = Candidatura
    template_name = "website/ver/candidatura.html"

    def get_queryset(self):
        return super().get_queryset().filter(candidato__usuario=self.request.user).select_related("vaga__empresa", "candidato")


class CandidaturasDaEmpresa(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = ["Empresa"]
    model = Candidatura
    template_name = "website/listas/candidaturas_empresa.html"
    paginate_by = 20

    def get_queryset(self):
        return (
            super().get_queryset()
            .filter(vaga__empresa__usuario=self.request.user)
            .select_related("vaga", "candidato", "candidato__usuario")
        )



#################### Notificações ####################

class NotificacaoList(LoginRequiredMixin, ListView):
    model = Notificacao
    template_name = "website/listas/notificacoes.html"
    context_object_name = "notificacoes"
    paginate_by = 15

    def get_queryset(self):
        return Notificacao.objects.filter(usuario=self.request.user).order_by("-criada_em")


class NotificacaoDetail(LoginRequiredMixin, DetailView):
    model = Notificacao
    template_name = "website/ver/notificacao.html"
    context_object_name = "notificacao"

    def get_queryset(self):
        return Notificacao.objects.filter(usuario=self.request.user)

    def get_object(self, queryset=None):
        objeto = super().get_object(queryset)
        if not objeto.lida:
            objeto.lida = True
            objeto.save(update_fields=["lida"])
        return objeto


class NotificacaoDelete(LoginRequiredMixin, DeleteView):
    model = Notificacao
    template_name = "website/form.html"
    success_url = reverse_lazy("notificacao_list")
    extra_context = {"titulo": "Excluir notificação", "botao": "Excluir"}

    def get_queryset(self):
        return Notificacao.objects.filter(usuario=self.request.user)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Notificação excluída com sucesso.")
        return response
