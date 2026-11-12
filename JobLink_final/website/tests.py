from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from .models import Candidato, Empresa, Vaga, Candidatura, Notificacao


class JobLinkTests(TestCase):
    def setUp(self):
        self.company_user = User.objects.create_user(username="empresa", password="Teste@123")
        self.candidate_user = User.objects.create_user(username="candidato", password="Teste@123")
        Group.objects.get_or_create(name="Empresa")
        Group.objects.get_or_create(name="Candidato")
        self.company_user.groups.add(Group.objects.get(name="Empresa"))
        self.candidate_user.groups.add(Group.objects.get(name="Candidato"))
        self.empresa = Empresa.objects.create(usuario=self.company_user, nome="Empresa Teste")
        self.candidato = Candidato.objects.create(usuario=self.candidate_user, nome="Candidato Teste")
        self.vaga = Vaga.objects.create(
            empresa=self.empresa, titulo="Desenvolvedor Django",
            descricao="Desenvolver sistemas web.", requisitos="Python e Django.",
            tipo_contrato="CLT", modalidade="REMOTO", ativa=True,
        )

    def test_lista_vagas_publica(self):
        response = self.client.get(reverse("vaga_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Desenvolvedor Django")

    def test_candidato_pode_se_candidatar(self):
        self.client.force_login(self.candidate_user)
        response = self.client.post(
            reverse("candidatura_create", args=[self.vaga.pk]),
            {"mensagem": "Tenho interesse na oportunidade."},
        )
        self.assertRedirects(response, reverse("minhas_candidaturas"))
        self.assertTrue(Candidatura.objects.filter(vaga=self.vaga, candidato=self.candidato).exists())


    def test_filtro_de_vagas_por_modalidade(self):
        response = self.client.get(reverse("vaga_list"), {"modalidade": "REMOTO"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Desenvolvedor Django")
        response = self.client.get(reverse("vaga_list"), {"modalidade": "PRESENCIAL"})
        self.assertNotContains(response, "Desenvolvedor Django")

    def test_empresa_so_lista_seu_proprio_perfil(self):
        outro_usuario = User.objects.create_user(username="outraempresa", password="Teste@123")
        grupo = Group.objects.get(name="Empresa")
        outro_usuario.groups.add(grupo)
        Empresa.objects.create(usuario=outro_usuario, nome="Outra Empresa")
        self.client.force_login(self.company_user)
        response = self.client.get(reverse("empresa_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Empresa Teste")
        self.assertNotContains(response, "Outra Empresa")

    def test_empresa_nao_visualiza_perfil_de_outra_empresa(self):
        outro_usuario = User.objects.create_user(username="outraempresa2", password="Teste@123")
        outra = Empresa.objects.create(usuario=outro_usuario, nome="Empresa Privada")
        self.client.force_login(self.company_user)
        response = self.client.get(reverse("empresa_detail", args=[outra.pk]))
        self.assertEqual(response.status_code, 404)

    def test_candidato_so_lista_seu_proprio_perfil(self):
        outro_usuario = User.objects.create_user(username="outrocandidato", password="Teste@123")
        outro_usuario.groups.add(Group.objects.get(name="Candidato"))
        Candidato.objects.create(usuario=outro_usuario, nome="Outro Candidato")
        self.client.force_login(self.candidate_user)
        response = self.client.get(reverse("candidato_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Candidato Teste")
        self.assertNotContains(response, "Outro Candidato")

    def test_cadastro_exibe_mensagem_de_sucesso(self):
        self.client.force_login(self.company_user)
        response = self.client.post(reverse("vaga_create"), {
            "titulo": "Analista de Testes",
            "descricao": "Testar sistemas",
            "requisitos": "Atenção aos detalhes",
            "tipo_contrato": "CLT",
            "modalidade": "HIBRIDO",
            "localizacao": "Curitiba",
            "ativa": "on",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cadastrado com sucesso")

    def test_recuperar_usuario_envia_email(self):
        from django.core import mail
        from django.test import override_settings
        self.candidate_user.email = "candidato@example.com"
        self.candidate_user.save()
        with override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"):
            response = self.client.post(reverse("recuperar_usuario"), {"email": "candidato@example.com"})
            self.assertRedirects(response, reverse("login"))
            self.assertEqual(len(mail.outbox), 1)
            self.assertIn("candidato", mail.outbox[0].body)


    def test_recuperar_senha_envia_email(self):
        from django.core import mail
        from django.test import override_settings
        self.candidate_user.email = "candidato@example.com"
        self.candidate_user.save()
        with override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"):
            response = self.client.post(reverse("password_reset"), {"email": "candidato@example.com"})
            self.assertRedirects(response, reverse("password_reset_done"))
            self.assertEqual(len(mail.outbox), 1)
            self.assertIn("recuperar-senha", mail.outbox[0].body)


    def test_notificacao_e_criada_ao_receber_candidatura(self):
        self.client.force_login(self.candidate_user)
        self.client.post(
            reverse("candidatura_create", args=[self.vaga.pk]),
            {"mensagem": "Tenho interesse."},
        )
        self.assertTrue(Notificacao.objects.filter(
            usuario=self.company_user,
            titulo="Nova candidatura recebida",
        ).exists())

    def test_usuario_so_acessa_suas_notificacoes(self):
        notificacao = Notificacao.objects.create(
            usuario=self.company_user,
            titulo="Aviso privado",
            mensagem="Conteúdo privado",
        )
        self.client.force_login(self.candidate_user)
        response = self.client.get(reverse("notificacao_detail", args=[notificacao.pk]))
        self.assertEqual(response.status_code, 404)

    def test_visualizar_notificacao_marca_como_lida(self):
        notificacao = Notificacao.objects.create(
            usuario=self.company_user,
            titulo="Aviso",
            mensagem="Mensagem",
        )
        self.client.force_login(self.company_user)
        response = self.client.get(reverse("notificacao_detail", args=[notificacao.pk]))
        self.assertEqual(response.status_code, 200)
        notificacao.refresh_from_db()
        self.assertTrue(notificacao.lida)
