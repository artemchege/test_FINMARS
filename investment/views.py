import json

from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from url_filter.integrations.drf import DjangoFilterBackend

from investment.renderers import TransactionCSVRenderer
from investment.serializers import PortfolioSerializer, TransactionSerializer, CurrencySerializer, InstrumentSerializer, \
    AccountSerializer
from investment.models import Portfolio, Transaction, Currency, Instrument, Account


class FilterCustomAttrsMixin(GenericViewSet):
    """ Миксин, который применяется для viewsets и позволяет делать гибкие и сложные фильтрации по JSONFIELD с именем
    custom_attrs"""

    def get_queryset(self):
        queryset = self.queryset
        filter_string = self.request.query_params.get('custom_attrs')

        if filter_string:
            filter_dictionary = json.loads(filter_string)
            queryset = queryset.filter(**filter_dictionary)

        return queryset


class PortfolioViewSet(FilterCustomAttrsMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'name', 'notes', 'strategy', 'custom_attrs']


class TransactionViewSet(FilterCustomAttrsMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all().prefetch_related('currency', 'instrument', 'portfolio', 'account')
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'transaction_date', 'type', 'amount', 'price', 'currency', 'instrument', 'portfolio',
                     'account', 'notes', 'custom_attrs']

    @action(detail=False, methods=["get"], renderer_classes=[TransactionCSVRenderer])
    def get_transaction_csv(self, request):
        content = [
            {
                'transaction': transaction.type,
                'instrument': transaction.instrument.name,
                'amount': transaction.amount,
                'price': transaction.price,
                'currency': transaction.currency.code,
                'portfolio': transaction.portfolio.name,
                'account': transaction.account.name,
             }
            for transaction in self.queryset]

        response = Response(content, content_type='text/csv')
        response["Content-Disposition"] = "attachment; filename=transactions.csv"
        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user) if not isinstance(self.request.user, AnonymousUser) else queryset


class CurrencyViewSet(FilterCustomAttrsMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'name', 'code', 'custom_attrs']


class InstrumentViewSet(FilterCustomAttrsMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'currency', 'name', 'isin', 'description', 'maturity_date', 'accrual_size', 'accrual_date',
                     'custom_attrs']


class AccountViewSet(FilterCustomAttrsMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'name', 'type', 'user', 'custom_attrs']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user) if not isinstance(self.request.user, AnonymousUser) else queryset
