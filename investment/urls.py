from rest_framework import routers

from investment.views import PortfolioViewSet, AccountViewSet, TransactionViewSet, CurrencyViewSet, InstrumentViewSet


router = routers.DefaultRouter()
router.register("portfolio", PortfolioViewSet, basename="portfolio")
router.register("account", AccountViewSet, basename="account")
router.register("transaction", TransactionViewSet, basename="transaction")
router.register("currency", CurrencyViewSet, basename="currency")
router.register("instrument", InstrumentViewSet, basename="instrument")

urlpatterns = router.urls
