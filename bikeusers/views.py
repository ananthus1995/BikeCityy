from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.views.generic import View,TemplateView,CreateView,RedirectView,FormView,ListView,DetailView
from django.urls import reverse_lazy
from bikeusers.forms import SignupForm,token_generator,LoginForm,PostBikeForm
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import login,authenticate
from django.contrib.auth.views import LoginView
from bikeusers.models import Bikes,BikeImages,InterestedBikes




class UserHome(TemplateView):
    template_name = 'user_home.html'
    model=Bikes
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_bikes = self.model.objects.exclude(added_user=self.request.user).order_by("-id")
        paginator = Paginator(all_bikes, 6)
        page_number = self.request.GET.get('page')
        print(page_number)
        bikes_list = paginator.get_page(page_number)
        context['bikes_list'] = bikes_list
        print(context)
        return context

class BikeDetailView(DetailView):
    template_name = 'bike_detail.html'
    model = Bikes
    context_object_name = 'bike_detail'
    pk_url_kwarg = 'bike_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bike_images = BikeImages.objects.filter(bikes=self.kwargs.get('bike_id'))
        sts = InterestedBikes.objects.filter(bike=self.kwargs.get('bike_id'))
        context['bike_int_status'] = sts
        context['bike_more_images'] = bike_images
        return context





def makeoffer(request,*args,**kwargs):
     bikes_id= kwargs.get('bike_id')
     bike = Bikes.objects.get(id=bikes_id)
     bike_owner= bike.added_user
     interested_by= request.user
     InterestedBikes.objects.create(bike=bike, users=interested_by, owner=bike_owner,status='Interested')
     return redirect('bike_details', bike_id=bikes_id)





class SignUp(CreateView):
    template_name = 'signup.html'
    model = User
    form_class =SignupForm
    success_url = reverse_lazy('check_email')

    def form_valid(self, form):
        to_return = super().form_valid(form)

        user = form.save()
        user.is_active = False  # Turns the user status to inactive
        user.save()

        form.send_activation_email(self.request, user)

        return to_return

class ActivateView(RedirectView):

    url = reverse_lazy('success')

    # Custom get method
    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(request, 'activate_account_invalid.html')

class CheckEmailView(TemplateView):
    template_name = 'check_email.html'

class SuccessView(TemplateView):
    template_name = 'success.html'

class SigninView(FormView):
    template_name = 'user_login.html'
    form_class = LoginForm

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=password)
            # print(user)
            if user:

                if user.is_active:
                    login(request, user)
                    return redirect('user_home')
                else:

                    return render(request,self.template_name,{'form': form,'errmsg1':'Inactive Account.Check Your Email and activate using the link'})
            else:
                return render(request, self.template_name, {'form': form, 'errmsg': 'Incorrect username or password'})
        else:
            return render(request, self.template_name, {'form': form, 'errmsg': 'Incorrect username or password'})



class Post_BikeView(CreateView):
    template_name = "post_bike.html"
    form_class = PostBikeForm
    model = Bikes
    success_url = reverse_lazy("user_home")
    def form_valid(self, form):
        form.instance.added_user = self.request.user
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            BikeImages.objects.create(bikes=p, image=i)
        return super().form_valid(form)








