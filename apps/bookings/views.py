from django.shortcuts import render, redirect
from django.views.generic import ListView, View

from apps.bookings.models import Booking
from apps.employees.models import Employee, EmployeeSetting
from core.views import LoginRequiredMixinView
from .tasks import process_send_email_task


# Create your views here.
class BookingListView(LoginRequiredMixinView, ListView):
    model = Booking
    template_name = "booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        user_setting = EmployeeSetting.objects.get(actor=self.request.user)

        if user_setting.role == "admin":
            return Booking.objects.all()

        return Booking.objects.filter(actor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employee = Employee.objects.filter(actor=self.request.user).first()
        user_setting = EmployeeSetting.objects.get(actor=self.request.user)
        booking_approved = Booking.objects.filter(status='approved').count()
        booking_pending = Booking.objects.filter(status='pending').count()
        booking_rejected = Booking.objects.filter(status='rejected').count()

        context["employee"] = employee
        context["user_setting"] = user_setting
        context["booking_approved"] = booking_approved
        context["booking_pending"] = booking_pending
        context["booking_rejected"] = booking_rejected

        return context


class BookingView(LoginRequiredMixinView, View):
    def get(self, request, id):
        user_setting = EmployeeSetting.objects.get(actor=self.request.user)
        booking = Booking.objects.get(id=id)
        return render(request, "booking.html", {"user_setting": user_setting, "booking": booking})

class BookingCreate(LoginRequiredMixinView, View):
    def get(self, request):
        user_setting = EmployeeSetting.objects.get(actor=self.request.user)
        return render(request, "booking-create.html", {"user_setting": user_setting})

    def post(self, request):
        from_city = request.POST.get("from_city")
        to_city = request.POST.get("to_city")
        departure_date = request.POST.get("departure_date")
        passenger_name = request.POST.get("passenger_name")
        passenger_id = request.POST.get("passenger_id")
        passenger_email = request.POST.get("passenger_email")
        job_title = request.POST.get("job_title")
        department = request.POST.get("department")
        company = request.POST.get("company")
        site = request.POST.get("site")

        Booking.objects.create(
            from_city=from_city,
            to_city=to_city,
            departure_date=departure_date,
            passenger_name=passenger_name,
            passenger_id=passenger_id,
            passenger_email=passenger_email,
            job_title=job_title,
            department=department,
            company=company,
            site=site,
            actor=request.user
        )

        return redirect("booking-list")
    
class BookingUpdate(LoginRequiredMixinView, View):
    def post(self, request, id):
        price = request.POST.get("price")
        ticket = request.FILES.get("ticket")
        status = request.POST.get("status")

        booking = Booking.objects.get(id=id)

        if price:
            booking.price = price
        
        if ticket:
            booking.ticket = ticket

        if status: 
            booking.status = status

        if price or ticket or status:    
            booking.save()


        if status == 'approved':
            process_send_email_task(id=id)

        return redirect("booking", id=id)


