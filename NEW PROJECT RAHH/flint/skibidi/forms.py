from django import forms
from .models import Donor,Receiver

class DonorRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        help_text="Enter the same password as above"
    )

    class Meta:
        model = Donor
        fields = ['name', 'email', 'password', 'confirm_password', 'blood_type', 'has_disqualifying_disease']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'has_disqualifying_disease': "Do you have HIV, Hepatitis B/C, or other blood-borne diseases?"
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Simple password match check
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords don't match!")
        
        # Disease check
        if cleaned_data.get('has_disqualifying_disease'):
            raise forms.ValidationError(
                "You cannot register as a donor with your medical condition."
            )
        
        return cleaned_data

    def save(self, commit=True):
        # Save plaintext password (for mini project only)
        donor = super().save(commit=False)
        donor.password = self.cleaned_data['password']
        if commit:
            donor.save()
        return donor
    
class ReceiverRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Receiver
        fields = ['name', 'email', 'password', 'confirm_password', 'blood_type', 'medical_condition']
        widgets = {
            'password': forms.PasswordInput(),
            'medical_condition': forms.Textarea(attrs={'rows': 3})
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords don't match!")
        return cleaned_data

    def save(self, commit=True):
        receiver = super().save(commit=False)
        receiver.password = self.cleaned_data['password']  # Plaintext for demo
        if commit:
            receiver.save()
        return receiver
    
class ReceiverLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'required': 'required'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'required': 'required'
        })
    )