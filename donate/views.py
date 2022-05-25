from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from donate.forms import RegisterForm, LoginForm, DonationForm
from donate.models import Donation, User, Institution, Category


class LandingPageView(View):  # HomePage View
    def get(self, request):
        bags = Donation.objects.all().aggregate(Sum('quantity'))
        bags_total = bags['quantity__sum']
        # institutions = Institution.objects.all().aggregate(Count('donation', distinct=True))
        # donated_institutions = institutions['donation__count']
        donated_institutions = len(set([x.institution for x in Donation.objects.all()]))

        foundations = Institution.objects.all().filter(type=0)
        ngo = Institution.objects.all().filter(type=1)
        loc_collections = Institution.objects.all().filter(type=2)

        return render(request, 'index.html', context={'bags_total': bags_total,
                                                      'donated_institutions': donated_institutions,
                                                      'foundations': foundations,
                                                      'ngo': ngo,
                                                      'loc_collections': loc_collections,
                                                      })


class FormView(LoginRequiredMixin, View):  # Add Donation View
    def get(self, request):
        form = DonationForm()
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        print(categories)
        return render(request, 'form.html', context={'form': form,
                                                     'categories': categories,
                                                     'institutions': institutions})


    def post(self, request):
        form = DonationForm(request.POST)
        # breakpoint()
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        if form.is_valid():
            category_id = form.cleaned_data.get('categories')
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()
            donation.categories.add(category_id)
            return redirect('confirm')

        return render(request, 'form.html', context={'form': form,
                                                     'categories': categories,
                                                     'institutions': institutions})



class FormConfirmView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class LoginView(View):  # Login View
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing_page')
            else:
                return render(request, 'register.html')


class RegisterView(View):  # Register View
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        errors = []
        if form.is_valid():
            first_name = form.cleaned_data.get('name')
            last_name = form.cleaned_data.get('surname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')
            if not password == password2:
                errors.append(("Podane hasła nie są takie same, spróbuj ponownie!"))
            if len(errors) == 0:
                User.objects.create_user(first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    password=password)
                return redirect(reverse('login'))
            return render(request, 'register.html', context={'errors': errors})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')


class ProfileView(View):
    def get(self, request):
        user = request.user
        return render(request, 'profile.html', context={'user': user})


class MyDonationsView(View):
    def get(self, request):
        user = request.user
        donations = user.donation_set.all()
        return render(request, 'my_donations.html', context={'donations': donations})
