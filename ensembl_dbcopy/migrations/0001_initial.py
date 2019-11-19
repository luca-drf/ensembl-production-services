# Generated by Django 2.1.7 on 2019-11-18 15:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dbs2Exclude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_schema', models.CharField(db_column='TABLE_SCHEMA', max_length=64)),
            ],
            options={
                'db_table': 'dbs_2_exclude',
            },
        ),
        migrations.CreateModel(
            name='DebugLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(blank=True, max_length=128, null=True)),
                ('sequence', models.IntegerField(blank=True, null=True)),
                ('function', models.CharField(blank=True, max_length=128, null=True)),
                ('value', models.TextField(blank=True, max_length=8192, null=True)),
            ],
            options={
                'db_table': 'debug_log',
            },
        ),
        migrations.CreateModel(
            name='RequestJob',
            fields=[
                ('job_id', models.CharField(default=uuid.uuid1, editable=False, max_length=128, primary_key=True, serialize=False)),
                ('src_host', models.TextField(max_length=2048)),
                ('src_incl_db', models.TextField(blank=True, max_length=2048, null=True)),
                ('src_skip_db', models.TextField(blank=True, max_length=2048, null=True)),
                ('src_incl_tables', models.TextField(blank=True, max_length=2048, null=True)),
                ('src_skip_tables', models.TextField(blank=True, max_length=2048, null=True)),
                ('tgt_host', models.TextField(max_length=2048)),
                ('tgt_db_name', models.TextField(blank=True, max_length=2048, null=True)),
                ('tgt_directory', models.TextField(blank=True, max_length=2048, null=True)),
                ('skip_optimize', models.BooleanField(default=False)),
                ('wipe_target', models.BooleanField(default=False)),
                ('convert_innodb', models.BooleanField(default=False)),
                ('email_list', models.TextField(blank=True, max_length=2048, null=True)),
                ('start_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('end_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('user', models.CharField(blank=True, max_length=64, null=True)),
                ('status', models.CharField(blank=True, editable=False, max_length=20, null=True)),
            ],
            options={
                'db_table': 'request_job',
            },
        ),
        migrations.CreateModel(
            name='TransferLog',
            fields=[
                ('auto_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tgt_host', models.CharField(editable=False, max_length=512)),
                ('table_schema', models.CharField(db_column='TABLE_SCHEMA', editable=False, max_length=64)),
                ('table_name', models.CharField(db_column='TABLE_NAME', editable=False, max_length=64)),
                ('renamed_table_schema', models.CharField(editable=False, max_length=64)),
                ('target_directory', models.TextField(blank=True, editable=False, max_length=2048, null=True)),
                ('start_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('end_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('size', models.BigIntegerField(blank=True, editable=False, null=True)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, related_name='transfer_logs', to='ensembl_dbcopy.RequestJob')),
            ],
            options={
                'verbose_name': 'TransferLog',
                'db_table': 'transfer_log',
            },
        ),
        migrations.AlterUniqueTogether(
            name='transferlog',
            unique_together={('job_id', 'tgt_host', 'table_schema', 'table_name')},
        ),
    ]
