from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from blog.models import Post

class Command(BaseCommand):
  help = 'Delete table posts and create new objects'

  def add_arguments(self, parser):
    parser.add_argument('posts_quantity', nargs='+', type=int)

  def handle(self, *args, **options):
    try:
      if options['posts_quantity'][0] < 1:
        raise CommandError('Posts quantity must be greater than 0')

      self.stdout.write(self.style.WARNING('Deleting post objects...'))
      Post.objects.all().delete()
      self.stdout.write(self.style.SUCCESS('Deleting post objects... Done!'))
      fake = Faker()

      self.stdout.write(self.style.WARNING('Creating new objects...'))
      for post in range(1, options['posts_quantity'][0] + 1):
        Post.objects.create(
          id=post, 
          title=fake.paragraph(nb_sentences=2),
          body=fake.paragraph()
        )
      self.stdout.write(self.style.SUCCESS('Creating new objects... Done!'))
    except Exception as message:
      raise CommandError("{}".format(message))
