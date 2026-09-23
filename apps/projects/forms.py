from django import forms
from django.contrib.auth import get_user_model
from .models import Projects, ProjectMember, ProjectLabel

class ProjectForm(forms.ModelForm):
    """
    For creating/editing a project. 'owner' is deliberately excluded —
    it's set in the view from request.user, never from user input.
    """

    labels_text = forms.CharField(
        required=False,
        label='Labels',
        help_text='Separate labels with commas, for example: design, launch',
    )

    class Meta:
        model = Projects
        fields = ('name', 'description', 'status')
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['labels_text'].initial = ', '.join(self.instance.labels.values_list('name', flat=True))

    def save(self, commit=True):
        project = super().save(commit=False)
        label_names = {name.strip() for name in self.cleaned_data['labels_text'].split(',') if name.strip()}

        def save_labels():
            labels = [ProjectLabel.objects.get_or_create(name=name)[0] for name in label_names]
            project.labels.set(labels)

        if commit:
            project.save()
            save_labels()
        else:
            self.save_m2m = save_labels
        return project

class ProjectMemberForm(forms.ModelForm):
    """
    For adding a member to a project. 'project' is set in the view from
    the URL, not exposed here. Excludes OWNER from assignable roles —
    ownership is handled separately (transfer-ownership flow), not through
    this generic add-member form.
    """

    username = forms.CharField(
        label='Username',
        help_text='Enter the exact username of the person you want to invite.',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. alex'}),
    )
    role = forms.ChoiceField(
        choices=[c for c in ProjectMember.Role.choices if c[0]!=ProjectMember.Role.OWNER]
    )

    class Meta:
        model = ProjectMember
        fields = ('role',)

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        user = get_user_model().objects.filter(username__iexact=username).first()
        if user is None:
            raise forms.ValidationError('No account was found with that username.')
        if self.project and ProjectMember.objects.filter(project=self.project, user=user).exists():
            raise forms.ValidationError('This user is already a member of the project.')
        self.selected_user = user
        return username

class ProjectLabelForm(forms.ModelForm):
    class Meta:
        model = ProjectLabel
        fields = ('name',)


