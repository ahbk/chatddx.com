from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class OpenAIMessageRole(models.Model):
    class Meta:
        verbose_name_plural = "OpenAI Message Roles"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class OpenAIModel(models.Model):
    class Meta:
        verbose_name_plural = "OpenAI Models"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class OpenAILogitBias(models.Model):
    class Meta:
        verbose_name_plural = "OpenAI Logit Biases"

    token = models.CharField(max_length=255)
    bias = models.IntegerField(
            validators=[
                MaxValueValidator(100),
                MinValueValidator(-100),
                ])

    def __str__(self):
        return f"{self.token} ({self.bias})"

    def serialize(self):
        return {
                "token": self.token,
                "bias": self.bias,
                }

class OpenAIMessage(models.Model):
    class Meta:
        verbose_name_plural = "OpenAI Messages"

    description = models.CharField(
            default="",
            max_length=255,
            )
    content = models.TextField()
    role = models.ForeignKey(OpenAIMessageRole, on_delete=models.PROTECT)
    name = models.CharField(
            max_length=255,
            default=None,
            null=True,
            blank=True,
            )

    def __str__(self):
        return self.description

    def serialize(self):
        m_dict = {
                "role": self.role.name,
                "content": self.content,
                }
        if not self.name is None:
            m_dict['name'] = self.name

        return m_dict
        


class OpenAIChat(models.Model):
    class Meta:
        verbose_name_plural = "OpenAI Chat Configuration"

    def __str__(self):
        return self.identifier

    identifier = models.CharField(
            max_length=255,
            unique=True,
            )
    active = models.BooleanField(default=True)
    endpoint = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    messages = models.ManyToManyField(OpenAIMessage)
    model = models.ForeignKey(OpenAIModel, on_delete=models.PROTECT)

    frequency_penalty = models.FloatField(
            default=None,
            null=True,
            blank=True,
            validators=[
                MinValueValidator(-2),
                MaxValueValidator(2),
                ])

    logit_bias = models.ManyToManyField(
            OpenAILogitBias,
            blank=True,
            )

    max_tokens = models.IntegerField(
            default=None,
            null=True,
            blank=True,
            validators=[
                MinValueValidator(1),
                MaxValueValidator(2000),
                ])

    presence_penalty = models.FloatField(
            default=None,
            null=True,
            blank=True,
            validators=[
                MinValueValidator(-2),
                MaxValueValidator(2),
                ])

    temperature = models.FloatField(
            default=None,
            null=True,
            blank=True,
            validators=[
                MinValueValidator(0),
                MaxValueValidator(2),
                ]
            )

    top_p = models.FloatField(
            default=None,
            null=True,
            blank=True,
            validators=[
                MinValueValidator(0),
                MaxValueValidator(1),
                ]
            )

    user = models.CharField(
            max_length=255,
            default=None,
            blank=True,
            null=True,
            )

    def serialize(self):
        payload = {
                "messages": [m.serialize() for m in self.messages.all()],
                "model": self.model.name
                }

        logit_bias = self.logit_bias.all()
        if logit_bias:
            payload['logit_bias'] = [lb.serialize() for lb in logit_bias]

        for attr in [
                'frequency_penalty',
                'max_tokens',
                'presence_penalty',
                'temperature',
                'top_p',
                'user',
                ]:
            val = getattr(self, attr)
            if not val is None:
                payload[attr] = val

        return {
                "identifier": self.identifier,
                "endpoint": self.endpoint,
                "api_key": self.api_key,
                "payload": payload,
                }
