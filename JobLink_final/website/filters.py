import django_filters
from django.db.models import Q

from .models import Vaga


class VagaFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="buscar", label="Palavra-chave")
    modalidade = django_filters.ChoiceFilter(
        choices=Vaga.MODALIDADE_CHOICES, empty_label="Todas as modalidades"
    )
    tipo_contrato = django_filters.ChoiceFilter(
        choices=Vaga.TIPO_CHOICES, empty_label="Todos os contratos"
    )
    cidade = django_filters.CharFilter(field_name="localizacao", lookup_expr="icontains", label="Cidade")

    class Meta:
        model = Vaga
        fields = ["q", "modalidade", "tipo_contrato", "cidade"]

    def buscar(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(titulo__icontains=value)
            | Q(empresa__nome__icontains=value)
            | Q(requisitos__icontains=value)
            | Q(descricao__icontains=value)
        )
