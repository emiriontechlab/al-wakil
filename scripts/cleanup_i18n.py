from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]

AR_SEO = {
    "index.html": (
        "الأدوات الصحية وحلول الحمامات في الإمارات | الوكيل",
        "الوكيل يورد الأدوات الصحية وإكسسوارات الحمامات وتجهيزاتها وحلول الديكور الداخلي في الإمارات للمنازل والفلل والمساحات التجارية.",
    ),
    "about.html": (
        "من نحن | الوكيل لحلول الحمامات والديكور في الإمارات",
        "تعرف على الوكيل لتجارة مواد البناء، مورد موثوق للأدوات الصحية وتجهيزات الحمامات والبلاط والرخام وحلول الديكور الداخلي في الإمارات.",
    ),
    "products.html": (
        "منتجات الحمامات والأدوات الصحية في الإمارات | الوكيل للتجارة",
        "استكشف منتجات الوكيل من الأدوات الصحية وتجهيزات الحمامات والبلاط والرخام والمواد الداخلية للمشاريع السكنية والتجارية في الإمارات.",
    ),
    "ravena.html": (
        "أدوات صحية فاخرة في الإمارات | رافينا من الوكيل",
        "اكتشف رافينا، العلامة التابعة للوكيل، مع تشكيلة فاخرة من مغاسل الحمامات والخلاطات وأنظمة الدش وإكسسوارات الحمامات في الإمارات.",
    ),
    "blog.html": (
        "مدونة الوكيل | البلاط والأدوات الصحية ومواد البناء",
        "اقرأ إرشادات عملية حول اختيار الأدوات الصحية والبلاط والرخام وحلول الحمامات والديكور الداخلي للمشاريع في الإمارات.",
    ),
    "contact.html": (
        "اتصل بالوكيل | مواد الحمامات والديكور في الإمارات",
        "تواصل مع الوكيل لتجارة مواد البناء في الشارقة للاستفسار عن الأدوات الصحية وتجهيزات الحمامات والبلاط والرخام وحلول المشاريع في الإمارات.",
    ),
}

REPLACEMENTS = {
    "الوكيلBRAND": "الوكيل",
    "الوكيل براند": "الوكيل",
    "رافينا براند": "رافينا",
    "العلامة التجارية الوكيل": "الوكيل",
    "الوكيل Trading": "الوكيل للتجارة",
    "الوكيل للتجارة Trading": "الوكيل للتجارة",
    "شركة الوكيل للتجارة Trading": "شركة الوكيل للتجارة",
    "Al WakilUAE": "Al Wakil UAE",
    "Al Wakilworks": "Al Wakil works",
    "Al Wakilsanitary": "Al Wakil sanitary",
    "Al Wakilhelps": "Al Wakil helps",
    "<p>???? ??????? ???? ???? ????? ????? ?????? ????? ?????? ???? ?? ???? ????? ?????? ?????.</p>": (
        "<p>بلاط بورسلان فاخر كبير الحجم بنقشة رخامية خضراء زمردية غنية مع عروق بيضاء وذهبية لافتة.</p>"
    ),
}

EN_REPLACEMENTS = {
    "<p>???? ??????? ???? ???? ????? ????? ?????? ????? ?????? ???? ?? ???? ????? ?????? ?????.</p>": (
        "<p>Exquisite large-format porcelain tile featuring a rich emerald green marble pattern "
        "accented by dramatic white and gold crystalline veining.</p>"
    ),
}


def write_html(path: Path, soup: BeautifulSoup) -> None:
    text = str(soup)
    if text.startswith("<!DOCTYPE html>"):
        path.write_text(text, encoding="utf-8")
    else:
        path.write_text("<!DOCTYPE html>\n" + text.lstrip().removeprefix("<!DOCTYPE html>").lstrip(), encoding="utf-8")


def main() -> None:
    for path in list(ROOT.glob("*.html")) + list((ROOT / "en").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        for source, target in REPLACEMENTS.items():
            text = text.replace(source, target)
        if path.parent.name == "en":
            for source, target in EN_REPLACEMENTS.items():
                text = text.replace(source, target)
        path.write_text(text, encoding="utf-8")

    for name, (title, description) in AR_SEO.items():
        path = ROOT / name
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        if soup.title:
            soup.title.string = title
        for meta in soup.find_all("meta"):
            key = meta.get("name") or meta.get("property")
            if key in {"description", "og:description"}:
                meta["content"] = description
            if key == "og:title":
                meta["content"] = title
            if key == "keywords":
                meta["content"] = "الأدوات الصحية الإمارات, حلول الحمامات الإمارات, تجهيزات الحمامات, البلاط والرخام, الوكيل للتجارة"
        write_html(path, soup)


if __name__ == "__main__":
    main()
