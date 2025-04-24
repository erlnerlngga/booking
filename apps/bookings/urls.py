from django.urls import path

from apps.bookings.views import BookingListView, BookingView, BookingCreate, BookingUpdate

urlpatterns = [
    path("booking/", BookingListView.as_view(), name="booking-list"),
    path("booking/<str:id>/", BookingView.as_view(), name="booking"),
    path("booking-create/", BookingCreate.as_view(), name="booking-create"),
    path("booking/<str:id>/update", BookingUpdate.as_view(), name="booking-update")
]
