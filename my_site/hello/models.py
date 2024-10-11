from django.db import models

class Autor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return [self.first_name, self.last_name]

class Book(models.Model):
    book_name = models.CharField(max_length=100)
    year = models.IntegerField(max)
    make_autor = models.ForeignKey(Autor, on_delete=models.CASCADE)

    def __str__(self):
        return [self.book_name, self.year, self.make_autor]
# Create your models hee.
