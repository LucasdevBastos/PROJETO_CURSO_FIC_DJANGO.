from django import forms
from .models import Comentario


class ComentarioForm(forms.ModelForm):
    """Form para criar/editar comentários"""
    class Meta:
        model = Comentario
        fields = ('texto', 'nota')
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Compartilhe sua opinião sobre este anime...',
                'rows': 4,
                'maxlength': 2000,
            }),
            'nota': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Nota de 1 a 10 (opcional)',
            }),
        }
        labels = {
            'texto': 'Seu Comentário',
            'nota': 'Nota',
        }
        help_texts = {
            'texto': 'Máximo 2000 caracteres',
            'nota': 'Avalie de 1 a 10 (opcional)',
        }

    def clean_texto(self):
        texto = self.cleaned_data.get('texto', '').strip()
        if len(texto) < 5:
            raise forms.ValidationError("Comentário deve ter no mínimo 5 caracteres")
        if len(texto) > 2000:
            raise forms.ValidationError("Comentário não pode ter mais de 2000 caracteres")
        return texto

    def clean_nota(self):
        nota = self.cleaned_data.get('nota')
        if nota is not None:
            if nota < 1 or nota > 10:
                raise forms.ValidationError("Nota deve estar entre 1 e 10")
        return nota
