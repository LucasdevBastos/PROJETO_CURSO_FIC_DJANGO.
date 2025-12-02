from django import forms
from .models import Perfil


class PerfilForm(forms.ModelForm):
    """Form para editar perfil do usuário"""
    class Meta:
        model = Perfil
        fields = ('avatar', 'bio')
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Conte-nos um pouco sobre você...',
                'rows': 3,
                'maxlength': 500,
            }),
        }
        labels = {
            'avatar': 'Avatar',
            'bio': 'Biografia',
        }
        help_texts = {
            'bio': 'Máximo 500 caracteres',
        }

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '').strip()
        if len(bio) > 500:
            raise forms.ValidationError("Biografia não pode ter mais de 500 caracteres")
        return bio
