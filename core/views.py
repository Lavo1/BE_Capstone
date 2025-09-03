from rest_framework import viewsets, permissions
from .models import Case, TimeEntry, Invoice
from .serializers import CaseSerializer, TimeEntrySerializer, InvoiceSerializer
from .permissions import IsPartnerOrAdmin, CanEditTimeEntry

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [permissions.IsAuthenticated]

class TimeEntryViewSet(viewsets.ModelViewSet):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class TimeEntryViewSet(viewsets.ModelViewSet):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsPartnerOrAdmin | CanEditTimeEntry]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [p() for p in permission_classes]