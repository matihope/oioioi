# Generated by Django 3.2.16 on 2023-01-01 22:16

from django.db import migrations, models
import django.db.models.deletion
import oioioi.participants.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('participants', '0010_alter_termsacceptedphrase_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MPRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terms_accepted', models.BooleanField(default=False, verbose_name='terms accepted')),
                ('participant', oioioi.participants.fields.OneToOneBothHandsCascadingParticipantField(on_delete=django.db.models.deletion.CASCADE, related_name='mp_mpregistration', to='participants.participant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
