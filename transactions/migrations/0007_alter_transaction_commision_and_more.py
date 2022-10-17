# Generated by Django 4.0.5 on 2022-10-05 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0006_alter_wallet_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="commision",
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="receiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="receiver",
                to="transactions.wallet",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="sender",
                to="transactions.wallet",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(max_length=100),
        ),
    ]
