from rest_framework_csv.renderers import CSVRenderer


class TransactionCSVRenderer(CSVRenderer):
    header = ['transaction', 'instrument', 'amount', 'price', 'currency', 'portfolio', 'account']
