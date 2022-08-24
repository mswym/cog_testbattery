from django.db import models

# Create your models here.

# Create your models here.
class SampleAppModel(models.Model):
    itemname = models.CharField(max_length=100)
    itemvalue = models.IntegerField()


class CognitiveTask(models.Model):
    name = models.TextField(blank=True)
    view_name = models.TextField(blank=True)
    instructions_prompt_label = models.TextField(blank=True)
    template_instruction_path = models.TextField(blank=True)
    template_tutorials_path = models.TextField(blank=True)


class CognitiveResult(models.Model):
    participant = models.ForeignKey(ParticipantProfile, on_delete=models.CASCADE)
    cognitive_task = models.ForeignKey(CognitiveTask, on_delete=models.CASCADE)
    idx = models.IntegerField()
    results = jsonfield.JSONField(blank=True)
    status = models.TextField(blank=True, default="pre_test")