# Go (2024)
**Secteur d’activité** : Mobilité et Transport.

## Concept
**GO** est une plateforme web de location de voitures entre particuliers. Les utilisateurs peuvent mettre leur voiture en location lorsqu'ils ne l'utilisent pas, et ceux qui en ont besoin peuvent la louer pour une durée déterminée. C'est une solution pratique et économique pour ceux qui ont besoin d'un véhicule temporairement.

## Fonctionnalités clés

### 1. Inscription et vérification des utilisateurs
- Les propriétaires et les locataires doivent créer un compte et fournir des documents tels que la pièce d'identité, le permis de conduire, et les informations sur leur véhicule.
- **Pour plus de sécurité** :
  - Les utilisateurs peuvent être vérifiés à travers des plateformes locales ou des services de vérification d'identité via une API.
  - Option de vérification manuelle en complément.

### 2. Mise en location d'un véhicule
- Les propriétaires de voitures peuvent lister leur véhicule sur la plateforme avec :
  - Photos, description, prix par jour ou par heure.
  - Conditions de location (ex. nombre de kilomètres autorisés).
- **Options supplémentaires** :
  - Ajouter des informations spécifiques comme la consommation de carburant, la disponibilité, et les restrictions géographiques.

### 3. Recherche et réservation
- Les locataires peuvent rechercher des véhicules disponibles en fonction de l'emplacement, du type de véhicule, et du prix.
- Réservation simple et flexible pour des périodes spécifiques (heure, jour, semaine).

### 4. Paiement sécurisé en ligne
- Paiements sécurisés via la plateforme par :
  - **Cartes locales** : CIP & EDAHABIA
  - **Cartes internationales** : VISA
- **Option de prélèvement ou de caution** pour garantir le véhicule.

### 5. Assurance intégrée
- Assurance de base incluse pour chaque location.
- Possibilité de souscrire à une assurance complémentaire pour une meilleure protection.

### 6. Système de notation et de feedback
- Les deux parties peuvent se noter après chaque transaction, instaurant la confiance et favorisant une communauté sûre.

### 7. Support client
- Service client dédié pour gérer :
  - Conflits, problèmes de réservation, ou urgences.

### 8. Gestion des pénalités
- Système pour gérer les pénalités en cas de :
  - Dépassement de kilométrage
  - Retard dans la restitution du véhicule
  - Dommages au véhicule

## Modèle économique

1. **Commissions** : La plateforme prélève une commission sur chaque location, typiquement un pourcentage (ex. 10-20%) du montant de la location.
2. **Assurance optionnelle** : Frais supplémentaires pour l'assurance complémentaire, générant un revenu pour la plateforme.
3. **Frais de services premium** : Offrir des services comme la livraison de la voiture au locataire.

## Technologie nécessaire

- **Frontend** : Utilisation de technologies comme **React.js** pour l'interface utilisateur.
- **Backend** : Un framework comme **Django (Python)** pour gérer la logique métier et les API.
- **Paiements** : Intégration d'une solution de paiement locale pour sécuriser les transactions (ex. CIB, carte EDAHABIA).

## Explications des dossiers principaux
- apps :
        - **users** : Gère les utilisateurs (inscription, connexion, profil).
        - **listings** : Gère les annonces de voitures (création d'annonce, visualisation).
        - **reservations** : Gère les réservations effectuées sur les voitures.
        - **payments** : Gère les paiements pour les locations.
