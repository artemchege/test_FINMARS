from rest_framework import serializers

from investment.models import Portfolio, Transaction, Currency, Instrument, Account


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['name', 'notes', 'strategy', 'custom_attrs']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        depth = 2
        fields = ['transaction_date', 'type', 'amount', 'price', 'currency', 'instrument', 'portfolio', 'account',
                  'notes', 'custom_attrs']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name', 'code', 'custom_attrs']


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['currency', 'name', 'isin', 'description', 'maturity_date', 'accrual_size', 'accrual_date',
                  'custom_attrs']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['name', 'type', 'user', 'custom_attrs']
