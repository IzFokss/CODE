// Programme de calculatrice
const affichage = document.getElementById("affichage");

// Ajoute le caractère choisi à la fin de ce qui est déjà affiché.
function ajouteraffichage(caractere) {
  affichage.value += caractere;
}

// Efface entièrement l'affichage de la calculatrice.
function effaceraffichage() {
  affichage.value = "";
}

// Calcule l'expression affichée et montre le résultat.
// Si l'expression n'est pas valide, affiche un message d'erreur.
function calculer() {
  try {
    affichage.value = eval(affichage.value);
  } catch (erreur) {
    affichage.value = "Erreur";
  }
}

// Programme de conversion d'unités

const champdistance = document.getElementById("champ-distance");
const versmetres = document.getElementById("vers-metres");
const verskilometres = document.getElementById("vers-kilometres");
const resultat = document.getElementById("resultat");
let distanceconvertie;

// Convertit la valeur saisie selon l'unité sélectionnée.
function convertir() {
  if (versmetres.checked) {
    distanceconvertie = Number(champdistance.value);
    distanceconvertie = distanceconvertie * 1000;
    resultat.textContent = distanceconvertie + "m";
  } else if (verskilometres.checked) {
    distanceconvertie = Number(champdistance.value);
    distanceconvertie = distanceconvertie / 1000;
    resultat.textContent = distanceconvertie + "km";
  } else {
    resultat.textContent = "Choisissez une unité";
  }
}

// Programme de calcul de budget

const champrevenus = document.getElementById("revenus");
const champdepenses = document.getElementById("depenses");
const affichagebudgetrestant = document.getElementById("budget-restant");

// Calcule les revenus moins les dépenses, puis affiche deux décimales.
function mettreajourbudget() {
  const montantrevenus = parseFloat(champrevenus.value) || 0;
  const montantdepenses = parseFloat(champdepenses.value) || 0;
  const budget = montantrevenus - montantdepenses;
  affichagebudgetrestant.textContent = budget.toFixed(2) + " €";
}

champrevenus.addEventListener("input", mettreajourbudget);
champdepenses.addEventListener("input", mettreajourbudget);

// Programme de gestion des tâches

const champnouvelletache = document.getElementById("champ-tache");
const conteneurliste = document.getElementById("liste-taches");

// Crée une tâche avec le texte saisi, puis enregistre la liste.
function ajoutertache() {
  if (champnouvelletache.value === "") {
    alert("Vous devez entrer du texte !");
  } else {
    let elementtache = document.createElement("li");
    elementtache.innerHTML = champnouvelletache.value;
    conteneurliste.appendChild(elementtache);
    let boutonsupprimer = document.createElement("span");
    boutonsupprimer.innerHTML = "\u00d7";
    elementtache.appendChild(boutonsupprimer);
  }
  champnouvelletache.value = "";
  sauvegarderdonnees();
}

// Réagit aux clics dans la liste : cliquer sur une tâche la coche,
// cliquer sur sa croix la supprime. La liste est ensuite enregistrée.
conteneurliste.addEventListener(
  "click",
  function (evenement) {
    if (evenement.target.tagName === "LI") {
      evenement.target.classList.toggle("coche");
      sauvegarderdonnees();
    } else if (evenement.target.tagName === "SPAN") {
      evenement.target.parentElement.remove();
      sauvegarderdonnees();
    }
  },
  false,
);

// Enregistre le contenu HTML de la liste dans le stockage du navigateur.
function sauvegarderdonnees() {
  localStorage.setItem("donnees", conteneurliste.innerHTML);
}

// Recharge la liste enregistrée pour la retrouver après un rechargement.
function actualiserdonnees() {
  conteneurliste.innerHTML = localStorage.getItem("donnees");
}

// Restaure les tâches dès le chargement de ce script.
actualiserdonnees();
