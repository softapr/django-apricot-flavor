'''
Created on 20 ago. 2019

@author: Francisco Prieto (Orishiku)
'''
import os
import git
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Update apricot-flavor sources from git repository.'
    __path = os.path.join(settings.BASE_DIR, 'apricot-flavor')
    __url = 'https://github.com/softapr/apricot-flavor.git'

    def handle(self, *args, **options):
        if os.path.exists(os.path.join(self.__path,'.git')):
            repo = git.Repo(self.__path)
            origin = repo.remote()
            
            if origin.exists():
                for info in origin.pull():
                    self.stdout.write(self.style.SUCCESS(
                        'Updated %s from %s' % (info.commit, info.ref)))
        
        else:
            repo = git.Repo.clone_from(self.__url, self.__path, branch='master')
            self.stdout.write(self.style.SUCCESS('\n...Cloned %s from %s' % (repo.head.commit, repo.head.ref)))

class ProgressPrinter(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print('%s - %s | %s' % (cur_count, max_count, message or "NO MESSAGE"))
        