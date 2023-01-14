from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from url_filter.integrations.drf import DjangoFilterBackend

from investment.mixins import FilterCustomAttrsMixin
from investment.renderers import TransactionCSVRenderer
from investment.serializers import PortfolioSerializer, TransactionSerializer, CurrencySerializer, InstrumentSerializer, \
    AccountSerializer
from investment.models import Portfolio, Transaction, Currency, Instrument, Account


class PortfolioViewSet(FilterCustomAttrsMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'name', 'notes', 'strategy']


class TransactionViewSet(FilterCustomAttrsMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all().prefetch_related('currency', 'instrument', 'portfolio', 'account')
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'transaction_date', 'type', 'amount', 'price', 'currency', 'instrument', 'portfolio',
                     'account', 'notes']

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
    filter_fields = ['id', 'name', 'code']


class InstrumentViewSet(FilterCustomAttrsMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'currency', 'name', 'isin', 'description', 'maturity_date', 'accrual_size', 'accrual_date']


class AccountViewSet(FilterCustomAttrsMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'name', 'type', 'user']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user) if not isinstance(self.request.user, AnonymousUser) else queryset
