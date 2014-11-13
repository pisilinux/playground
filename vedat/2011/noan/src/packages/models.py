# TODO source.packager.name gibi bir kisayol ara.

from django.db import models
from django.contrib.auth.models import User

from django.db.models import Q

from django.utils import translation

class PackageManager(models.Manager):
    def normal(self):
        return self.select_related('arch', 'repo')

class Package(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateField('date published')
    isA = models.ManyToManyField('isA')
    partOf = models.ForeignKey('partOf', related_name='packages')
    license = models.ManyToManyField('License', related_name='packages')
    build_host = models.ForeignKey('BuildHost', related_name='packages')
    distribution = models.ForeignKey('Distribution', related_name='packages')
    architecture = models.ForeignKey('Architecture', related_name='packages')
    installed_size = models.IntegerField()
    package_size = models.IntegerField()
    package_hash = models.CharField(max_length=256)  # FIXME
    package_format = models.CharField(max_length=100)
    # source_name = models.CharField(max_length=255)
    homepage = models.URLField()
    packager = models.ForeignKey(User)
    dependencies = models.ManyToManyField('self', symmetrical=False)
    last_update = models.DateField('last update', null=True)
    pkgbase = models.CharField(max_length=250)

    flag_date = models.DateTimeField(null=True)
    uri = models.CharField(max_length=250)

    package_files = models.TextField(null=True)

    objects = PackageManager()

    @property
    def url(self):
        return "%s/%s/%s" % (self.distribution, self.architecture, self.name)

    def get_absolute_url(self):
        return self.url

    @property
    def last_packager(self):
        packager = Update.objects.filter(package=self)[0].packager
        return packager if packager else self.packager.username

    @property
    def full_version(self):
        return Update.objects.filter(package=self)[0].version

    @property
    def pkgdesc(self):
        lang = translation.get_language()
        try:
            return Description.objects.get(package=self, lang=lang)
        except Description.DoesNotExist:
            return Description.objects.get(package=self, lang='en')

    @property
    def licenses(self):
        return [license.name for license in self.license.all()]

    @property
    def repo(self):
        return self.distribution

    @property
    def flag_date(self):
        return ""

    @property
    def deps(self):
        return [dep.name for dep in self.dependencies.all()]

    @property
    def revdeps(self):
        q = Q(dependencies__name=self.name)&Q(dependencies__architecture=self.architecture)&Q(dependencies__distribution=self.distribution)
        return Package.objects.filter(q)

    @property
    def updates(self):
        return Update.objects.filter(package=self)

    def __unicode__(self):
        return self.name

class Dependency(models.Model):
    pass

class Update(models.Model):
    release = models.IntegerField()
    version = models.CharField(max_length=256)
    comment = models.TextField()
    packager = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    package = models.ForeignKey(Package)
    date = models.DateField()

    @property
    def comment_html(self):
        return self.comment.replace('\n', '<br />')

    def __unicode__(self):
        return "%s_%s" % (self.release, self.version)


class Description(models.Model):
    package = models.ForeignKey(Package)
    lang = models.CharField(max_length=2)
    desc = models.CharField(max_length=1000)

    def __unicode__(self):
        if len(self.desc) > 255:
            return self.desc[:255] + '...'
        return self.desc

class Summary(models.Model):
    package = models.ForeignKey(Package)
    lang = models.CharField(max_length=2)
    sum = models.CharField(max_length=255)

    def __unicode__(self):
        return self.sum

class OneToMany(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        abstract = True

class partOf(OneToMany):
    pass

class isA(OneToMany):
    pass

class License(OneToMany):
    pass

class BuildHost(OneToMany):
    pass

class Distribution(OneToMany):
    pass

class Architecture(OneToMany):
    pass

class XmlHash(models.Model):
    name = models.CharField(max_length=500)
    hash = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s: %s" % (self.name, self.hash)
