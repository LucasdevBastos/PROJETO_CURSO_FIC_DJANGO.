from django import forms
from .models import Perfil


class PerfilForm(forms.ModelForm):
    """
    Form para editar perfil do usuário
    
    Regras:
    - Todos podem escolher avatar_choice (avatares padrão)
    - Apenas VIP pode usar custom_avatar e custom_banner
    """
    class Meta:
        model = Perfil
        fields = ('avatar_choice', 'bio', 'custom_avatar', 'custom_banner')
        widgets = {
            'avatar_choice': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Conte-nos um pouco sobre você...',
                'rows': 3,
                'maxlength': 500,
            }),
            'custom_avatar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL do avatar personalizado (apenas VIP)',
            }),
            'custom_banner': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL do banner personalizado (apenas VIP)',
            }),
        }
        labels = {
            'avatar_choice': 'Avatar Padrão',
            'bio': 'Biografia',
            'custom_avatar': 'Avatar Personalizado (VIP)',
            'custom_banner': 'Banner Personalizado (VIP)',
        }
        help_texts = {
            'bio': 'Máximo 500 caracteres',
            'avatar_choice': 'Escolha um dos avatares padrão disponíveis',
            'custom_avatar': 'Apenas para usuários VIP',
            'custom_banner': 'Apenas para usuários VIP',
        }

    def __init__(self, *args, **kwargs):
        """
        Customiza o formulário baseado no status VIP do usuário
        """
        super().__init__(*args, **kwargs)
        
        # Se o usuário não for VIP, remover campos personalizados
        if self.instance and not self.instance.is_vip:
            self.fields.pop('custom_avatar', None)
            self.fields.pop('custom_banner', None)

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '').strip()
        if len(bio) > 500:
            raise forms.ValidationError("Biografia não pode ter mais de 500 caracteres")
        return bio
    
    def clean(self):
        """
        Validação adicional para garantir que não-VIP não possam definir campos personalizados
        """
        cleaned_data = super().clean()
        
        # Se o usuário não for VIP, limpar campos personalizados
        if self.instance and not self.instance.is_vip:
            cleaned_data['custom_avatar'] = None
            cleaned_data['custom_banner'] = None
        
        return cleaned_data

