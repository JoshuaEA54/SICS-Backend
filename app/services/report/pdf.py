from pathlib import Path
from urllib.parse import unquote


def _link_callback(uri: str, _rel: str) -> str:
    """Resolve local file paths/URIs for xhtml2pdf asset loading."""
    if uri.startswith("file:"):
        raw = unquote(uri.removeprefix("file://").removeprefix("file:"))
        if raw.startswith("/") and len(raw) > 2 and raw[2] == ":":
            raw = raw.lstrip("/")
        path = Path(raw)
        if path.is_file():
            return str(path.resolve())

    path = Path(uri)
    if path.is_file():
        return str(path.resolve())

    return uri


def html_to_pdf(html: str, output_path: Path) -> None:
    from xhtml2pdf import pisa

    with output_path.open("wb") as dest:
        status = pisa.CreatePDF(
            html,
            dest=dest,
            encoding="utf-8",
            link_callback=_link_callback,
        )
    if status.err:
        raise RuntimeError("PDF generation failed")
