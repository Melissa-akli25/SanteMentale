from django.db import models

class Mood(models.Model):
    emoji = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return f"{self.emoji} - {self.message[:20]}"

    class Meta:
        db_table = "mood"
        managed = False   # Django n'essaie pas de créer/modifier la table


class Utilisateur(models.Model):
    id_utilisateur = models.AutoField(primary_key=True)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    adresse_mail = models.CharField(max_length=100)
    mdp = models.TextField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        db_table = "utilisateur"
        managed = False


class Tracking(models.Model):
    id = models.AutoField(primary_key=True)
    date_mood = models.DateField()
    hydratation = models.IntegerField()
    activite = models.IntegerField()
    sommeil = models.IntegerField()
    humeur = models.CharField(max_length=20, null=True, blank=True)

    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        db_column="id_utilisateur"   # <-- correspond au vrai champ dans ta table
    )

    class Meta:
        db_table = "tracking"
        managed = False



class Resolution(models.Model):
    id = models.AutoField(primary_key=True)
    intitule = models.CharField(max_length=255)
    checked = models.BooleanField(null=True, default=None)
    date_fixee = models.DateField(null=True, blank=True)

    id_utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        db_column="id_utilisateur"
    )

    class Meta:
        db_table = "resolutions"
        managed = False
