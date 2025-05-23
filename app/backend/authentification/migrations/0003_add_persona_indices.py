from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('authentification', '0002_authuser_remove_doctor_user_remove_pacient_user_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='persona',
            index=models.Index(fields=['tipo_usuario'], name='auth_tipo_usuario_idx'),
        ),
        migrations.AddIndex(
            model_name='persona',
            index=models.Index(fields=['nombre'], name='auth_nombre_idx'),
        ),
        migrations.AddIndex(
            model_name='persona',
            index=models.Index(fields=['apellido'], name='auth_apellido_idx'),
        ),
        # Índice compuesto para búsquedas por nombre y apellido juntos
        migrations.AddIndex(
            model_name='persona',
            index=models.Index(fields=['nombre', 'apellido'], name='auth_nombre_apellido_idx'),
        ),
    ]
