from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
import random
from django.contrib.auth import logout
import pickle
import os
from django.http import HttpResponseNotFound

from django.core.mail import send_mail
from django.conf import settings


# Create your views here.


def index(request):
    return render(request, 'user/index.html')


def about(request):
    return render(request, 'user/about.html')


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            messages.success(request, 'Login Successful')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid details !')
            return redirect('admin_login')
    return render(request, 'user/admin-login.html')


def contact(request):
    return render(request, 'user/contact.html')


def services(request):
    return render(request, 'user/service.html')


def UserLogin(req):
    if req.method == 'POST':
        Email = req.POST.get('email')
        Password = req.POST.get('password')
        print(Email, Password)

        user_data = User.objects.get(Email=Email)
        print(user_data)
        if user_data.Password == Password:
            # if user_data.User_Status=='accepted':
            req.session['User_id'] = user_data.User_id
            messages.success(req, 'You are logged in..')
            user_data.No_Of_Times_Login += 1
            user_data.save()
            return redirect('user_dashboard')

        else:
            # messages.warning(req, 'verifyOTP...!')
            req.session['Email'] = user_data.Email
            # return redirect('otpverify')
    else:
        messages.error(req, 'incorrect credentials...!')
        return render(req, 'user/user-login.html')

    return render(req, 'user/user-login.html')


def user_dashboard(request):
    return render(request, 'user/user-dashboard.html')


def user_profile(request):
    user_id = request.session['user_id']
    print(user_id)
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            profile = request.FILES['profile']
            user.user_profile = profile
        except MultiValueDictKeyError:
            profile = user.user_profile
        password = request.POST.get('password')
        location = request.POST.get('location')
        user.user_name = name
        user.user_email = email
        user.user_phone = phone
        user.user_password = password
        user.user_location = location
        user.save()
        messages.success(request, 'updated succesfully!')
        return redirect('user_profile')
    return render(request, 'user/user-profile.html', {'user': user})


def generate_otp(length=4):
    otp = ''.join(random.choices('0123456789', k=length))
    return otp


def UserRegister(req):
    if req.method == 'POST':
        name = req.POST.get('myName')
        age = req.POST.get('myAge')
        password = req.POST.get('myPwd')
        phone = req.POST.get('myPhone')
        email = req.POST.get('myEmail')
        address = req.POST.get("address")
        image = req.FILES['image']
        print(name, age, password, phone, email, address, image)
        image = req.FILES['image']
        number = random.randint(1000, 9999)

        print(number)
        # try:
        #     user_data = User.objects.get(Email = email)
        #     if user_data!=None:
        #         messages.warning(req, 'Email was already registered, choose another email..!')
        #         return redirect("register")
        # except:
        # sendSMS(name,number,phone)
        User.objects.create(Full_name=name, Image=image, Age=age,
                            Password=password, Address=address, Email=email, Phone_Number=phone)
        mail_message = f'Registration Successfully\n Your 4 digit Pin is below\n {number}'
        print(mail_message)
        send_mail("User Password", mail_message,
                  settings.EMAIL_HOST_USER, [email])
        req.session['Email'] = email
        messages.success(req, 'Your account was created..')
        # return redirect('otpverify')
    return render(req, 'user/user-register.html')


def user_logout(request):
    logout(request)
    return redirect('user_login')


