from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from announcements.models import Announcement

def str_announcement(a):
    return '%d: %s - %s' % (a.pk, a.title, a.content)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-l', '--list', dest='list',
                    action='store_true', default=False,
                    help='List current announcements.'),
        make_option('-d', '--delete', dest='delete',
                    help='The title or pk of the announcement to delete.'),
    )
    help = 'Create, delete, or list announcements.'
    args = '[title, content]'

    def handle(self, *args, **options):
        # List existing announcements.
        if options.get('list'):
            announcements = Announcement.objects.all()
            if announcements:
                for a in announcements:
                    print str_announcement(a)
            else:
                print 'No announcements exist.'
            return

        # Delete an announcement.
        delete = options.get('delete')
        if delete:
            for field in ['pk', 'title__iexact']:
                try:

                    a = Announcement.objects.get(**{field: delete})
                    s = str_announcement(a)
                    a.delete()
                    print 'Deleted announcement:'
                    print s
                    return
                except (ValueError, Announcement.DoesNotExist):
                    pass
            raise CommandError('The announcement with title or PK "%s" does not exist.' % delete)

        # Create an announcement.
        try:
            title, content = args
        except ValueError:
            raise CommandError('To create an announcement, you must specify the title and content.')
        try:
            admin = User.objects.filter(is_superuser=True)[0]
        except IndexError:
            raise CommandError('Please create a superuser account in order to make announcements.')

        a = Announcement.objects.create(
            title=title,
            content=content,
            creator=admin,
            site_wide=True,
        )
        print 'Created announcement:'
        print str_announcement(a)
