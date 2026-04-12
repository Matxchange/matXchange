import frappe
import json
import hashlib


def get_stellar_credentials():
    return {
        "secret_key": frappe.conf.get("stellar_secret_key", ""),
        "network":    frappe.conf.get("stellar_network", "testnet"),
    }


def _get_server_and_network(creds):
    from stellar_sdk import Server, Network
    if creds["network"] == "testnet":
        return (
            Server("https://horizon-testnet.stellar.org"),
            Network.TESTNET_NETWORK_PASSPHRASE,
        )
    return (
        Server("https://horizon.stellar.org"),
        Network.PUBLIC_NETWORK_PASSPHRASE,
    )


def mint_reco_token(collector_id, weight_kg, transaction_id):
    try:
        from stellar_sdk import Keypair, TransactionBuilder, Asset

        creds = get_stellar_credentials()
        if not creds["secret_key"]:
            frappe.log_error("Stellar secret key not configured", "Stellar RECO Mint")
            return None

        server, network = _get_server_and_network(creds)
        keypair  = Keypair.from_secret(creds["secret_key"])
        pub      = keypair.public_key

        reco_asset  = Asset("RECO", pub)
        reco_amount = str(round(float(weight_kg), 7))
        memo_text   = str(transaction_id)[:28]

        account = server.load_account(pub)

        builder = TransactionBuilder(
            source_account=account,
            network_passphrase=network,
            base_fee=100,
        )

        # No change_trust — this account IS the issuer of RECO
        builder.append_payment_op(
            destination=pub,
            asset=reco_asset,
            amount=reco_amount,
        )
        builder.add_text_memo(memo_text)
        builder.set_timeout(30)

        tx = builder.build()
        tx.sign(keypair)
        response = server.submit_transaction(tx)

        stellar_hash = response.get("hash")

        frappe.logger().info(
            f"[MatXchange] RECO minted | amount={reco_amount} | "
            f"collector={collector_id} | erp_tx={transaction_id} | hash={stellar_hash}"
        )

        return {
            "stellar_hash":   stellar_hash,
            "stellar_ledger": response.get("ledger"),
            "reco_amount":    float(weight_kg),
        }

    except ImportError:
        frappe.log_error("stellar-sdk not installed", "Stellar Import Error")
        return None
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Stellar RECO Mint Error")
        return None


def write_transaction(data):
    try:
        from stellar_sdk import Keypair, TransactionBuilder

        creds = get_stellar_credentials()
        if not creds["secret_key"]:
            frappe.log_error("Stellar secret key not configured", "Stellar Error")
            return None

        server, network = _get_server_and_network(creds)
        keypair = Keypair.from_secret(creds["secret_key"])
        account = server.load_account(keypair.public_key)

        data_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()[:28]

        tx = (
            TransactionBuilder(
                source_account=account,
                network_passphrase=network,
                base_fee=100,
            )
            .append_manage_data_op(
                data_name="matxchange",
                data_value=data_hash.encode(),
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
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Stellar Write Error")
        return None


def test_reco_mint():
    result = mint_reco_token(
        collector_id="TEST-COLLECTOR",
        weight_kg=10.0,
        transaction_id="TEST-MATX-2026-00001",
    )
    if result:
        frappe.errprint(f"RECO mint OK - hash: {result['stellar_hash']}")
        frappe.errprint(f"Check: https://stellar.expert/explorer/testnet/tx/{result['stellar_hash']}")
    else:
        frappe.errprint("RECO mint FAILED - check Error Log in Frappe desk")