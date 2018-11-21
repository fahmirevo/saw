from django import forms

class MainForm(forms.Form):

    case = forms.ChoiceField(
        label='case',
        choices=(
            (0, "Tomcat Web Developer"),
            (1, "VSCODE Web Developer"),
            (2, "Mobile Developer"),
            (3, "Non-IT"),
        )
    )
