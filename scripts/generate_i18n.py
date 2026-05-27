from __future__ import annotations

from pathlib import Path
import re
import time

from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
from deep_translator import GoogleTranslator


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://alwakil.ae"
HTML_FILES = sorted([p for p in ROOT.glob("*.html") if p.is_file()])
PAGE_NAMES = [p.name for p in HTML_FILES]
EN_DIR = ROOT / "en"
ARABIC_LABEL = "\u0627\u0644\u0639\u0631\u0628\u064a\u0629"

SKIP_PARENTS = {"script", "style", "svg", "path", "source", "canvas"}
TEXT_ATTRS = ["alt", "aria-label", "title", "placeholder", "data-blog-title"]
META_TEXT_KEYS = {
    "description",
    "keywords",
    "og:title",
    "og:description",
    "twitter:title",
    "twitter:description",
}

AR_OVERRIDES = {
    "Home": "الرئيسية",
    "About": "من نحن",
    "Products": "المنتجات",
    "Ravena": "رافينا",
    "Blog": "المدونة",
    "Contact": "اتصل بنا",
    "English": "English",
    "العربية": "العربية",
    "Al Wakil": "الوكيل",
    "ALWAKIL": "الوكيل",
    "RAVENA": "رافينا",
    "THE LUXURY DESTINATION": "وجهة الفخامة",
    "Explore Our Products": "استكشف منتجاتنا",
    "Learn More": "اعرف المزيد",
    "View Less": "عرض أقل",
    "Request a Quote": "اطلب عرض سعر",
    "Talk to Our Team": "تحدث إلى فريقنا",
    "Get In Touch": "تواصل معنا",
    "All rights reserved.": "جميع الحقوق محفوظة.",
    "Powered by Emirion techlab": "مدعوم من Emirion techlab",
    "Call Al Wakil": "اتصل بالوكيل",
    "WhatsApp Al Wakil": "واتساب الوكيل",
    "Email Al Wakil": "راسل الوكيل",
    "LinkedIn Al Wakil": "لينكدإن الوكيل",
    "Chat with us on WhatsApp": "تحدث معنا عبر واتساب",
    "20+ years experience": "خبرة أكثر من 20 عاماً",
    "Quality standard products": "منتجات بمعايير جودة عالية",
    "Premium showroom visuals": "تجربة عرض راقية",
    "Who We Are": "من نحن",
    "What We Do": "ما نقدمه",
    "Why Choose Us": "لماذا تختارنا",
    "Our Mission": "رسالتنا",
    "Our Vision": "رؤيتنا",
    "Our Values": "قيمنا",
    "Founder & CEO": "المؤسس والرئيس التنفيذي",
    "Project support": "دعم المشاريع",
    "Years experience": "سنوات خبرة",
    "Complete solutions": "حلول متكاملة",
    "Sanitary ware": "الأدوات الصحية",
    "Bathroom fittings": "تجهيزات الحمامات",
    "Tiles and surfaces": "البلاط والأسطح",
    "Marble and stone finishes": "تشطيبات الرخام والحجر",
    "Interior accessories": "إكسسوارات الديكور الداخلي",
}

EN_OVERRIDES = {
    "الرئيسية": "Home",
    "من نحن": "About",
    "المنتجات": "Products",
    "رافينا": "Ravena",
    "المدونة": "Blog",
    "اتصل بنا": "Contact",
    "الوكيل": "Al Wakil",
    "عرض أقل": "View Less",
    "جميع الحقوق محفوظة.": "All rights reserved.",
}

ar_translator = GoogleTranslator(source="en", target="ar")
en_translator = GoogleTranslator(source="auto", target="en")
CACHE_AR: dict[str, str] = {}
CACHE_EN: dict[str, str] = {}


def normalize(text: str) -> str:
    return " ".join(text.split())


def has_latin(text: str) -> bool:
    return bool(re.search(r"[A-Za-z]", text))


def has_arabic(text: str) -> bool:
    return bool(re.search(r"[\u0600-\u06ff]", text))