def student(request):
    status = ""
    predicted_status = ""
    predicted_salary = 0
    formatted_salary = 0

    if request.method == 'POST':
        gender = 1 if request.POST.get('gender') == 'Male' else 0
        print(f'Gender: {gender}')

        ssc_p = float(request.POST.get('ssc_p', 0))
        print(f'SSC Percentage: {ssc_p}')

        hsc_p = float(request.POST.get('hsc_p', 0))
        print(f'HSC Percentage: {hsc_p}')

        hsc_s = request.POST.get('hsc_s', '')
        if hsc_s == 'Arts':
            hsc_s_numeric = 0
        elif hsc_s == 'Commerce':
            hsc_s_numeric = 1
        elif hsc_s == 'Science':
            hsc_s_numeric = 2
        else:
            hsc_s_numeric = -1

        degree_p = float(request.POST.get('degree_p', 0))
        print(f'Degree Percentage: {degree_p}')

        degree_t = request.POST.get('degree_t', '')
        if degree_t == 'Comm&Mgmt':
            degree_t_numeric = 0
        elif degree_t == 'Sci&Tech':
            degree_t_numeric = 2
        elif degree_t == 'Others':
            degree_t_numeric = 1
        else:
            degree_t_numeric = -1

        workex = 1 if request.POST.get('workex') == 'Yes' else 0
        print(f'Work Experience: {workex}')

        etest_p = float(request.POST.get('etest_p', 0))
        print(f'E-Test Percentage: {etest_p}')

        specialisation = 1 if request.POST.get(
            'specialisation') == 'Mkt&Fin' else 0
        print(f'Specialization: {specialisation}')

        mba_p = float(request.POST.get('mba_p', 0))
        print(f'MBA Percentage: {mba_p}')

        # salary = float(request.POST.get('Status', 0))
        # print(f'Salary: {salary}')

        with open('rfc_placement.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)

        feature_vector = [gender, ssc_p, hsc_p, hsc_s_numeric, degree_p,
                          degree_t_numeric, workex, etest_p, specialisation, mba_p]

        predicted_status = loaded_model.predict([feature_vector])
        print(predicted_status)

        if predicted_status[0] == 1:

            with open('rfr_placement.pkl', 'rb') as salary_model_file:
                salary_model = pickle.load(salary_model_file)

            feature_vector_salary = [gender, ssc_p, hsc_p, hsc_s_numeric, degree_p,
                                     degree_t_numeric, workex, etest_p, specialisation, mba_p, predicted_status[0]]

            predicted_salary = salary_model.predict([feature_vector_salary])[0]

            formatted_salary = "{:.0f}L {:.0f}k".format(
                predicted_salary // 100000, (predicted_salary % 100000) // 1000)

            status = 'Placed'
        else:
            status = 'Not Placed'

    return render(request, 'user/student.html', {
        'status': status,
        'predicted_status': predicted_status,
        'predicted_salary': formatted_salary
    })


def forgot_password(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        if phone == "":
            messages.warning(request, 'Enter Number')
        else:
            try:
                user = User.objects.get(user_phone=phone)
                if user.status == "Accepted":
                    subject = "Password Reminder"
                    message = f"Your password is: {user.user_password}"
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.user_email]

                    send_mail(subject, message, from_email, recipient_list)

                    messages.info(
                        request, "Your password has been sent to your email.")
                    request.session['user_id'] = user.user_id
                    return redirect('user_login')
                else:
                    messages.warning(request, 'You are not registered yet!')
                    return redirect('forgot')
            except User.DoesNotExist:
                messages.warning(request, 'You are not registered yet!')
                return redirect('forgot')
    return render(request, 'user/forgot-password.html')


def otp(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    if request.method == "POST":
        otp_entered = request.POST.get('otp')
        print(otp_entered)
        user_id = request.session['user_id']
        print(user_id)
        try:
            user = User.objects.get(user_id=user_id)
            if user.status == "Accepted":
                user_pass = user.user_password
                print(user_pass)
                messages.info(request, 'Your password is : ' + user_pass)
                return redirect('user_login')

            elif str(user.otp) == otp_entered:
                messages.success(
                    request, 'OTP verification  and Registration is  Successfully!')
                user.status = "Verified"
                user.save()
                return redirect('user_login')

            else:
                messages.error(request, 'Invalid OTP entered')
                print("Invalid OTP entered")
                return redirect('otp')

        except User.DoesNotExist:
            messages.error(request, 'Invalid user')
            print("invalid user")
            return redirect('user_register')
    return render(request, 'user/otp.html')
