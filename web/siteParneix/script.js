// ========== GESTION DU FORMULAIRE ========== //
// Attachment d'un écouteur sur l'envoi du formulaire pour valider et personnaliser le titre

document.addEventListener('DOMContentLoaded', function() {
    // Écouteur sur la soumission du formulaire
    document.querySelector('form').addEventListener('submit', function(e) {
        e.preventDefault(); // Empêche le rechargement de la page
        
        // Récupération des valeurs du formulaire
        const prenom = document.getElementById('prenom').value.trim();
        const nom = document.getElementById('nom').value.trim();
        const sexe = document.querySelector('input[name="sexe"]:checked');
        
        // Validation des champs
        if (!prenom || !nom || !sexe) {
            alert("Veuillez remplir tous les champs.");
            return;
        }
        
        // Génération de la salutation personnalisée selon le sexe
        let salutation;
        if (sexe.value === 'Homme') {
            salutation = 'M. ' + prenom + ' ' + nom;
        } else {
            salutation = 'Mme. ' + prenom + ' ' + nom;
        }

        // Mise à jour du titre avec le nom de l'utilisateur
        document.querySelector('.titre').textContent = 'Bonjour, ' + salutation + ' !';
    });
});