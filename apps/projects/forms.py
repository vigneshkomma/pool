from django import forms
from .models import Projects, ProjectMember, ProjectLabel

class ProjectForm(forms.ModelForm):
    """
    For creating/editing a project. 'owner' is deliberately excluded —
    it's set in the view from request.user, never from user input.
    """

    class Meta:
        model = Projects
        fields = ('name', 'description', 'status', 'labels')
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }

class ProjectMemberForm(forms.ModelForm):
    """
    For adding a member to a project. 'project' is set in the view from
    the URL, not exposed here. Excludes OWNER from assignable roles —
    ownership is handled separately (transfer-ownership flow), not through
    this generic add-member form.
    """

    role = forms.ChoiceField(
        choices=[c for c in ProjectMember.Role.choices if c[0]!=ProjectMember.Role.OWNER]
    )

    class Meta:
        model = ProjectMember
        fields = ('user', 'role')

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project

    def clean_user(self):
        user = self.cleaned_data['user']
        if self.project and ProjectMember.objects.filter(project=self.project, user=user).exists():
            raise forms.ValidationError('This user is already a member of the project. ')
        return user

class ProjectLabelForm(forms.ModelForm):
    class Meta:
        model = ProjectLabel
        fields = ('name',)



