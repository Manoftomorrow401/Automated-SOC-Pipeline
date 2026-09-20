# Automated-SOC-Pipeline

Step-by-Step Implementation
1. Wazuh Detection Engineering
Configured /var/ossec/etc/rules/local_rules.xml to catch repeated SSH failures within a 60-second window:

Please check wazuh/local_rules.xml for rule code

2. Wazuh-to-Shuffle Integration Hook
In /var/ossec/etc/ossec.conf:

Please check wazuh/ossec_integration_snippet.xml

3. Shuffle SOAR Workflow Configuration
Trigger: Webhook receiving Wazuh alert JSON ($exec).

Enrichment Node: AbuseIPDB_v2_1 querying attacking IP with lookback window.

Dispatch Node: Native HTTP node using POST method pointing to Discord incoming webhook.

{
  "content": "**[SOC INCIDENT] SSH Brute-Force Detected**\n- Host: $exec.agent.name\n- Attacked User: $exec.data.srcuser\n- Attacker IP: $exec.data.srcip\n- Rule ID: $exec.rule.id (Severity: Level $exec.rule.level)\n- AbuseIPDB Confidence: $abuseipdb_v2_1.body.data.abuseConfidenceScore%\n- Country: $abuseipdb_v2_1.body.data.countryCode\n- Total Reports: $abuseipdb_v2_1.body.data.totalReports\n- Event Timestamp: $exec.timestamp"
}

Simulated brute-force attack from external/local endpoint:

ssh invaliduser999@127.0.0.1

Verified Incident Card Output (Discord Channel)

[SOC INCIDENT ALERT] SSH Brute-Force Detected
• Host: Ubuntu26
• Attacked User: invaliduser999
• Attacker IP: 127.0.0.1
• Rule ID: 100002 (Level 10)
• Abuse Confidence: 7%
• Country: CN
• Total Reports: 2
• Timestamp: 2026-09-19T13:37:41+0000
