/*
    ThreatLens-AI - Custom YARA Rules
    Member: Vamshi - YARA & Signature Detection Engine
    Branch: feat/yara-signature-engine
*/

rule EICAR_Test_File
{
    meta:
        description = "Detects the standard EICAR antivirus test string"
        author = "Vamshi"
        severity = "test"
        category = "test"

    strings:
        $eicar = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

    condition:
        $eicar
}

rule Trojan_Suspicious_CMD_Execution
{
    meta:
        description = "Flags files referencing command shell / remote execution patterns typical of trojans"
        author = "Vamshi"
        severity = "medium"
        category = "trojan"

    strings:
        $cmd1 = "cmd.exe /c" nocase
        $cmd2 = "powershell -enc" nocase
        $cmd3 = "WScript.Shell" nocase
        $cmd4 = "CreateRemoteThread" nocase

    condition:
        any of them
}

rule Trojan_Packed_PE_Indicator
{
    meta:
        description = "Flags PE files with common packer section names, often used to hide trojan payloads"
        author = "Vamshi"
        severity = "medium"
        category = "trojan"

    strings:
        $upx1 = "UPX0"
        $upx2 = "UPX1"
        $section_packed = ".packed"

    condition:
        uint16(0) == 0x5A4D and any of them
}

rule Ransomware_Note_Indicators
{
    meta:
        description = "Flags strings commonly found in ransomware ransom notes and file extensions"
        author = "Vamshi"
        severity = "high"
        category = "ransomware"

    strings:
        $note1 = "README_DECRYPT" nocase
        $note2 = "your files have been encrypted" nocase
        $note3 = "DECRYPT_INSTRUCTIONS" nocase
        $ext1 = ".locked"
        $ext2 = ".encrypted"

    condition:
        any of them
}

rule Ransomware_Crypto_API_Usage
{
    meta:
        description = "Flags use of Windows crypto APIs commonly abused by ransomware to encrypt files"
        author = "Vamshi"
        severity = "high"
        category = "ransomware"

    strings:
        $api1 = "CryptEncrypt"
        $api2 = "CryptGenKey"
        $api3 = "CryptAcquireContext"

    condition:
        2 of them
}

rule Webshell_PHP_Generic
{
    meta:
        description = "Flags common PHP webshell patterns that allow remote code execution"
        author = "Vamshi"
        severity = "high"
        category = "webshell"

    strings:
        $php1 = "eval(base64_decode" nocase
        $php2 = "<?php system(" nocase
        $php3 = "shell_exec(" nocase
        $php4 = "passthru(" nocase

    condition:
        any of them
}

rule Webshell_ASPX_Generic
{
    meta:
        description = "Flags common ASPX webshell patterns"
        author = "Vamshi"
        severity = "high"
        category = "webshell"

    strings:
        $aspx1 = "Process.Start" nocase
        $aspx2 = "cmd.exe /c" nocase
        $aspx3 = "Eval Request" nocase

    condition:
        any of them
}