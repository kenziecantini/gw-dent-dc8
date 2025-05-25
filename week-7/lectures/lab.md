
# Web 3.0 Security Investigation Lab

## Introduction

This lab provides hands-on experience investigating security issues in Web 3.0 technologies, including blockchain, cryptocurrency, and decentralized applications (dApps). Through five use cases, you will explore historical and ongoing security challenges—such as smart contract vulnerabilities, phishing attacks, and ransomware payment tracing—using freely accessible online tools. Each use case combines an overview of the incident or issue with step-by-step instructions for practical investigation.

By completing this lab, you will:
- Understand key security risks in Web 3.0 ecosystems.
- Learn to use blockchain explorers and security tools to analyze transactions and smart contracts.
- Develop skills in identifying phishing attempts and tracing cryptocurrency flows.

---

## Use Case 1: Investigate the DAO Hack Using Etherscan
- **What Happened**: The DAO (Decentralized Autonomous Organization) was a venture capital fund on Ethereum. In June 2016, an attacker exploited a reentrancy vulnerability in its smart contract, draining 3.6 million Ether (worth ~$70 million at the time). This led to a controversial Ethereum hard fork to recover the funds.
- **When**: June 17, 2016.
- **Significance**: The DAO hack exposed smart contract vulnerabilities and emphasized the need for rigorous security audits in decentralized systems.
- **Tool**: [Etherscan](https://etherscan.io/)
- **Objective**: Trace the transactions from the DAO hack to understand the exploit.
- **Learning Outcome**: Learn how blockchain transparency reveals exploits and understand reentrancy risks.

### Step-by-Step Instructions
1. Open your browser and go to [https://etherscan.io/](https://etherscan.io/).
2. In the search bar, paste the DAO contract address: `0xbb9bc244d798123fde783fcc1c72d3bb8c189413`, then press "Enter."
3. On the contract page, check the "Balance" section for the current Ether balance, then click the "Transactions" tab to see all related transactions. Note the high activity around June 2016.
4. Scroll or filter transactions by date (around June 17, 2016). 
5. On the "Transaction Details" page, observe:
   - **From**: The attacker’s address (clickable).
   - **To**: The DAO contract address.
   - **Value**: Ether stolen in this transaction.
   - **Transaction Receipt Status**: Should say "Success."
6. Click the attacker’s address under "From" and view its transactions to see where the stolen Ether went.
7. Note how the attacker used multiple transactions to drain funds, exploiting reentrancy.

---

## Use Case 2: Analyze a Smart Contract for Vulnerabilities Using Remix
- **What Happened**: Smart contracts can have vulnerabilities like reentrancy, where a malicious contract repeatedly calls back into the vulnerable one before it finishes executing, potentially draining funds. This remains a persistent risk in blockchain development.
- **When**: Ongoing incidents.
- **Significance**: Preventing smart contract vulnerabilities is critical for secure dApps.
- **Tool**: [Remix IDE](https://remix.ethereum.org/)
- **Objective**: Identify security flaws in a sample Solidity contract using static analysis.
- **Learning Outcome**: Spot vulnerabilities like reentrancy and value secure coding practices.

### Step-by-Step Instructions
1. Open your browser and go to [https://remix.ethereum.org/](https://remix.ethereum.org/).
2. In the left sidebar under "File Explorer," click "+" and name the file `Vulnerable.sol`.
3. Paste this code into the editor:
   ```solidity
   pragma solidity ^0.8.0;
   contract Vulnerable {
       mapping(address => uint) public balances;
       function withdraw() public {
           uint amount = balances[msg.sender];
           if (amount > 0) {
               (bool sent, ) = msg.sender.call{value: amount}("");
               require(sent, "Failed to send Ether");
               balances[msg.sender] = 0;
           }
       }
       function deposit() public payable {
           balances[msg.sender] += msg.value;
       }
   }
   ```
4. Click the "Solidity Compiler" tab (small "S" icon) on the left, ensure the compiler version is `0.8.0` or higher, and click "Compile Vulnerable.sol."
5. Go to the "Solidity Static Analysis" tab (magnifying glass over code icon), select "Vulnerable," and click "Run."
6. Review warnings like "Reentrancy." Note how the contract sends Ether before updating the balance, making it vulnerable.
7. Observe the risks highlighted in the analysis results.

---

## Use Case 3: Investigate a Phishing Website Targeting Cryptocurrency Users
- **What Happened**: Phishing scams trick crypto users into visiting fake websites mimicking legitimate services (e.g., MetaMask) to steal private keys or credentials. This is a widespread, ongoing threat.
- **When**: Ongoing; no specific date.
- **Significance**: Recognizing phishing is vital for protecting digital assets in decentralized environments.
- **Tools**: [PhishTank](https://phishtank.org/), [Google Safe Browsing](https://transparencyreport.google.com/safe-browsing/search)
- **Objective**: Investigate a suspicious URL for phishing traits and red flags.
- **Learning Outcome**: Identify phishing tactics and verify website safety with online tools.

### Step-by-Step Instructions
1. Open your browser and go to [https://phishtank.org/](https://phishtank.org/).
2. In the "Search" bar, paste `http://metamask-login.com` and click "Search."
3. Check if the URL is listed and its status (e.g., "Online" or "Offline"). If not found, proceed to the next step.
4. Go to [https://transparencyreport.google.com/safe-browsing/search](https://transparencyreport.google.com/safe-browsing/search).
5. Paste `http://metamask-login.com` into the "Enter a URL" field and click "Search."
6. Look for "No unsafe content found" or a warning like "Deceptive site."
7. In a safe environment (e.g., virtual machine), visit the URL and check:
   - **HTTPS**: Padlock in the address bar (HTTP is a red flag).
   - **Domain**: Compare to `metamask.io` (official) vs. `metamask-login.com`.
   - **Content**: Look for login forms requesting private keys or seed phrases.
8. Note phishing signs like domain typos or sensitive data requests.

---

## Use Case 4: Trace a Ransomware Bitcoin Address Using Blockchain.com
- **What Happened**: Ransomware attacks like WannaCry (May 2017) encrypt victims’ data and demand Bitcoin payments. WannaCry impacted thousands globally, using Bitcoin addresses for ransoms. Tracing these payments reveals fund movements, though pseudo-anonymity complicates it.
- **When**: May 2017 (WannaCry); ransomware persists today.
- **Significance**: Blockchain forensics can track illicit flows, aiding investigations.
- **Tools**: [BitcoinAbuse](https://www.bitcoinabuse.com/), [Blockchain.com](https://www.blockchain.com/explorer)
- **Objective**: Trace transactions from a ransomware-linked Bitcoin address.
- **Learning Outcome**: Explore blockchain forensics and tracing challenges.

### Step-by-Step Instructions
1. Open your browser and go to [https://www.bitcoinabuse.com/](https://www.bitcoinabuse.com/).
2. In the "Search" bar, type `ransomware`, press "Enter," and pick an address with multiple reports (e.g., `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`).
3. Copy the chosen address.
4. Go to [https://www.blockchain.com/explorer](https://www.blockchain.com/explorer).
5. Paste the address into the search bar and press "Enter."
6. Check "Total Received" and "Total Sent" amounts, then scroll to view transactions.
7. Click a transaction to see "Inputs" (source) and "Outputs" (destination).
8. Observe patterns like fund splitting or transfers to exchanges, hinting at cash-out attempts.

---

## Use Case 5: Analyze a DeFi Hack Transaction Using Etherscan
- **What Happened**: In the Harvest Finance hack (October 26, 2020), an attacker used a flash loan vulnerability to manipulate the DeFi protocol and steal funds. Flash loans, enabling large uncollateralized borrowing, are often exploited in DeFi to manipulate prices or drain pools.
- **When**: October 26, 2020.
- **Significance**: DeFi hacks underscore risks in smart contract interactions and the need for robust security.
- **Tool**: [Etherscan](https://etherscan.io/)
- **Objective**: Analyze a transaction from the Harvest Finance hack to understand the exploit.
- **Learning Outcome**: Interpret complex blockchain transactions and recognize DeFi vulnerabilities.

### Step-by-Step Instructions
1. Open your browser and go to [https://etherscan.io/](https://etherscan.io/).
2. Ask your instructor for a specific Harvest Finance hack transaction hash (e.g., `0x...`), then paste it into the search bar and press "Enter."
3. On the "Transaction Details" page, check "From" and "To" addresses, "Value" (Ether transferred), and any "Tokens Transferred."
4. Scroll to "Input Data" and click "Decode Input Data" (if available) to see function calls or parameters used in the exploit.
5. Click the "Logs" tab to view events like token swaps or approvals.
6. Go to the "ERC20 Token Txns" tab and look for large or unusual token movements indicating the exploit’s mechanics.
7. Identify how the attacker used flash loans or price manipulation to drain funds.

---

## Reflection and Discussion
Reflect on your findings after completing the activities:
- What surprised you about blockchain transaction transparency?
- How do crypto phishing tactics differ from traditional web phishing?
- What challenges arose when tracing ransomware payments, and how might attackers hide their tracks?
- Based on the smart contract analysis, what secure coding practices would you recommend?
- How do DeFi hacks exploit protocol composability?

