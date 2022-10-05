from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from set_api.forms import UploadFileForm
from django.core.files.storage import default_storage
from set_api.tasks import process_file


class UploadFileView(generic.CreateView):
    template_name = "set_api/upload_file.html"
    form_class = UploadFileForm
    success_url = reverse_lazy('set_api:upload_file')

    def get_context_data(self, **kwargs):
        context = dict(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            file_name = default_storage.save(file.name, file)
            process_file.delay(file_name=file_name)
            messages.success(request, "File uploaded successfully. We are processing your file")
            return redirect(self.success_url)
        return render(request, self.template_name, context={"form": form})
