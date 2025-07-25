# Bitcoin Examples Overview

This directory contains comprehensive working examples of Bitcoin address types, funding, and spending using the bitcoinutils library with a Bitcoin regtest node.

## Examples Included

### P2SH (Pay-to-Script-Hash) Examples

#### 1. Basic P2SH Example (`p2shFullflow.py`)
- ✅ **Complete P2SH lifecycle**: Create → Fund → Spend
- ✅ **Single signature P2PK wrapped in P2SH**
- ✅ **Proper transaction signing and broadcasting**
- ✅ **Comprehensive verification and error handling**

#### 2. Advanced Multisig P2SH Example (`p2shMultisigExample.py`)
- ✅ **2-of-3 multisignature P2SH address**
- ✅ **Multiple signature creation and validation**
- ✅ **Complex redeem script structure**
- ✅ **Real-world multisig use case**

### Taproot Examples

#### 3. Basic Taproot Key Path Example (`taprootKeyPathExample.py`)
- ✅ **Complete key path flow**: Create → Fund → Spend
- ✅ **Simple Taproot address** (no scripts)
- ✅ **Direct signature spending** with automatic key tweaking
- ✅ **Minimal witness data** (just signature)
- ✅ **Most efficient Taproot spending method**

#### 4. Advanced Taproot Script Path Example (`taprootScriptPathExample.py`)
- ✅ **Complete script path flow**: Create → Fund → Spend
- ✅ **Multiple script types** (P2PK, 2-of-2 multisig)
- ✅ **Script path spending** with control blocks
- ✅ **Merkle path verification**
- ✅ **Complex witness structure** (signature + script + control block)

#### 5. Taproot Comparison Example (`taprootComparisonExample.py`)
- ✅ **Side-by-side comparison** of key path vs script path
- ✅ **Two separate Taproot addresses** with different characteristics
- ✅ **Transaction size and efficiency analysis**
- ✅ **Use case demonstrations**

## How to Run

1. Ensure your Bitcoin regtest node is running
2. Activate the virtual environment: `source bin/activate`
3. Run any example:

```bash
# P2SH Examples
python examples/p2shFullflow.py
python examples/p2shMultisigExample.py

# Taproot Examples
python examples/taprootKeyPathExample.py
python examples/taprootScriptPathExample.py
python examples/taprootComparisonExample.py
```

## Technical Comparison

### P2SH vs Taproot

| Feature | P2SH | Taproot |
|---------|------|---------|
| **Address Length** | Longer | Shorter |
| **Privacy** | Script visible on-chain | Script hidden until spending |
| **Efficiency** | Larger transactions | Smaller transactions |
| **Flexibility** | Limited script types | Any script type |
| **Security** | ECDSA signatures | Schnorr signatures |
| **Complexity** | Medium | High (but more powerful) |

### Key Path vs Script Path (Taproot)

| Feature | Key Path | Script Path |
|---------|----------|-------------|
| **Witness Structure** | `[signature]` | `[signature, script, control_block]` |
| **Transaction Size** | ~153 bytes | ~254 bytes |
| **Virtual Size** | ~102 vbytes | ~128 vbytes |
| **Complexity** | Simple | Complex |
| **Efficiency** | Most efficient | Less efficient but more flexible |
| **Use Case** | Simple payments | Advanced spending conditions |

## Key Features Demonstrated

### P2SH Features
- **Redeem Script Creation**: Both simple (`<pubkey> OP_CHECKSIG`) and complex (2-of-3 multisig) scripts
- **Proper ScriptSig Structure**: Including the required `OP_0` dummy value for multisig
- **Error Handling**: Graceful handling of wallet loading and transaction verification
- **Complete Lifecycle**: From address creation to successful spending

### Taproot Features
- **Schnorr Signatures**: More efficient than ECDSA
- **Key Tweaking**: Automatic when scripts are present
- **Merkle Trees**: Efficient script organization
- **Privacy**: All spends look identical on-chain
- **Flexibility**: Support for any script type

