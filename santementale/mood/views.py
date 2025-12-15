
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from .models import Tracking


from .models import Utilisateur, Mood, Tracking, Resolution



def save_tracking(request):
    if request.method == "POST":
        # Récupérer les valeurs telles qu'elles arrivent du formulaire
        water = request.POST.get("water")
        sleep = request.POST.get("sleep")
        sport = request.POST.get("sport")
        mood = request.POST.get("mood") or "neutral"

        # Si toutes les valeurs sont "0" et humeur neutre → ne rien faire
        if water == "0" and sleep == "0" and sport == "0" and mood == "neutral":
            messages.info(request, "Aucune donnée enregistrée car toutes les valeurs sont nulles.")
            return redirect("tracking")

        user_id = request.session.get("user_id")
        try:
            user = Utilisateur.objects.get(id_utilisateur=user_id)
            today = timezone.now().date()

            # Vérifier si une ligne existe déjà pour cet utilisateur et ce jour
            tracking_entry = Tracking.objects.filter(
                utilisateur=user,
                date_mood=today
            ).first()

            if tracking_entry:
                # Mise à jour
                tracking_entry.hydratation = water
                tracking_entry.sommeil = sleep
                tracking_entry.activite = sport
                tracking_entry.humeur = mood
                tracking_entry.save()
                messages.success(request, "Votre tracking du jour a été mis à jour")
            else:
                # Création
                Tracking.objects.create(
                    date_mood=today,
                    hydratation=water,
                    sommeil=sleep,
                    activite=sport,
                    humeur=mood,
                    utilisateur=user
                )
                messages.success(request, "Votre tracking du jour a été sauvegardé")

        except Utilisateur.DoesNotExist:
            messages.error(request, "Utilisateur introuvable")
        except Exception as e:
            messages.error(request, f"Erreur lors de la sauvegarde : {e}")

        return redirect("tracking")
 
def tracking(request):
    # Vérifier que l'utilisateur est connecté
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("connexion")

    # Récupérer les 30 derniers jours de tracking
    today = timezone.now().date()
    start_date = today - timedelta(days=30)

    trackings = Tracking.objects.filter(
        utilisateur_id=user_id,
        date_mood__gte=start_date
    ).order_by("-date_mood")

    # Calculer les moyennes
    summary = trackings.aggregate(
        avg_water=Avg("hydratation"),
        avg_sleep=Avg("sommeil"),
        avg_sport=Avg("activite")
    )

    # Trouver l’humeur dominante
    dominant_mood = trackings.values("humeur").annotate(
        count=Count("humeur")
    ).order_by("-count").first()

    return render(request, "tracking.html", {
        "trackings": trackings,
        "summary": summary,
        "dominant_mood": dominant_mood["humeur"] if dominant_mood else None
    })



def mood_list(request):
    moods = Mood.objects.all()
    return render(request, "index.html", {"moods": moods})


# enregistrer des résolutions

def save_resolution(request):
    if request.method == 'POST':
        text_resolution = request.POST.get("resolutionInput")
        date_resolution = request.POST.get("resolutionDate")
        user_id = request.session.get("user_id")

        if not date_resolution:
            date_resolution = timezone.now().date()
    try:
        user = Utilisateur.objects.get(id_utilisateur=user_id)
        Resolution.objects.create(
            intitule=text_resolution,
            checked=False,
            date_fixee=date_resolution,
            id_utilisateur=user   # <-- ici on passe l'objet
        )
        messages.success(request, "La résolution a bien été enregistrée")
    except Utilisateur.DoesNotExist:
        messages.error(request, "Utilisateur introuvable")


        messages.success(request,"La résolution a bien été enregistrée")
    
    return redirect("resolutions")





def connexion(request):
    if request.method == "POST":
        mail = request.POST.get("mail")
        mdp = request.POST.get("mdp")

        try:
            user = Utilisateur.objects.get(adresse_mail=mail)

            # Vérification du mot de passe haché
            if check_password(mdp, user.mdp):
                request.session["user_id"] = user.id_utilisateur
                request.session["user_nom"] = user.nom
                request.session["user_prenom"] = user.prenom
                request.session["user_mail"] = user.adresse_mail
                return redirect("home")
            else:
                messages.error(request, "Mail ou mot de passe incorrect")

        except Utilisateur.DoesNotExist:
            messages.error(request, "Mail ou mot de passe incorrect")

    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        mdp = request.POST.get("mdp")
        confirm = request.POST.get("confirm")

        # Vérification des champs obligatoires
        if not nom or not prenom or not email or not mdp or not confirm:
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, "register.html")

        # Vérification des mots de passe
        if mdp != confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "register.html")

        # Vérification si l'email existe déjà
        if Utilisateur.objects.filter(adresse_mail=email).exists():
            messages.error(request, "L'adresse mail est déjà utilisée.")
            return render(request, "register.html")

        # Hachage du mot de passe avant stockage
        hashed_password = make_password(mdp)

        Utilisateur.objects.create(
            nom=nom,
            prenom=prenom,
            adresse_mail=email,
            mdp=hashed_password
        )

        messages.success(request, "Inscription réussie ! Vous pouvez vous connecter.")
        return redirect("connexion")

    return render(request, "register.html")

