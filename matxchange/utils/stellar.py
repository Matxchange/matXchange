import frappe
import json
import hashlib


def get_stellar_credentials():
    return {
        "secret_key": frappe.conf.get("stellar_secret_key", ""),
        "network": frappe.conf.get("stellar_network", "testnet")
    }


def write_transaction(data):
    try:
        from stellar_sdk import Server, Keypair, TransactionBuilder, Network, ManageData

        creds = get_stellar_credentials()
        if not creds["secret_key"]:
            frappe.log_error("Stellar secret key not configured", "Stellar Error")
            return None

        if creds["network"] == "testnet":
            server = Server("https://horizon-testnet.stellar.org")
            network = Network.TESTNET_NETWORK_PASSPHRASE
        else:
            server = Server("https://horizon.stellar.org")
            network = Network.PUBLIC_NETWORK_PASSPHRASE

        keypair = Keypair.from_secret(creds["secret_key"])
        account = server.load_account(keypair.public_key)

        data_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()[:28]

        tx = (
            TransactionBuilder(
                source_account=account,
                network_passphrase=network,
                base_fee=100
            )
            .append_manage_data_op(
                data_name="matxchange",
                data_value=data_hash.encode()
            )
            .add_text_memo(data_hash)
            .set_timeout(30)
            .build()
        )
        tx.sign(keypair)
        response = server.submit_transaction(tx)
        return response.get("hash")

    except ImportError:
        frappe.log_error("stellar-sdk not installed", "Stellar Import Error")
        return None
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Stellar Write Error")
        return None
