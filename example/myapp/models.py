from django.db import models


class Thing(models.Model):
    """
    A sample thing that will hold stuff. If you want to try this out, add a new
    mapping in the admin using http://rich.io/985t as the source, Atom as the parser,
    and the following JSON as the data map::

        {
          "models": {
            "myapp.Thing": {
              "nodePath": "atom:entry",
              "identifier": "atom:id",
              "fields": {
                "atom_id": "atom:id",
                "title": "atom:title",
                "link": "atom:link",
                "summary": "atom:summary",
                "content": "atom:content"
              }
            }
          }
        }
    """
    atom_id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True, verify_exists=False)
    summary = models.TextField()
    content = models.TextField()

    def __unicode__(self):
        return self.title
