"""
# Complete Taproot Example: Key Path + Script Path
# This demonstrates the full flexibility of Taproot by:
# 1. Creating a Taproot address with both key path and script paths
# 2. Funding the Taproot address
# 3. Spending using key path (first transaction)
# 4. Spending using script path (second transaction)
"""
from bitcoinutils.setup import setup
from bitcoinutils.proxy import NodeProxy
from bitcoinutils.utils import to_satoshis, ControlBlock
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.keys import PrivateKey


"""
This one has bugs and is not working.
"""


def main():
    # Setup the Bitcoin node connection
    setup("regtest")
    proxy = NodeProxy("bitcoin", "localtest").get_proxy()

    try:
        proxy.loadwallet('mywallet')
        print('Loaded mywallet')
    except:
        try:
            print("Loading failed. Try creating wallet 'mywallet'.")
            proxy.createwallet('mywallet')
        except:
            print("Error creating wallet 'mywallet'. Maybe already loaded")

    # Generate some initial coins
    addr = proxy.getnewaddress("first_address", "bech32")
    proxy.generatetoaddress(101, addr)
    print(f'\nInitial Balance: {proxy.getbalance()} BTC')

    # ============================================================================
    # STEP 1: Create Taproot address with key path + script paths
    # ============================================================================
    print("\n" + "="*60)
    print("STEP 1: Creating Taproot address with key path + script paths")
    print("="*60)
    
    # Create the internal key (this will be tweaked for the Taproot address)
    internal_private_key = PrivateKey()
    internal_public_key = internal_private_key.get_public_key()
    
    print(f"Internal Private Key (WIF): {internal_private_key.to_wif()}")
    print(f"Internal Public Key: {internal_public_key.to_hex()}")
    print(f"Internal X-only Public Key: {internal_public_key.to_x_only_hex()}")
    
    # Create script keys for different spending conditions
    script_key_1 = PrivateKey()
    script_key_2 = PrivateKey()
    
    print(f"Script Key 1 (WIF): {script_key_1.to_wif()}")
    print(f"Script Key 2 (WIF): {script_key_2.to_wif()}")
    
    # Create different script types
    # Script 1: Simple P2PK
    script_1 = Script([script_key_1.get_public_key().to_x_only_hex(), "OP_CHECKSIG"])
    
    # Script 2: 2-of-2 multisig
    script_2 = Script([
        "OP_2",
        script_key_1.get_public_key().to_x_only_hex(),
        script_key_2.get_public_key().to_x_only_hex(),
        "OP_2",
        "OP_CHECKMULTISIG"
    ])
    
    print(f"Script 1 (P2PK): {script_1.to_hex()}")
    print(f"Script 2 (2-of-2 multisig): {script_2.to_hex()}")
    
    # Create Taproot address with scripts
    # This allows both key path and script path spending
    taproot_scripts = [script_1, script_2]
    taproot_address = internal_public_key.get_taproot_address(taproot_scripts)
    
    print(f"Taproot Address: {taproot_address.to_string()}")
    print(f"Witness Program: {taproot_address.to_witness_program()}")
    print(f"Address Type: {taproot_address.get_type()}")
    print(f"Is Odd: {taproot_address.is_odd()}")
    
    # ============================================================================
    # STEP 2: Fund the Taproot address
    # ============================================================================
    print("\n" + "="*60)
    print("STEP 2: Funding the Taproot address")
    print("="*60)
    
    # Send some BTC to the Taproot address
    funding_amount = 0.2
    tx_fund = proxy.sendtoaddress(taproot_address.to_string(), funding_amount)
    print(f"Funding transaction ID: {tx_fund}")
    
    # Generate a block to confirm the funding transaction
    proxy.generatetoaddress(1, addr)
    print(f"Balance after funding: {proxy.getbalance()} BTC")
    
    # Get transaction details to find the UTXO
    tx_details = proxy.gettransaction(tx_fund)
    print(f"Transaction details: {tx_details}")
    
    # Find the output that went to our Taproot address
    vout = None
    for detail in tx_details['details']:
        if detail['address'] == taproot_address.to_string():
            vout = detail['vout']
            break
    
    if vout is None:
        print("Error: Could not find the correct output")
        return
    
    print(f"Found UTXO at vout: {vout}")
    
    # ============================================================================
    # STEP 3: First spend - Key Path
    # ============================================================================
    print("\n" + "="*60)
    print("STEP 3: First spend - Key Path")
    print("="*60)
    
    # Create a destination address for the first spend
    dest_private_key_1 = PrivateKey()
    dest_address_1 = dest_private_key_1.get_public_key().get_address()
    print(f"Destination address 1: {dest_address_1.to_string()}")
    
    # Create transaction input from the Taproot UTXO
    txin_1 = TxInput(tx_fund, vout)
    
    # Create transaction output (send half the funds)
    spend_amount_1 = 0.09
    txout_1 = TxOutput(to_satoshis(spend_amount_1), dest_address_1.to_script_pub_key())
    
    # Create the transaction (must set has_segwit=True for Taproot)
    tx_1 = Transaction([txin_1], [txout_1], has_segwit=True)
    print(f"Raw unsigned transaction 1:\n{tx_1.serialize()}")
    
    # Sign using key path (internal key is automatically tweaked)
    amounts = [to_satoshis(funding_amount)]
    utxo_script_pubkeys = [taproot_address.to_script_pub_key()]
    
    sig_1 = internal_private_key.sign_taproot_input(
        tx_1,
        0,
        utxo_script_pubkeys,
        amounts,
        script_path=False,  # Key path spending
        tweak=True  # Tweak the key for Taproot
    )
    print(f"Key path signature: {sig_1}")
    
    # Add the witness (for key path, just the signature)
    tx_1.witnesses.append(TxWitnessInput([sig_1]))
    
    # Get the signed transaction
    signed_tx_1 = tx_1.serialize()
    print(f"Raw signed transaction 1:\n{signed_tx_1}")
    print(f"Transaction ID 1: {tx_1.get_txid()}")
    
    # Broadcast the first transaction
    txid_1 = proxy.sendrawtransaction(signed_tx_1)
    print(f"Broadcast transaction ID 1: {txid_1}")
    
    # Generate a block to confirm the first spend
    proxy.generatetoaddress(1, addr)
    print(f"Balance after first spend: {proxy.getbalance()} BTC")
    
    # ============================================================================
    # STEP 4: Second spend - Script Path (from remaining UTXO)
    # ============================================================================
    print("\n" + "="*60)
    print("STEP 4: Second spend - Script Path")
    print("="*60)
    
    # Create a destination address for the second spend
    dest_private_key_2 = PrivateKey()
    dest_address_2 = dest_private_key_2.get_public_key().get_address()
    print(f"Destination address 2: {dest_address_2.to_string()}")
    
    # Create transaction input from the remaining UTXO (change from first transaction)
    txin_2 = TxInput(txid_1, 1)  # The change output from the first transaction
    
    # Create transaction output (send most of the remaining funds)
    spend_amount_2 = 0.08
    txout_2 = TxOutput(to_satoshis(spend_amount_2), dest_address_2.to_script_pub_key())
    
    # Create the transaction
    tx_2 = Transaction([txin_2], [txout_2], has_segwit=True)
    print(f"Raw unsigned transaction 2:\n{tx_2.serialize()}")
    
    # For script path spending, we need to spend from the original Taproot address
    # But since we already spent from it in the key path, we need to create a new funding transaction
    # Let's fund the Taproot address again for the script path demonstration
    print("\nFunding Taproot address again for script path demonstration...")
    tx_fund_2 = proxy.sendtoaddress(taproot_address.to_string(), 0.15)
    proxy.generatetoaddress(1, addr)
    
    # Get the new UTXO details
    tx_details_2 = proxy.gettransaction(tx_fund_2)
    vout_2 = None
    for detail in tx_details_2['details']:
        if detail['address'] == taproot_address.to_string():
            vout_2 = detail['vout']
            break
    
    print(f"New UTXO at vout: {vout_2}")
    
    # Create transaction input from the new Taproot UTXO
    txin_script = TxInput(tx_fund_2, vout_2)
    
    # Create the script path transaction
    tx_script = Transaction([txin_script], [txout_2], has_segwit=True)
    print(f"Script path Raw unsigned transaction:\n{tx_script.serialize()}")
    
    # Sign using script path (script_1)
    amounts_script = [to_satoshis(0.15)]
    utxo_script_pubkeys_script = [taproot_address.to_script_pub_key()]
    
    sig_script = script_key_1.sign_taproot_input(
        tx_script,
        0,
        utxo_script_pubkeys_script,
        amounts_script,
        script_path=True,
        tapleaf_script=script_1,
        tweak=False  # Don't tweak for script path
    )
    print(f"Script path signature: {sig_script}")
    
    # Create the control block (merkle path)
    control_block = ControlBlock(internal_public_key, taproot_scripts, 0, is_odd=taproot_address.is_odd())
    print(f"Control Block: {control_block.to_hex()}")
    
    # Add the witness (signature + script + control block)
    tx_script.witnesses.append(TxWitnessInput([sig_script, script_1.to_hex(), control_block.to_hex()]))
    
    # Get the signed transaction
    signed_tx_script = tx_script.serialize()
    print(f"Script path Raw signed transaction:\n{signed_tx_script}")
    print(f"Script path Transaction ID: {tx_script.get_txid()}")
    
    # Broadcast the script path transaction
    txid_script = proxy.sendrawtransaction(signed_tx_script)
    print(f"Script path Broadcast transaction ID: {txid_script}")
    
    # Generate a block to confirm the script path spend
    proxy.generatetoaddress(1, addr)
    print(f"Final balance: {proxy.getbalance()} BTC")
    
    # ============================================================================
    # STEP 5: Verify the results
    # ============================================================================
    print("\n" + "="*60)
    print("STEP 5: Verification")
    print("="*60)
    
    # Verify both transactions
    try:
        raw_tx_1 = proxy.getrawtransaction(txid_1, True)
        raw_tx_script = proxy.getrawtransaction(txid_script, True)
        
        print(f"Key path transaction confirmations: {raw_tx_1.get('confirmations', 0)}")
        print(f"Script path transaction confirmations: {raw_tx_script.get('confirmations', 0)}")
        
        # Check witness data for both transactions
        if 'vin' in raw_tx_1 and len(raw_tx_1['vin']) > 0:
            witness_1 = raw_tx_1['vin'][0].get('txinwitness', [])
            print(f"Key path witness: {witness_1}")
            
        if 'vin' in raw_tx_script and len(raw_tx_script['vin']) > 0:
            witness_script = raw_tx_script['vin'][0].get('txinwitness', [])
            print(f"Script path witness: {witness_script}")
            
    except Exception as e:
        print(f"Could not get transaction details: {e}")
    
    print("\n" + "="*60)
    print("TAPROOT COMPLETE FLOW COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("Summary:")
    print(f"- Created Taproot address: {taproot_address.to_string()}")
    print(f"- Funded with: {funding_amount} BTC (first funding)")
    print(f"- Key path spend: {spend_amount_1} BTC to {dest_address_1.to_string()}")
    print(f"- Script path spend: {spend_amount_2} BTC to {dest_address_2.to_string()}")
    print(f"- Transaction IDs:")
    print(f"  Key path: {txid_1}")
    print(f"  Script path: {txid_script}")
    print(f"- Internal key (WIF): {internal_private_key.to_wif()}")
    print(f"- Script keys (WIF):")
    print(f"  Script 1: {script_key_1.to_wif()}")
    print(f"  Script 2: {script_key_2.to_wif()}")
    print(f"- Scripts:")
    print(f"  Script 1: {script_1.to_hex()}")
    print(f"  Script 2: {script_2.to_hex()}")
    print(f"- Demonstrated both key path and script path spending from same address!")


if __name__ == "__main__":
    main() 