## Common Use Cases

### P2SH Use Cases
- **Multisignature Wallets**: Require multiple signatures to spend
- **Time-locked Transactions**: Spend only after a certain time
- **Escrow Services**: Complex spending conditions for escrow
- **Smart Contracts**: Implement custom spending logic

### Taproot Use Cases
- **Simple Payments**: Key path for regular transactions
- **Multisignature Wallets**: Script path with multisig scripts
- **Time-locked Transactions**: Script path with time conditions
- **Escrow Services**: Complex script conditions
- **Smart Contracts**: Advanced spending logic

## Verification Features

All examples include comprehensive verification:
- Transaction confirmation status
- Output amounts
- Raw transaction details
- Witness data inspection (for Taproot)
- Complete transaction lifecycle tracking

## Output Examples

### P2SH Example Output
```
============================================================
P2SH FLOW COMPLETED SUCCESSFULLY!
============================================================
Summary:
- Created P2SH address: 2N63pdBBttQBg9c44UcxdzCkPZPk6n8EJUg
- Funded with: 0.1 BTC
- Spent: 0.09 BTC to my6pPzb1ftrwr92bHaBqG4w49AqDZ29fsp
- Transaction ID: 781b2e51a4b72c39603a47c19296464d84bdc98f0d198735a8706b20cf4a387f
- Redeem script: 21030d7851af1ffacdff29f9d1e6c7d455575e49211acc926aedc05eb5beae741798ac
- Private key (WIF): cUooyFo3LAVSwtG87q4XAnVio1RpcY9gCiA8GD4FupXnSpbdQeNr
```

### Taproot Example Output
```
============================================================
TAPROOT KEY PATH FLOW COMPLETED SUCCESSFULLY!
============================================================
Summary:
- Created Taproot address: bcrt1p4v6vqjcref0438d6qdapwtw9fnmgsq3q08y07w0lhjmpyzuaqndsm8gpwz
- Funded with: 0.1 BTC
- Spent: 0.09 BTC to ms6mN6my7wzZaZLnf6gWEB5A2QW5TwVWp9
- Transaction ID: de31e8d53d5faccfadb2fbbfe738b960bc24eef97713cd5d3ad7710b06b4ee3a
- Private key (WIF): cTV4VSqHNcTNgW8Buw9DpqupEMdzL6VbFwvWTEDyuXHu4UXqNqAF
- Spending method: Key path (direct signature)
```

## Key Classes Used

### P2SH Classes
- `P2shAddress`: Creates P2SH addresses from scripts
- `PrivateKey`: Generates and manages private keys
- `Script`: Creates and manipulates Bitcoin scripts
- `Transaction`: Builds and signs transactions
- `NodeProxy`: Interfaces with the Bitcoin node

### Taproot Classes
- `PrivateKey`: Generates and manages private keys
- `Script`: Creates and manipulates Bitcoin scripts
- `Transaction`: Builds and signs transactions
- `TxWitnessInput`: Creates witness data
- `ControlBlock`: Creates merkle paths for script spending
- `NodeProxy`: Interfaces with the Bitcoin node

## Troubleshooting

- **Wallet Loading Issues**: All examples handle wallet loading gracefully
- **Transaction Verification**: Uses `getrawtransaction` for reliable verification
- **Error Handling**: Comprehensive error handling for all Bitcoin node operations
- **Script Limitations**: Current Taproot implementation supports up to 2 scripts per address

## Next Steps

These examples provide a foundation for:
- Building more complex Bitcoin scripts
- Implementing time-locked transactions
- Creating custom smart contracts
- Developing advanced Bitcoin applications
- Understanding privacy features of different address types
- Learning Schnorr signatures and Taproot benefits

## Documentation Files

- `README_P2SH.md`: Comprehensive P2SH documentation
- `README_TAPROOT.md`: Comprehensive Taproot documentation
- `README_ALL_EXAMPLES.md`: This overview file

All examples are production-ready and include comprehensive error handling and verification steps. 