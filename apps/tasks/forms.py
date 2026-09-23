from django import forms
from .models import Tasks, Subtasks, Comment, TaskLabel

class TaskForm(forms.ModelForm):
    """
    For creating/editing a task. 'project' and 'created_by' are excluded —
    both are set in the view from URL/request context, never user input.
    """

    labels_text = forms.CharField(
        required=False,
        label='Labels',
        help_text='Separate labels with commas, for example: bug, customer request',
    )

    class Meta:
        model = Tasks
        fields = ('title', 'description', 'status', 'priority', 'assignee', 'due_date')
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project

        if project is not None:
            self.fields['assignee'].queryset = project.members.all()
        if self.instance.pk:
            self.fields['labels_text'].initial = ', '.join(self.instance.labels.values_list('name', flat=True))

    def save(self, commit=True):
        task = super().save(commit=False)
        label_names = {name.strip() for name in self.cleaned_data['labels_text'].split(',') if name.strip()}

        def save_labels():
            labels = [TaskLabel.objects.get_or_create(name=name)[0] for name in label_names]
            task.labels.set(labels)

        if commit:
            task.save()
            save_labels()
        else:
            self.save_m2m = save_labels
        return task

class SubtaskForm(forms.ModelForm):
    """
    'task' is excluded — set in the view from the URL.
    """
    class Meta:
        model = Subtasks
        fields = ('title', 'is_completed')


class CommentForm(forms.ModelForm):
    """
    'task' and 'author' are excluded — set in the view from URL/request.user.
    """

    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }


class TaskLabelForm(forms.ModelForm):
    class Meta:
        model = TaskLabel
        fields = ('name',)














