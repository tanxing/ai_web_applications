from django.db import models
from sentence_transformers import SentenceTransformer

class Recipe(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField()
  ingredient1 = models.CharField(max_length=255, default='')
  ingredient2 = models.CharField(max_length=255, blank=True, null=True)
  ingredient3 = models.CharField(max_length=255, blank=True, null=True)
  ingredient4 = models.CharField(max_length=255, blank=True, null=True)
  ingredient5 = models.CharField(max_length=255, blank=True, null=True)
  ingredient6 = models.CharField(max_length=255, blank=True, null=True)
  ingredient7 = models.CharField(max_length=255, blank=True, null=True)
  ingredient8 = models.CharField(max_length=255, blank=True, null=True)
  ingredient1_embedding = models.JSONField(default=list, blank=True, null=True)
  ingredients = models.JSONField(default=list, blank=True, null=True)

  instructions = models.TextField()

  def save(self, *args, **kwargs):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    if self.ingredient1:
      self.ingredient1 = self.ingredient1.lower()
      self.ingredient1_embedding = model.encode(self.ingredient1).tolist()
    if self.ingredient2:
      self.ingredient2 = self.ingredient2.lower()
    if self.ingredient3:
      self.ingredient3 = self.ingredient3.lower()
    if self.ingredient4:
      self.ingredient4 = self.ingredient4.lower()
    if self.ingredient5:
      self.ingredient5 = self.ingredient5.lower()
    if self.ingredient6:
      self.ingredient6 = self.ingredient6.lower()
    if self.ingredient7:
      self.ingredient7 = self.ingredient7.lower()
    if self.ingredient8:
      self.ingredient8 = self.ingredient8.lower()
    super(Recipe, self).save(*args, **kwargs)