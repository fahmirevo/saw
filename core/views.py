from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from core import forms
import numpy as np
import pandas as pd

# Create your views here.

class HomePageView(TemplateView):

    template_name = 'core/index.html'
    form_class = forms.MainForm

    @property
    def reference_index(self):
        return np.array([
            "Asus A455LA",
            "Asus X441UV",
            "Asus VIVOBOOK",
            "Asus Zenbook",
        ])

    @property
    def reference_header(self):
        return np.array([
            "Speed Processor",
             "VGA",
            "Layar",
            "RAM",
            "Jenis HD",
            "Harga",
        ])

    @property
    def reference_header_function(self):
        return np.array([max, max, max, max, max, min])

    @property
    def reference_data(self):
        return np.array([
            [8, 2, 7, 8, 7.5, 10],
            [8, 2, 6, 9, 8, 6],
            [10, 7, 7, 10, 9, 5],
            [5, 6, 5, 4, 7, 10],
        ], dtype=float)

    # def get_weights(self):
    #     form = forms.MainForm(request.GET)
    #     if form.is_valid():
    #         choice = form.cleaned_data['case']

    #         if case == 1:
    #             return np.array([[7.5, 2.5, 5.0, 7.0, 5.0, 0.0]])
    #         elif case == 2:
    #             return np.array([[7.5, 2.5, 5.0, 3.5, 5.0, 6.125]])
    #         elif case == 3:
    #             return np.array([[10.0, 10.0, 5.0, 10.0, 5.0, 6.125]])
    #         elif case ==

    def solve(self):
        form = forms.MainForm(self.request.GET)
        if form.is_valid():
            case = form.cleaned_data['case']

            if case == "0":
                focus = [0, 3, 5]
                weights = np.array([0.6, 0.6, 10.0])
            elif case == "1":
                focus = [0, 3, 5]
                weights = np.array([0.4, 0.4, 0.375])
            elif case == "2":
                focus = list(range(6))
                weights = np.array([10., 10., 7.5, 9.0, 6.0, 0.375])
            else:
                focus = [0, 3, 4]
                weights = np.array([0.3, 0.4, 0.7])

            focus_table = self.reference_data[:, focus]
            focus_header = self.reference_header[focus]
            normalized_table = np.zeros(focus_table.shape)
            for enu, col in enumerate(focus):
                f = self.reference_header_function[col]
                val = f(focus_table[:, enu])
                if f is max:
                    normalized_table[:, enu] = focus_table[:, enu] / val
                else:
                    normalized_table[:, enu] = val / focus_table[:, enu]

            score = np.sum(normalized_table * weights, axis=1)
            wut = np.max(score)
            suggestion = np.argmax(score)
            index = self.reference_index
            return {
                'case': case,
                'focus': focus,
                'weights': pd.DataFrame(weights[np.newaxis], columns=focus_header),
                'table': pd.DataFrame(self.reference_data, index=index, columns=self.reference_header),
                'focus_table': pd.DataFrame(focus_table, index=index, columns=focus_header),
                'normalized_table': pd.DataFrame(normalized_table, index=index, columns=focus_header),
                'score': pd.DataFrame(score[:, np.newaxis], index=index, columns=['skor']),
                'suggestion': index[suggestion],
            }
        return {'errors': form.errors}


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {**context, **self.solve(), 'form': forms.MainForm}
        return context
