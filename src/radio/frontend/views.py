import subprocess
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from rest_framework.reverse import reverse
from django.views.generic import ListView

from radio.entities.models import Station
from radio.frontend.forms.youtube import YoutubeForm


class HomeView(ListView):
    model = Station
    template_name = "index.html"

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, **kwargs)
        return HttpResponse(
            status=401,
            content='<div>Unauthenticated!</div>'
                    '<div>Click <a href={}> here </a> to login</div>'.format(
                request.build_absolute_uri('/admin/login/?next={}'.format(
                    request.get_full_path()
                ))
            ))
    @staticmethod
    def find_between(s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    @staticmethod
    def system_do(args, split=True):
        if split:
            args = args.split(' ')
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        return process.communicate()[0]

    def get_context_data(self, **kwargs):
        form = YoutubeForm()
        context = super().get_context_data()
        context['form'] = form
        return context

    def post(self, request, **kwargs):
        form = YoutubeForm(data=request.POST)
        if form.is_valid():
            url = form.data['youtube_url']

            out, err, *junk = self.system_do(
                "youtube-dl {} -x --audio-format mp3".format(url))
            filename = self.find_between(str(out), 'Destination:', '.mp3')
            try:
                filename = filename[filename.index('Destination:')+13:]
            except ValueError:
                print(filename)
                pass
            print("filename: {}.mp3".format(filename))
            self.system_do(
                ["sudo", "mv", "{}.mp3".format(filename), "/mnt/music"], split=False
            )
            print('moved to /mnt/music')
            self.system_do("mpc clear")
            self.system_do("mpc update")
            self.system_do(
                ["mpc", "add", "music/{}.mp3".format(filename)], split=False)
            self.system_do("mpc play")
            print('Playing')

        return HttpResponseRedirect(reverse('home'))
