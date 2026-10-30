//programme calculatrice
const display = document.getElementById("display");
function appendtodisplay(input) {
  display.value += input;
}

function cleardisplay() {
  display.value = "";
}
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
function sauvegarderDonnees() {
  localStorage.setItem("donnees", conteneurListe.innerHTML);
}
function ActualiserDonnees() {
  conteneurListe.innerHTML = localStorage.getItem("donnees");
}
ActualiserDonnees();