def change_infos(request):
    if request.method == 'POST':
        new_nom = request.POST.get("nom")
        new_prenom = request.POST.get("prenom")

        # Si vide, reprendre les valeurs actuelles
        if not new_nom:
            new_nom = request.session.get("user_nom")
        if not new_prenom:
            new_prenom = request.session.get("user_prenom")

        try:
            user = Utilisateur.objects.get(id_utilisateur=request.session["user_id"])
            user.nom = new_nom
            user.prenom = new_prenom
            user.save()

            # Mettre à jour la session
            request.session["user_nom"] = user.nom
            request.session["user_prenom"] = user.prenom
            request.session["user_mail"] = user.adresse_mail

            messages.success(request, "Les informations ont été enregistrées.")
            return render(request, "profile.html", {
                "user_prenom": request.session.get("user_prenom"),
                "user_nom": request.session.get("user_nom"),
                "user_mail": request.session.get("user_mail")
            })

        except Utilisateur.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")
            return render(request, "profile.html", {
                "user_prenom": request.session.get("user_prenom"),
                "user_nom": request.session.get("user_nom"),
                "user_mail": request.session.get("user_mail")
            })


def change_mdp(request):
    if request.method == 'POST':
        current_pwd = request.POST.get("currentPwd")
        new_pwd = request.POST.get("newPwd")
        conf_pwd = request.POST.get("confirmPwd")

        if new_pwd != conf_pwd:
            messages.error(request, "Les mots de passe ne concordent pas.")
            return render(request, "profile.html", {
                "user_prenom": request.session.get("user_prenom"),
                "user_nom": request.session.get("user_nom"),
                "user_mail": request.session.get("user_mail")
            })

        try:
            user = Utilisateur.objects.get(id_utilisateur=request.session["user_id"])

            # Vérifier l'ancien mot de passe
            if not check_password(current_pwd, user.mdp):
                messages.error(request, "Mot de passe actuel incorrect.")
                return render(request, "profile.html", {
                    "user_prenom": request.session.get("user_prenom"),
                    "user_nom": request.session.get("user_nom"),
                    "user_mail": request.session.get("user_mail")
                })

            # Mettre à jour le mot de passe
            user.mdp = make_password(new_pwd)
            user.save()

            messages.success(request, "Mot de passe modifié avec succès.")
        except Utilisateur.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")

    return render(request, "profile.html", {
        "user_prenom": request.session.get("user_prenom"),
        "user_nom": request.session.get("user_nom"),
        "user_mail": request.session.get("user_mail")
    })



def home(request):
    user_nom = request.session.get("user_nom")
    user_prenom = request.session.get("user_prenom")
    return render(request, "home.html", {"user_nom": user_nom, "user_prenom": user_prenom})


def articles(request):
    return render(request, "articles.html")


def exercices(request):
    return render(request, "exercices.html")


def numeros(request):
    return render(request, "numeros.html")


def profile(request):
    user_prenom = request.session.get("user_prenom")
    user_nom = request.session.get("user_nom")
    user_mail = request.session.get("user_mail")
    return render(request, "profile.html", {
        "user_prenom": user_prenom,
        "user_nom": user_nom,
        "user_mail": user_mail
    })


def resolutions(request):
    user_id = request.session.get("user_id")

    try:
        user = Utilisateur.objects.get(id_utilisateur=user_id)
        user_resolutions = Resolution.objects.filter(id_utilisateur=user).order_by("-date_fixee")
    except Utilisateur.DoesNotExist:
        user_resolutions = []

    return render(request, "resolutions.html", {"resolutions": user_resolutions})


def toggle_resolution(request, id):
    if request.method == "POST":
        try:
            r = Resolution.objects.get(id=id, id_utilisateur=request.session.get("user_id"))
            r.checked = not r.checked
            r.save()
        except Resolution.DoesNotExist:
            pass
    return redirect("resolutions")


def delete_resolution(request, id):
    if request.method == "POST":
        Resolution.objects.filter(id=id, id_utilisateur=request.session.get("user_id")).delete()
    return redirect("resolutions")


def logout(request):
    request.session.flush()
    messages.success(request, "Vous avez été déconnecté.")
    return redirect("connexion")


