from django import forms
from .models import *
class LoginForm(forms.ModelForm):
    class Meta:
        # 指定关联的Model
        model = Users
        # 指定要生成的控件的属性们
        fields = ['uphone','upwd']
        # 指定控件对应的标签
        labels = {
            'uphone':'手机号',
            'upwd':'密码',
        }
        # 指定控件对应的小部件
        widgets = {
            'uphone':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'输入用户名',
                    'id':'uphone',
                }
            ),
            'upwd':forms.PasswordInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'输入密码',
                    'id':'upwd',
                }
            )
        }