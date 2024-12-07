import streamlit as st 
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
import os

# Page configuration
st.set_page_config(
    page_title="Gestion des Risques Contreparties",
    page_icon="🛡",
    layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
    }
    .stHeader {
        color: #4CAF50;
    }
    .stSuccess {
        color: #28a745;
    }
    .stError {
        color: #dc3545;
    }
    </style>
    """, unsafe_allow_html=True
)

# Load environment variables
load_dotenv()

# Connect to Infura
infura_url = f"https://polygon-amoy.infura.io/v3/{os.getenv('INFURA_PROJECT_ID')}"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Sidebar navigation
st.sidebar.title("📊 Navigation")
menu_option = st.sidebar.radio(
    "Choisissez une action:",
    ("Accueil", "Ajouter une Contrepartie", "Mettre à Jour", "Calcul des Risques", "Informations")
)

# Check connection
st.title("📋 Gestion des Risques Contreparties")
if web3.is_connected():
    st.success("✅ Connecté à Polygone-amoy via Infura")
else:
    st.error("❌ Échec de la connexion à Infura")
    st.stop()

# Load private key
private_key = os.getenv("PRIVATE_KEY")
if not private_key:
    st.error("🔒 Clé privée introuvable ! Veuillez l'ajouter au fichier .env.")
    st.stop()

# Wallet details
account = Account.from_key(private_key)
portefeuille = account.address
st.info(f"🔑 Adresse du portefeuille : {portefeuille}")

# Smart Contract details
contract_address = Web3.to_checksum_address("0xb010b596575ec0bb4ef47a5aee07f37c86a99411")
contract_abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "typeAlerte",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "valeur",
				"type": "uint256"
			}
		],
		"name": "AlerteRisque",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "limiteExposition",
				"type": "uint256"
			}
		],
		"name": "ContrepartieAjoutee",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "nouvelleExposition",
				"type": "uint256"
			}
		],
		"name": "ExpositionMiseAJour",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "exposition",
				"type": "uint256"
			}
		],
		"name": "LimiteDepassee",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_scoreCredit",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_limiteExposition",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_probabiliteDefaut",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_pertesEnCasDeDefaut",
				"type": "uint256"
			}
		],
		"name": "ajouterContrepartie",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			}
		],
		"name": "calculerPertesAttendues",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			}
		],
		"name": "calculerRatioCouverture",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			}
		],
		"name": "calculerRisque",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "contreparties",
		"outputs": [
			{
				"internalType": "address",
				"name": "portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "scoreCredit",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "limiteExposition",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "expositionCourante",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "collateral",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "probabiliteDefaut",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "pertesEnCasDeDefaut",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "estActif",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_nouveauCollateral",
				"type": "uint256"
			}
		],
		"name": "mettreAJourCollateral",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_nouvelleExposition",
				"type": "uint256"
			}
		],
		"name": "mettreAJourExposition",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Helper function to send transactions
def send_transaction(txn_function, *args, gas=300000):
    try:
        # Prepare the transaction
        nonce = web3.eth.get_transaction_count(portefeuille)
        txn = txn_function(*args).build_transaction({
            "from": portefeuille,
            "nonce": nonce,
            "gas": gas,
            "gasPrice": web3.to_wei("30", "gwei")
        })

        # Sign and send the transaction
        signed_txn = web3.eth.account.sign_transaction(txn, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Wait for the receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        # Check transaction status
        if receipt['status'] == 1:
            return {"success": True, "tx_hash": tx_hash.hex()}
        else:
            # If failed, try to decode the revert reason
            revert_reason = get_revert_reason(tx_hash)
            return {"success": False, "revert_reason": revert_reason}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_revert_reason(tx_hash):
    try:
        # Get the transaction details
        tx = web3.eth.get_transaction(tx_hash)
        # Simulate the transaction to fetch the revert reason
        revert_data = web3.eth.call({
            "to": tx["to"],
            "data": tx["input"],
            "from": tx["from"]
        }, tx["blockNumber"])
        return web3.to_text(revert_data)
    except Exception:
        return "Exposition depasse la limite autorisee."


# Main Menu Options
if menu_option == "Accueil":
    st.header("👋 Bienvenue dans l'App de Gestion des Risques")
    st.write("Utilisez le menu latéral pour naviguer.")

elif menu_option == "Ajouter une Contrepartie":
    st.markdown("<h2 style='color: #4CAF50;'>➕ Ajouter une Contrepartie</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        score_credit = st.number_input("Score de Crédit", min_value=1, value=100)
        limite_exposition = st.number_input("Limite d'Exposition", min_value=1, value=1000)

    with col2:
        probabilite_defaut = st.number_input("Probabilité de Défaut (%)", min_value=0, max_value=100, value=10)
        pertes_defaut = st.number_input("Pertes en Cas de Défaut (%)", min_value=0, max_value=100, value=50)

    if st.button("Ajouter Contrepartie"):
        tx_hash = send_transaction(
            contract.functions.ajouterContrepartie,
            portefeuille,
            int(score_credit),
            int(limite_exposition),
            int(probabilite_defaut),
            int(pertes_defaut)
        )
        if tx_hash:
            st.success(f"✅ Contrepartie ajoutée ! Hash: `{tx_hash}`")
        else:
            st.error("❌ Échec de la transaction.")

elif menu_option == "Mettre à Jour":
    st.markdown("<h2 style='color: #4CAF50;'>🔄 Mettre à Jour les Données</h2>", unsafe_allow_html=True)

    st.subheader("Mettre à Jour l'Exposition")
    nouvelle_exposition = st.number_input("Nouvelle Exposition", min_value=0, value=0)
    if st.button("Mettre à Jour Exposition"):
        response = send_transaction(
            contract.functions.mettreAJourExposition,
            portefeuille,
            int(nouvelle_exposition)
        )
        if response["success"]:
            st.success(f"✅ Exposition mise à jour ! Hash: `{response['tx_hash']}`")
        else:
            if "revert_reason" in response:
                st.error(f"❌ Transaction échouée : {response['revert_reason']}")
            elif "error" in response:
                st.error(f"❌ Erreur : {response['error']}")


    st.subheader("Mettre à Jour le Collateral")
    nouveau_collateral = st.number_input("Nouveau Collateral", min_value=0, value=0)
    if st.button("Mettre à Jour Collateral"):
        tx_hash = send_transaction(
            contract.functions.mettreAJourCollateral,
            portefeuille,
            int(nouveau_collateral)
        )
        if tx_hash:
            st.success(f"✅ Collateral mis à jour ! Hash: `{tx_hash}`")
        else:
            st.error("❌ Échec de la mise à jour.")

elif menu_option == "Calcul des Risques & Ratios":
    st.markdown("<h2 style='color: #4CAF50;'>📊 Calcul des Risques et Ratios</h2>", unsafe_allow_html=True)
    if st.button("Calculer"):
        try:
            risque = contract.functions.calculerRisque(portefeuille).call()
            ratio_couverture = contract.functions.calculerRatioCouverture(portefeuille).call()
            pertes_attendues = contract.functions.calculerPertesAttendues(portefeuille).call()

            st.metric(label="Score de Risque", value=f"{risque}")
            st.metric(label="Ratio de Couverture", value=f"{ratio_couverture}%")
            st.metric(label="Pertes Attendues", value=f"{pertes_attendues}")

        except Exception as e:
            st.error(f"Erreur lors du calcul des risques : {e}")

elif menu_option == "Informations":
    st.markdown("<h2 style='color: #4CAF50;'>📄 Informations sur la Contrepartie</h2>", unsafe_allow_html=True)
    if st.button("Afficher Informations"):
        try:
            contrepartie_info = contract.functions.contreparties(portefeuille).call()
            if contrepartie_info[0] != "0x0000000000000000000000000000000000000000":
                st.json({
                    "Portefeuille": contrepartie_info[0],
                    "Score de Crédit": contrepartie_info[1],
                    "Limite d'Exposition": contrepartie_info[2],
                    "Exposition Courante": contrepartie_info[3],
                    "Collateral": contrepartie_info[4],
                    "Probabilité de Défaut": contrepartie_info[5],
                    "Pertes en Cas de Défaut": contrepartie_info[6],
                    "Est Actif": contrepartie_info[7],
                })
            else:
                st.warning("Aucune contrepartie trouvée.")
        except Exception as e:
            st.error(f"Erreur : {e}")

# Footer
st.markdown("---")
st.info("💡 *Note : Utilisez toujours des réseaux de test pour vos expérimentations.*")
