//programme calculatrice
const display = document.getElementById("display");

// Ajoute le caractère choisi à la fin de ce qui est déjà affiché.
function appendtodisplay(input) {
  display.value += input;
}

// Efface entièrement l'affichage de la calculatrice.
function cleardisplay() {
  display.value = "";
}

// Calcule l'expression affichée et montre le résultat.
// Si l'expression n'est pas valide, affiche un message d'erreur.
function calculate() {
  try {
    display.value = eval(display.value);
  } catch (error) {
    display.value = "Erreur";
  }
}

//programme de conversion d'unités

const textbox = document.getElementById("textbox");
const vers_mètres = document.getElementById("vers_mètres");
const vers_kilomètres = document.getElementById("vers_kilomètres");
const resultat = document.getElementById("resultat");
let distance;

// Convertit la valeur saisie selon l'unité sélectionnée.
function convertir() {
  if (vers_mètres.checked) {
    distance = Number(textbox.value);
    distance = distance * 1000;
    resultat.textContent = distance + "m";
  } else if (vers_kilomètres.checked) {
    distance = Number(textbox.value);
    distance = distance / 1000;
    resultat.textContent = distance + "km";
  } else {
    resultat.textContent = "Choissisez une unité";
  }
}

//programme de calculateur de budget

const revenueInput = document.getElementById("revenue");
const depensesInput = document.getElementById("depenses");
const budget_restant = document.getElementById("budget_restant");

// Calcule les revenus moins les dépenses, puis affiche deux décimales.
function updatebudget() {
  const montantRevenue = parseFloat(revenueInput.value) || 0;
  const montantDepenses = parseFloat(depensesInput.value) || 0;
  const budget = montantRevenue - montantDepenses;
  budget_restant.textContent = budget.toFixed(2) + " €";
}

revenueInput.addEventListener("input", updatebudget);
depensesInput.addEventListener("input", updatebudget);

//programme du gestionnaire de taches

const inputBox = document.getElementById("input-box");
const conteneurListe = document.getElementById("conteneur-liste");

// Crée une tâche avec le texte saisi, puis enregistre la liste.
function ajtTache() {
  if (inputBox.value === "") {
    alert("Vous devez entrer du texte !");
  } else {
    let li = document.createElement("li");
    li.innerHTML = inputBox.value;
    conteneurListe.appendChild(li);
    let span = document.createElement("span");
    span.innerHTML = "\u00d7";
    li.appendChild(span);
  }
  inputBox.value = "";
  sauvegarderDonnees();
}

// Réagit aux clics dans la liste : cliquer sur une tâche la coche,
// cliquer sur sa croix la supprime. La liste est ensuite enregistrée.
conteneurListe.addEventListener(
  "click",
  function (e) {
    if (e.target.tagName === "LI") {
      e.target.classList.toggle("coche");
      sauvegarderDonnees();
    } else if (e.target.tagName === "SPAN") {
      e.target.parentElement.remove();
      sauvegarderDonnees();
    }
  },
  false,
);

// Enregistre le contenu HTML de la liste dans le stockage du navigateur.
function sauvegarderDonnees() {
  localStorage.setItem("donnees", conteneurListe.innerHTML);
}

// Recharge la liste enregistrée pour la retrouver après un rechargement.
function ActualiserDonnees() {
  conteneurListe.innerHTML = localStorage.getItem("donnees");
}

// Restaure les tâches dès le chargement de ce script.
ActualiserDonnees();
