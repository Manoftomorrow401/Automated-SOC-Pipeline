# Automated-SOC-Pipeline

Step-by-Step Implementation
1. Wazuh Detection Engineering
Configured /var/ossec/etc/rules/local_rules.xml to catch repeated SSH failures within a 60-second window:

<group name="local,syslog,sshd,">
  <rule id="100002" level="10" frequency="5" timeframe="60">
    <if_matched_sid>5710</if_matched_sid>
    <description>SOC Project Alert: SSH Authentication Failure Detected</description>
    <mitre>
      <id>T1110</id>
      <tactic>Credential Access</tactic>
      <technique>Brute Force</technique>
    </mitre>
    <group>authentication_failures,</group>
  </rule>
</group>

2. Wazuh-to-Shuffle Integration Hook
In /var/ossec/etc/ossec.conf:

<integration>
  <name>custom-shuffle</name>
  <rule_id>100002</rule_id>
  <hook_url>http://<SHUFFLE_HOST>:3001/api/v1/hooks/webhook_<HOOK_ID></hook_url>
  <alert_format>json</alert_format>
</integration>

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