def is_external(url: str) -> bool:
    return bool(re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|//)", url or "", re.I))


def protect(text: str) -> str:
    replacements = {
        "Al Wakil": "ALWAKILBRAND",
        "ALWAKIL": "ALWAKILBRAND",
        "Al WakilUAE": "ALWAKILBRAND UAE",
        "Al Wakilworks": "ALWAKILBRAND works",
        "RAVENA": "RAVENABRAND",
        "Ravena": "RAVENABRAND",
        "UAE": "UAE",
        "Dubai": "Dubai",
        "Sharjah": "Sharjah",
        "Abu Dhabi": "Abu Dhabi",
        "Emirion techlab": "EMIRIONTECHLAB",
        "alwakil.ae": "ALWAKILDOMAIN",
    }
    for source, token in replacements.items():
        text = text.replace(source, token)
    return text


def unprotect_ar(text: str) -> str:
    return (
        text.replace("ALWAKILBRAND", "الوكيل")
        .replace("الوكيل براند", "الوكيل")
        .replace("الوكيلBRAND", "الوكيل")
        .replace("RAVENABRAND", "رافينا")
        .replace("رافينا براند", "رافينا")
        .replace("UAE", "الإمارات")
        .replace("Dubai", "دبي")
        .replace("Sharjah", "الشارقة")
        .replace("Abu Dhabi", "أبوظبي")
        .replace("EMIRIONTECHLAB", "Emirion techlab")
        .replace("ALWAKILDOMAIN", "alwakil.ae")
    )


def translate_ar(text: str) -> str:
    raw = normalize(text)
    if not raw or not has_latin(raw):
        return text
    if raw in AR_OVERRIDES:
        return AR_OVERRIDES[raw]
    if raw in CACHE_AR:
        return CACHE_AR[raw]
    try:
        translated = unprotect_ar(ar_translator.translate(protect(raw)))
    except Exception:
        translated = raw
    CACHE_AR[raw] = translated
    time.sleep(0.03)
    return translated


def translate_en(text: str) -> str:
    raw = normalize(text)
    if not raw or not has_arabic(raw):
        return text
    if raw in EN_OVERRIDES:
        return EN_OVERRIDES[raw]
    if raw in CACHE_EN:
        return CACHE_EN[raw]
    try:
        translated = en_translator.translate(raw)
    except Exception:
        translated = raw
    CACHE_EN[raw] = translated
    time.sleep(0.03)
    return translated


def page_url(page_name: str, lang: str) -> str:
    if lang == "en":
        return f"{SITE}/en/" if page_name == "index.html" else f"{SITE}/en/{page_name}"
    return f"{SITE}/" if page_name == "index.html" else f"{SITE}/{page_name}"


def parse_html(path: Path) -> BeautifulSoup:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for item in list(soup.contents):
        if isinstance(item, Doctype):
            item.extract()
    return soup


def write_html(path: Path, soup: BeautifulSoup) -> None:
    for item in list(soup.contents):
        if item is soup.html:
            continue
        if isinstance(item, Doctype) or (isinstance(item, NavigableString) and item.strip()):
            item.extract()
    path.write_text("<!DOCTYPE html>\n" + str(soup), encoding="utf-8")


def configure_html(soup: BeautifulSoup, lang: str) -> None:
    if soup.html:
        soup.html["lang"] = lang
        soup.html["dir"] = "rtl" if lang == "ar" else "ltr"
    if soup.body:
        classes = [c for c in soup.body.get("class", []) if c not in ("rtl", "ltr")]
        classes.append("rtl" if lang == "ar" else "ltr")
        soup.body["class"] = classes


def translate_soup(soup: BeautifulSoup, lang: str) -> None:
    translate = translate_ar if lang == "ar" else translate_en
    for node in list(soup.find_all(string=True)):
        if isinstance(node, Comment):
            continue
        if node.parent and node.parent.name in SKIP_PARENTS:
            continue
        raw = str(node)
        if not raw.strip():
            continue
        leading = raw[: len(raw) - len(raw.lstrip())]
        trailing = raw[len(raw.rstrip()) :]
        node.replace_with(NavigableString(leading + translate(raw.strip()) + trailing))
    for tag in soup.find_all(True):
        for attr in TEXT_ATTRS:
            if tag.has_attr(attr):
                tag[attr] = translate(tag[attr])
        if tag.name == "meta" and tag.has_attr("content"):
            key = tag.get("name") or tag.get("property")
            if key in META_TEXT_KEYS:
                tag["content"] = translate(tag["content"])


def set_seo(soup: BeautifulSoup, page_name: str, lang: str) -> None:
    if not soup.head:
        return
    for tag in list(soup.head.find_all("link")):
        rel = tag.get("rel", [])
        if "canonical" in rel or "alternate" in rel:
            tag.decompose()
    soup.head.append(soup.new_tag("link", rel="canonical", href=page_url(page_name, lang)))
    soup.head.append(soup.new_tag("link", rel="alternate", hreflang="ar", href=page_url(page_name, "ar")))
    soup.head.append(soup.new_tag("link", rel="alternate", hreflang="en", href=page_url(page_name, "en")))
    soup.head.append(soup.new_tag("link", rel="alternate", hreflang="x-default", href=page_url(page_name, "ar")))
    meta_lang = soup.head.find("meta", attrs={"http-equiv": "content-language"}) or soup.new_tag("meta")
    meta_lang["http-equiv"] = "content-language"
    meta_lang["content"] = lang
    if meta_lang.parent is None:
        soup.head.append(meta_lang)
    og_url = soup.head.find("meta", attrs={"property": "og:url"})
    if og_url:
        og_url["content"] = page_url(page_name, lang)


def prefix_asset(url: str) -> str:
    if is_external(url) or url.startswith("../") or url.startswith("data:"):
        return url
    return "../" + url


def update_paths(soup: BeautifulSoup, page_name: str, lang: str) -> None:
    for tag in soup.find_all(["link", "script", "img", "source", "video"]):
        for attr in ("href", "src", "poster"):
            if tag.has_attr(attr):
                value = tag[attr].strip()
                if value and not is_external(value) and not value.startswith("data:"):
                    value = value[3:] if value.startswith("../") else value
                    tag[attr] = prefix_asset(value) if lang == "en" else value

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if is_external(href):
            continue
        href = href[3:] if href.startswith("../") else href
        href = href[3:] if href.startswith("en/") else href
        anchor["href"] = href


def add_language_switch(soup: BeautifulSoup, page_name: str, lang: str) -> None:
    nav_links = soup.select_one(".nav-links")
    if not nav_links:
        return
    for old in nav_links.select(".language-switch"):
        old.decompose()
    ar_href = f"../{page_name}" if lang == "en" else page_name
    en_href = page_name if lang == "en" else f"en/{page_name}"
    for label, href, active in [
        (ARABIC_LABEL, ar_href, lang == "ar"),
        ("English", en_href, lang == "en"),
    ]:
        anchor = soup.new_tag("a", href=href)
        anchor.string = label
        anchor["class"] = "language-switch active" if active else "language-switch"
        nav_links.append(anchor)


def generate_sitemap() -> None:
    urls: list[str] = []
    for page in PAGE_NAMES:
        priority = "1.0" if page == "index.html" else ("0.7" if page == "blog.html" else "0.8")
        for lang in ("ar", "en"):
            urls.append(
                "\n".join(
                    [
                        "<url>",
                        f"<loc>{page_url(page, lang)}</loc>",
                        "<lastmod>2026-05-27</lastmod>",
                        "<changefreq>monthly</changefreq>",
                        f"<priority>{priority}</priority>",
                        "</url>",
                    ]
                )
            )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n'
        + "\n\n".join(urls)
        + "\n\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def main() -> None:
    EN_DIR.mkdir(exist_ok=True)

    for source in HTML_FILES:
        soup = parse_html(source)
        configure_html(soup, "en")
        translate_soup(soup, "en")
        set_seo(soup, source.name, "en")
        update_paths(soup, source.name, "en")
        add_language_switch(soup, source.name, "en")
        write_html(EN_DIR / source.name, soup)

    for source in HTML_FILES:
        soup = parse_html(source)
        configure_html(soup, "ar")
        translate_soup(soup, "ar")
        set_seo(soup, source.name, "ar")
        update_paths(soup, source.name, "ar")
        add_language_switch(soup, source.name, "ar")
        write_html(source, soup)

    generate_sitemap()
    print(f"Generated {len(PAGE_NAMES)} Arabic root pages and {len(PAGE_NAMES)} English pages.")
    print(f"Arabic translations cached: {len(CACHE_AR)}")
    print(f"English translations cached: {len(CACHE_EN)}")


if __name__ == "__main__":
    main()
