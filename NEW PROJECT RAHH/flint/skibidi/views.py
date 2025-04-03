from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Donor
from .models import Receiver
from .forms import ReceiverRegistrationForm  # You'll need to create this
from django.shortcuts import render, redirect
from .forms import DonorRegistrationForm
from .forms import ReceiverLoginForm

def register_donor(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            donor = form.save()  # This will handle password and validation
            request.session['donor_id'] = donor.id
            return redirect('donor_login')  # Redirect to dashboard after registration
    else:
        form = DonorRegistrationForm()
    
    return render(request, 'register_donor.html', {'form': form})

def donor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            donor = Donor.objects.get(email=email, password=password)
            request.session['donor_id'] = donor.id
            return redirect('donor_dashboard')
        except Donor.DoesNotExist:
            return render(request, 'donor_login.html', 
                        {'error': 'Invalid email or password'})
    
    return render(request, 'donor_login.html')

def donor_dashboard(request):
    if 'donor_id' not in request.session:
        return redirect('donor_login')
    
    try:
        donor = Donor.objects.get(id=request.session['donor_id'])
        return render(request, 'donor_dashboard.html', {'donor': donor})
    except Donor.DoesNotExist:
        return redirect('donor_login')
    

def update_donor(request):
    if 'donor_id' not in request.session:
        return redirect('donor_login')
    
    if request.method == 'POST':
        donor = Donor.objects.get(id=request.session['donor_id'])
        has_disease = request.POST.get('has_disqualifying_disease') == 'true'
        
        if has_disease and not donor.has_disqualifying_disease:
            donor.delete()
            request.session.flush()
            messages.success(request, 'Account removed due to medical ineligibility')
            return redirect('home')
        
        donor.has_disqualifying_disease = has_disease
        donor.save()
        return redirect('donor_dashboard')
    
    return redirect('donor_dashboard')


def donor_logout(request):
    request.session.flush()
    return redirect('home')

def home(request):
    return render(request, 'home.html')

def receiver_register(request):
    if request.method == 'POST':
        form = ReceiverRegistrationForm(request.POST)
        if form.is_valid():
            receiver = form.save(commit=False)
            receiver.password = form.cleaned_data['password']  # Plaintext for demo
            receiver.save()
            request.session['receiver_id'] = receiver.id
            messages.success(request, 'Registration successful!')
            return redirect('receiver_login')
    else:
        form = ReceiverRegistrationForm()
    
    return render(request, 'receiver_register.html', {'form': form})

def receiver_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            receiver = Receiver.objects.get(email=email, password=password)
            request.session['receiver_id'] = receiver.id
            request.session['receiver_email'] = receiver.email
            return redirect('receiver_dashboard')
        except Receiver.DoesNotExist:
            return render(request, 'receiver_login.html', {
                'error': 'Invalid email or password',
                'email': email  # Preserve the email in the form
            })
    
    return render(request, 'receiver_login.html')

def receiver_dashboard(request):
    if 'receiver_id' not in request.session:
        return redirect('receiver_login')
    
    donors = Donor.objects.filter()
    return render(request, 'receiver_dashboard.html', {'donors': donors})

def book_appointment(request):
    # Check if receiver is logged in (if you want this check)
    if 'receiver_id' not in request.session:
        return redirect('receiver_login')
    
    if request.method == 'POST':
        donor_email = request.POST.get('email')
        
        try:
            # Find and delete the donor
            donor = Donor.objects.get(email=donor_email)
            donor.delete()
            messages.success(request, 'Appointment booked! Donor removed.')
            return redirect('receiver_dashboard')
            
        except Donor.DoesNotExist:
            messages.error(request, 'Donor not found')
            return redirect('receiver_dashboard')

    return redirect('receiver_dashboard')


def receiver_logout(request):
    request.session.flush()
    return redirect('home')