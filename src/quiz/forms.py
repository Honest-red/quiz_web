from django.core.exceptions import ValidationError
from django import forms # noqa
from django.forms import BaseInlineFormSet, modelformset_factory
from django.forms import ModelForm # noqa

from quiz.models import Choice


class ChoicesInlineFormset(BaseInlineFormSet):
    def clean(self):
        # lst = []
        # for form in self.forms:
        #     if form.cleaned_data['is_correct']:
        #         lst.append(1)
        #     else:
        #         lst.append(0)
        # num_correct_answers = sum(lst)

        num_correct_answers = sum([form.cleaned_data['is_correct'] for form in self.forms])
        if num_correct_answers == 0:
            raise ValidationError('Not save if All answer not right')
        if num_correct_answers == len(self.forms):
            raise ValidationError('Not save if All answer right')


class QuestionInlineFormset(BaseInlineFormSet):
    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(f'Num question mast start {self.instance.QUESTION_MIN_LIMIT} '
                                  f'and not be bigger {self.instance.QUESTION_MAX_LIMIT}')
        lst = []
        for form in self.forms:
            position = form.cleaned_data['order_num']
            if position <= len(self.forms) and position-1 in lst or position == 1 and position not in lst:
                lst.append(position)
            else:
                raise ValidationError(f'- Number question mast start with 1 AND don\'t be bigger {len(self.forms)}'
                                      f' AND step +1')


class ChoiceForm(ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['text', ]


ChoicesFormSet = modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
