// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GestionnaireRisqueContrepartie {
    // Structure pour représenter une contrepartie
    struct Contrepartie {
        address portefeuille;
        uint256 scoreCredit;
        uint256 limiteExposition;
        uint256 expositionCourante;
        uint256 collateral;
        uint256 probabiliteDefaut; // Probabilité de défaut (PD) en pourcentage
        uint256 pertesEnCasDeDefaut; // Pertes en cas de défaut (LGD) en pourcentage
        bool estActif;
    }

    // Variables d'état
    mapping(address => Contrepartie) public contreparties;

    // Événements
    event ContrepartieAjoutee(address indexed contrepartie, uint256 limiteExposition);
    event ExpositionMiseAJour(address indexed contrepartie, uint256 nouvelleExposition);
    event LimiteDepassee(address indexed contrepartie, uint256 exposition);
    event ContrepartieFrozee(address indexed contrepartie);
    event AlerteRisque(address indexed contrepartie, string typeAlerte, uint256 valeur);

    // Ajouter une contrepartie
    function ajouterContrepartie(
        address _portefeuille,
        uint256 _scoreCredit,
        uint256 _limiteExposition,
        uint256 _probabiliteDefaut,
        uint256 _pertesEnCasDeDefaut
    ) public {
        require(
            contreparties[_portefeuille].portefeuille == address(0),
            "Contrepartie existe deja"
        );
        require(_scoreCredit > 0, "Score de credit doit etre positif");
        require(_limiteExposition > 0, "Limite d'exposition doit etre positive");

        contreparties[_portefeuille] = Contrepartie({
            portefeuille: _portefeuille,
            scoreCredit: _scoreCredit,
            limiteExposition: _limiteExposition,
            expositionCourante: 0,
            collateral: 0,
            probabiliteDefaut: _probabiliteDefaut,
            pertesEnCasDeDefaut: _pertesEnCasDeDefaut,
            estActif: true
        });

        emit ContrepartieAjoutee(_portefeuille, _limiteExposition);
    }

    // Mettre à jour l'exposition globale et vérifier les alertes/risques
    function mettreAJourExposition(address _portefeuille, uint256 _nouvelleExposition) public {
        Contrepartie storage c = contreparties[_portefeuille];
        require(c.portefeuille != address(0), "Contrepartie introuvable");
        require(c.estActif, "Contrepartie inactive");
        require(_nouvelleExposition >= 0, "L'exposition ne peut pas etre negative");

        c.expositionCourante = _nouvelleExposition;
        emit ExpositionMiseAJour(_portefeuille, _nouvelleExposition);

        // Vérifications des alertes et limites
        verifierAlertesEtLimites(_portefeuille);
    }

    // Calculer les pertes attendues
    function calculerPertesAttendues(address _portefeuille) public view returns (uint256) {
        Contrepartie memory c = contreparties[_portefeuille];
        require(c.portefeuille != address(0), "Contrepartie introuvable");
        require(c.expositionCourante > 0, "Exposition courante invalide");

        // Pertes Attendues = Exposition * Probabilité de Défaut (PD) * Pertes en Cas de Défaut (LGD)
        return (c.expositionCourante * c.probabiliteDefaut * c.pertesEnCasDeDefaut) / 10000;
    }

    // Calculer et vérifier les alertes et limites
    function verifierAlertesEtLimites(address _portefeuille) internal {
        Contrepartie storage c = contreparties[_portefeuille];
        uint256 ratioCouverture = (c.expositionCourante * 100) / c.limiteExposition;

        if (c.expositionCourante > c.limiteExposition) {
            c.estActif = false;
            emit LimiteDepassee(_portefeuille, c.expositionCourante);
            emit ContrepartieFrozee(_portefeuille);
        }

        if (ratioCouverture > 100) {
            emit AlerteRisque(_portefeuille, "Ratio de couverture eleve", ratioCouverture);
        }

        uint256 risque = calculerRisque(_portefeuille);
        if (risque > 100) {
            emit AlerteRisque(_portefeuille, "Score de risque eleve", risque);
        }
    }

    // Calculer le risque
    function calculerRisque(address _portefeuille) public view returns (uint256) {
        Contrepartie memory c = contreparties[_portefeuille];
        require(c.portefeuille != address(0), "Contrepartie introuvable");
        require(c.limiteExposition > 0, "Limite d'exposition invalide");

        return (c.expositionCourante * 10000) / (c.limiteExposition * c.scoreCredit);
    }

    // Mettre à jour le collatéral
    function mettreAJourCollateral(address _portefeuille, uint256 _nouveauCollateral) public {
        Contrepartie storage c = contreparties[_portefeuille];
        require(c.portefeuille != address(0), "Contrepartie introuvable");
        require(_nouveauCollateral >= 0, "n'accepte pas des valeur negative");

        c.collateral = _nouveauCollateral;
    }

    // Calculer le ratio de couverture
    function calculerRatioCouverture(address _portefeuille) public view returns (uint256) {
        Contrepartie memory c = contreparties[_portefeuille];
        require(c.portefeuille != address(0), "Contrepartie introuvable");
        require(c.expositionCourante > 0, "Exposition courante doit etre superieure a 0");

        return (c.collateral * 100) / c.expositionCourante;
    }
}