import re
from datetime import datetime, timezone


def build_report_download_filename(company_name: str, reviewed_at: datetime | None) -> str:
    """Return a human-readable filename for the PDF download.

    Format: {empresa-sanitizada}-informe-sics-{YYYY-MM-DD}.pdf
    Example: Acme-Costa-Rica-informe-sics-2026-05-24.pdf
    """
    date_str = (reviewed_at or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    sanitized = re.sub(r"[^\w\s-]", "", company_name.strip(), flags=re.UNICODE)
    sanitized = re.sub(r"[\s/_]+", "-", sanitized)
    sanitized = sanitized.strip("-")
    if len(sanitized) > 50:
        sanitized = sanitized[:50].rstrip("-")
    return f"{sanitized}-informe-sics-{date_str}.pdf"
