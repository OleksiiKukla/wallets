# Generated by Django 4.0.5 on 2022-10-03 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_wallet_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transer_amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('commision', models.IntegerField()),
                ('status', models.CharField(max_length=6)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='transactions.wallet')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='transactions.wallet')),
            ],
        ),
    ]