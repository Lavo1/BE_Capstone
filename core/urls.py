from rest_framework.routers import DefaultRouter
from .views import CaseViewSet, TimeEntryViewSet, InvoiceViewSet

router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='cases')
router.register(r'time-entries', TimeEntryViewSet, basename='time-entries')
router.register(r'invoices', InvoiceViewSet, basename='invoices')

urlpatterns = router.urls
