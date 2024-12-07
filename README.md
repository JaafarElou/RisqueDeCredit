# Gestion des Risques de Contrepartie - Smart Contract

Ce projet implémente un **smart contract Ethereum** écrit en Solidity, conçu pour gérer les **risques de contrepartie** dans un contexte financier. Il permet d'automatiser et de sécuriser la gestion des expositions financières, tout en intégrant des mécanismes avancés pour évaluer et réduire les risques associés.

## **Objectifs du Projet**
1. Proposer une solution décentralisée pour la gestion des expositions financières.
2. Automatiser les calculs de risques pour une transparence accrue et une meilleure traçabilité.
3. Mettre en place des alertes et des contrôles proactifs pour prévenir les dépassements de limites.
4. Intégrer des fonctionnalités pour sécuriser les garanties (collatéraux) dans les transactions financières.

---

## **Fonctionnalités Principales**

### 1. Gestion des Contreparties
- Ajout de contreparties avec des paramètres financiers personnalisés (score de crédit, limite d'exposition, probabilité de défaut, etc.).
- Stockage sécurisé des données via un mapping Solidity.

### 2. Gestion des Expositions
- Mise à jour de l'exposition courante d'une contrepartie.
- Détection automatique des dépassements de limites avec gel des opérations si nécessaire.
- Calcul du ratio de couverture pour évaluer la sécurité des engagements financiers.

### 3. Calcul des Risques
- Évaluation des risques financiers basés sur l'exposition courante, les scores de crédit et les facteurs de probabilité de défaut.
- Calcul des pertes attendues en cas de défaut (Expected Loss).

### 4. Gestion des Collatéraux
- Mise à jour et suivi des garanties déposées par les contreparties.
- Intégration du ratio de couverture dans l'évaluation globale des risques.

### 5. Notifications et Alertes
- Emission d'événements Solidity pour notifier des actions critiques telles que :
  - Dépassement des limites d'exposition.
  - Alertes de risques élevés.
  - Mise à jour des données financières.

---

## **Structure du Contrat**

### Variables Principales
- **`Contrepartie`** : Structure contenant les informations financières (portefeuille, exposition, score de crédit, garanties, etc.).
- **`contreparties`** : Mapping associant chaque portefeuille Ethereum à une structure `Contrepartie`.

### Événements
- **`ContrepartieAjoutee`** : Déclenché lorsqu'une contrepartie est ajoutée.
- **`ExpositionMiseAJour`** : Déclenché lors de la mise à jour de l'exposition courante.
- **`LimiteDepassee`** : Déclenché en cas de dépassement de la limite d'exposition.
- **`AlerteRisque`** : Émis pour signaler un risque élevé ou une alerte critique.
- **`ContrepartieFrozee`** : Déclenché lorsque la contrepartie est gelée pour des raisons de risque.

### Fonctions Clés
1. **`ajouterContrepartie`** : Permet d'ajouter une nouvelle contrepartie avec des paramètres financiers prédéfinis.
2. **`mettreAJourExposition`** : Met à jour l'exposition courante et vérifie les dépassements de seuils.
3. **`calculerRisque`** : Évalue le risque basé sur l'exposition courante, les scores de crédit et les limites.
4. **`calculerPertesAttendues`** : Calcule les pertes potentielles en cas de défaut.
5. **`mettreAJourCollateral`** : Gère les mises à jour des garanties déposées par les contreparties.

---

## **Déploiement**

### Prérequis
- **Remix IDE** : Pour l'écriture, la compilation et le déploiement du contrat.
- **MetaMask** : Connecté au réseau Polygon Mumbai Testnet.
- **Solidity Compiler** : Version 0.8.0 ou ultérieure.

### Étapes de Déploiement
1. Ouvrir **Remix IDE** et créer un fichier nommé `RisqueDeContrepartie.sol`.
2. Copier et coller le code du contrat dans le fichier.
3. Sélectionner le compilateur Solidity version 0.8.0 ou supérieure.
4. Connecter **MetaMask** au réseau Polygon Mumbai Testnet.
5. Déployer le contrat en utilisant l'environnement `Injected Web3`.

---

## **Tests et Résultats**

### Scénarios Testés
1. **Ajout de Contreparties** : Vérification de l'ajout correct des contreparties avec des paramètres financiers personnalisés.
2. **Mise à Jour de l'Exposition** : Simulation de mises à jour valides et tests des alertes en cas de dépassement de limites.
3. **Calcul des Risques** : Validation des formules pour les pertes attendues et les risques globaux.
4. **Gestion des Collatéraux** : Mise à jour des garanties et impact sur le ratio de couverture.

### Résultats Observés
- Les événements ont été émis correctement pour chaque action (ajout, mise à jour, alerte).
- Les dépassements de limites ont déclenché des alertes et gelé les contreparties concernées.
- Les pertes attendues ont été calculées avec précision en fonction des données financières.

---

## **Cas Limites Gérés**

1. **Entrées Invalides** : Validation stricte des données entrantes (ex : les valeurs négatives sont interdites).
2. **Transactions Échouées** : Les transactions sont annulées si les conditions préalables ne sont pas respectées.
3. **Congestion du Réseau** : Les événements Solidity assurent une traçabilité même en cas de retard de transaction.

---

## **Applications Potentielles**

Ce contrat peut être utilisé dans plusieurs contextes financiers réels, notamment :
1. **Plateformes DeFi (Finance Décentralisée)** :
   - Gestion automatisée des risques de prêt.
   - Surveillance proactive des garanties et des limites d'exposition.
2. **Institutions Financières** :
   - Optimisation de la gestion des contreparties.
   - Réduction des risques associés aux défauts financiers.

### Modifications Nécessaires pour une Utilisation en Production
- **Audits de Sécurité** : Validation indépendante pour sécuriser le contrat contre les failles potentielles.
- **Optimisation des Coûts de Gas** : Réduction des frais pour rendre l'utilisation viable à grande échelle.
- **Interface Utilisateur** : Développement d'une interface conviviale pour interagir avec le contrat.

---

## **Réflexions sur le Développement**

### Défis Rencontrés
- Gestion de l'efficacité des coûts de gas lors des mises à jour fréquentes.
- Prise en compte des cas limites tels que les dépassements de seuils et les entrées invalides.

### Solutions Apportées
- Utilisation de `mappings` pour un accès rapide aux données.
- Validation stricte des entrées pour éviter les erreurs.

### Améliorations Futures
- Intégrer des **facteurs macroéconomiques** dans le calcul des risques.
- Développer une API ou une interface utilisateur pour simplifier les interactions avec le contrat.

---

## **Contributeur**
- **El Ouakhchachi Jaafar** - Développeur principal.

---

## **Licence**
Ce projet est sous licence MIT.

