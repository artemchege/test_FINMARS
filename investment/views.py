import codecs
import csv
import json

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from url_filter.integrations.drf import DjangoFilterBackend

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
    permission_classes = [AllowAny]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all().prefetch_related('currency', 'instrument', 'portfolio', 'account')
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'transaction_date', 'type', 'amount', 'price', 'currency', 'instrument', 'portfolio',
                     'account', 'notes', 'custom_attrs']

    @action(detail=False, methods=["get"])
    def get_transaction_csv(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=transactions.csv"
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)

        writer.writerow(
            [
                "transaction",
                "instrument",
                "amount",
                "price",
                "currency",
                "portfolio",
                "account",
            ]
        )

        for transaction in self.queryset:
            writer.writerow(
                [
                    transaction.type,
                    transaction.instrument.name,
                    transaction.amount,
                    transaction.price,
                    transaction.currency.code,
                    transaction.portfolio.name,
                    transaction.account.name,
                ]
            )

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
