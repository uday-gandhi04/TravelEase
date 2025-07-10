from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import User

from .models import TravelOption, Booking
from .forms import BookingForm, CustomUserCreationForm, UserForm, UserProfileForm



# ---------------- Travel List ---------------- #
class TravelListView(LoginRequiredMixin,generic.ListView):
    model = TravelOption
    template_name = 'bookings/travel_list.html'
    context_object_name = 'travel_options'
    paginate_by = 10
    ordering = ['departure_datetime']
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.GET

        if params.get('type'):
            queryset = queryset.filter(type=params['type'])
        if params.get('source'):
            queryset = queryset.filter(source__icontains=params['source'])
        if params.get('dest'):
            queryset = queryset.filter(destination__icontains=params['dest'])
        if params.get('date'):
            queryset = queryset.filter(datetime__date=params['date'])

        return queryset

# ---------------- Travel Booking ---------------- #
class BookView(LoginRequiredMixin, generic.FormView):
    form_class = BookingForm
    template_name = 'bookings/book_travel.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['travel_option'] = get_object_or_404(TravelOption, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        travel = get_object_or_404(TravelOption, pk=self.kwargs['pk'])
        seats = form.cleaned_data['seats']

        if seats > travel.available_seats:
            form.add_error('seats', 'Not enough seats available.')
            return self.form_invalid(form)

        Booking.objects.create(
            user=self.request.user,
            travel=travel,
            seats=seats,
            total_price=seats * travel.price
        )

        travel.available_seats -= seats
        travel.save()

        return redirect('bookings:my_bookings')

# ---------------- View My Bookings ---------------- #
class MyBookingsView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'
    login_url = 'login'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

# ---------------- Cancel Booking ---------------- #
class CancelBookingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user, status='confirmed')
        booking.status = 'cancelled'
        booking.travel.available_seats += booking.seats
        booking.travel.save()
        booking.save()
        return redirect('bookings:my_bookings')

# ---------------- Optional Direct Booking ---------------- #
def book_travel(request, travel_id):
    travel = get_object_or_404(TravelOption, id=travel_id)
    return render(request, 'bookings/book_travel.html', {'travel': travel})

# ---------------- Register ---------------- #
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # ✅ Redirects to login after signup
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})



# ---------------- Profile View ---------------- #
@login_required
def profile_view(request):
    return render(request, "registration/profile.html")

# ---------------- Edit Profile ---------------- #
@login_required
def profile_edit(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("bookings:profile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, "registration/profile_update.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })

from .forms import ProfileUpdateForm

# ---------------- Profile Update View ---------------- #
class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('bookings:profile')
    login_url = 'login'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ✅ Pass user to form
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.user.userprofile.save()
        return response
    

# ---------------- Profile View ---------------- #
class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user'
    login_url = 'login'

    def get_object(self, queryset=None):
        return self.request.user
#     # This will return the currently logged-in user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.userprofile
        return context  

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # or use your landing page URL name


