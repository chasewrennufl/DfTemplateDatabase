# Generated by Django 4.0.4 on 2022-07-22 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import survey.models.survey
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, verbose_name='Name')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Display order')),
                ('description', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='IntentList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='intent list', max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Update date')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('is_published', models.BooleanField(default=True, verbose_name='Users can see it and answer it')),
                ('need_logged_user', models.BooleanField(verbose_name='Only authenticated users can see it and answer it')),
                ('editable_answers', models.BooleanField(default=True, verbose_name='Users can edit their answers afterwards')),
                ('display_method', models.SmallIntegerField(choices=[(1, 'By question'), (2, 'By category'), (0, 'All in one page')], default=0, verbose_name='Display method')),
                ('template', models.CharField(blank=True, max_length=255, null=True, verbose_name='Template')),
                ('publish_date', models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Publication date')),
                ('expire_date', models.DateField(blank=True, default=survey.models.survey.in_duration_day, verbose_name='Expiration date')),
                ('redirect_url', models.URLField(blank=True, verbose_name='Redirect URL')),
            ],
            options={
                'verbose_name': 'survey',
                'verbose_name_plural': 'surveys',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('interview_uuid', models.CharField(max_length=36, verbose_name='Interview unique identifier')),
                ('project_id', models.CharField(max_length=30)),
                ('auth', models.FileField(upload_to='')),
                ('intent_List', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='survey.intentlist', verbose_name='Intent List')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='survey.survey', verbose_name='Survey')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Set of answers to surveys',
                'verbose_name_plural': 'Sets of answers to surveys',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('order', models.IntegerField(verbose_name='Order')),
                ('required', models.BooleanField(verbose_name='Required')),
                ('type', models.CharField(choices=[('text', 'text (multiple line)'), ('short-text', 'short text (one line)'), ('radio', 'radio'), ('select', 'select'), ('select-multiple', 'Select Multiple'), ('select_image', 'Select Image'), ('integer', 'integer'), ('float', 'float'), ('date', 'date')], default='text', max_length=200, verbose_name='Type')),
                ('choices', models.TextField(blank=True, help_text="The choices field is only used if the question type\nif the question type is 'radio', 'select', or\n'select multiple' provide a comma-separated list of\noptions for this question .", null=True, verbose_name='Choices')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='survey.category', verbose_name='Category')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='survey.survey', verbose_name='Survey')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
                'ordering': ('survey', 'order'),
            },
        ),
        migrations.AddField(
            model_name='intentlist',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intent_list', to='survey.survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='intentlist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='Intent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='intent', max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('trainingPhrase', models.TextField()),
                ('message', models.TextField()),
                ('intentList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intents', to='survey.intentlist', verbose_name='Intent List')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intents', to='survey.question', verbose_name='Question')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='survey.survey', verbose_name='Survey'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Content')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='survey.question', verbose_name='Question')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='survey.response', verbose_name='Response')),
            ],
        ),
    ]
