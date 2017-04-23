from django.core.management.base import BaseCommand, CommandError

from ask.models import Question, Tag

from random import choice, randint
import os

class Command(BaseCommand):
	help = 'Fill tags'

	def add_arguments(self, parser):
		parser.add_argument('--number',
            action='store',
            dest='number',
            default=3,
            help='Number of tags for a question'
    	)

	def handle(self, *args, **options):
		tags = [
			'javascript', 'java', 'c#', 'php', 'android', 'jquery', 'python',
			'html', 'css', 'c++', 'ios', 'mysql', 'objective-c', 'sql', 'asp.net',
			'ruby-on-rails', 'iphone', 'angularjs', 'regexp'
		]

		number = int(options['number'])
		for i in range(0, number):
			t = Tag()
			t.title = choice(tags) + str(i)
			t.save()  
    
