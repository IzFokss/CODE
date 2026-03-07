document.addEventListener('DOMContentLoaded', function() {
    

    document.querySelector('form').addEventListener('submit', function(e) {
        e.preventDefault();
        const prenom = document.getElementById('prenom').value.trim();
        const nom = document.getElementById('nom').value.trim();
        const sexe = document.querySelector('input[name="sexe"]:checked');
        
        if (!prenom || !nom || !sexe) {
            alert("Veuillez remplir tous les champs."); //Permet d'afficher une alerte si les champs ne sont pas remplis
            return;
        }
        
        let salutation;

        if (sexe.value === 'Homme') {
            salutation = 'M. ' + prenom + ' ' + nom;
        } else {
            salutation = 'Mme. ' + prenom + ' ' + nom;
        }

        document.querySelector('.titre').textContent = 'Bonjour, ' + salutation + ' !';
    });
});