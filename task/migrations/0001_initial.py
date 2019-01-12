# Generated by Django 2.1.5 on 2019-01-10 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deliveries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inning', models.IntegerField(default=0)),
                ('batting_team', models.CharField(max_length=100)),
                ('bowling_team', models.CharField(max_length=100)),
                ('over', models.IntegerField(default=0)),
                ('ball', models.IntegerField(default=0)),
                ('batsman', models.CharField(max_length=100)),
                ('non_striker', models.CharField(max_length=100)),
                ('bowler', models.CharField(max_length=100)),
                ('is_super_over', models.IntegerField(default=0)),
                ('wide_runs', models.IntegerField(default=0)),
                ('bye_runs', models.IntegerField(default=0)),
                ('legbye_runs', models.IntegerField(default=0)),
                ('noball_runs', models.IntegerField(default=0)),
                ('penalty_runs', models.IntegerField(default=0)),
                ('batsman_runs', models.IntegerField(default=0)),
                ('extra_runs', models.IntegerField(default=0)),
                ('total_runs', models.IntegerField(default=0)),
                ('player_dismissed', models.CharField(max_length=100)),
                ('dismissal_kind', models.CharField(max_length=100)),
                ('fielder', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.IntegerField(default=0)),
                ('city', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('team1', models.CharField(max_length=100)),
                ('team2', models.CharField(max_length=100)),
                ('toss_winner', models.CharField(max_length=100)),
                ('toss_decision', models.CharField(max_length=100)),
                ('result', models.CharField(max_length=100)),
                ('dl_applied', models.IntegerField(default=0)),
                ('winner', models.CharField(max_length=100)),
                ('win_by_runs', models.IntegerField(default=0)),
                ('win_by_wickets', models.IntegerField(default=0)),
                ('player_of_match', models.CharField(max_length=100)),
                ('venue', models.CharField(max_length=100)),
                ('umpire1', models.CharField(max_length=100)),
                ('umpire2', models.CharField(max_length=100)),
                ('umpire3', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='deliveries',
            name='match_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Matches'),
        ),
    ]
