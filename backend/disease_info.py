"""Short, general advice per disease. Always confirm with a local agriculture officer."""
import re

# (crop keyword, disease keyword, about, action) - matched on normalised lowercase text
_DB = [
    ("apple", "scab", "Fungus (Venturia inaequalis). Olive-green to brown scabby spots on leaves and fruit; favoured by cool, wet weather.",
     "Collect and destroy fallen leaves, prune for airflow, and use a protectant fungicide as advised locally."),
    ("apple", "blackrot", "Fungus (Botryosphaeria obtusa). 'Frogeye' leaf spots, fruit rot and bark cankers.",
     "Prune out cankers and mummified fruit, keep the orchard clean, apply fungicide if pressure is high."),
    ("apple", "cedar", "Rust fungus that alternates between apple and juniper/cedar. Bright yellow-orange leaf spots.",
     "Remove nearby juniper if possible, choose resistant varieties, spray early in the season."),
    ("corn", "gray", "Fungus (Cercospora zeae-maydis). Long rectangular tan lesions between leaf veins; survives in crop residue.",
     "Rotate crops, manage residue, plant resistant hybrids; fungicide only if severe."),
    ("corn", "commonrust", "Fungus (Puccinia sorghi). Reddish-brown powdery pustules on both leaf surfaces.",
     "Use resistant hybrids and plant early; treat with fungicide only if it appears early and spreads."),
    ("corn", "northern", "Fungus (Exserohilum turcicum). Long cigar-shaped grey-green to tan lesions.",
     "Rotate crops, bury or remove residue, use resistant hybrids; fungicide if severe."),
    ("grape", "blackrot", "Fungus (Guignardia bidwellii). Brown circular leaf spots with dark margins; berries shrivel and turn black.",
     "Remove mummified berries, open the canopy, apply a protective fungicide from before bloom."),
    ("grape", "esca", "Fungal trunk-disease complex. 'Tiger-stripe' yellow/brown leaf pattern, berries with dark spots.",
     "No cure. Prune diseased wood in dry weather, disinfect tools, protect pruning wounds."),
    ("grape", "leafblight", "Fungus (Isariopsis). Angular brown spots on leaves, early leaf drop.",
     "Remove infected leaves, improve ventilation, apply copper or other recommended fungicide."),
    ("pepper", "bacterial", "Bacteria (Xanthomonas). Small water-soaked spots that turn brown; spreads in wet, windy weather.",
     "Use clean seed, avoid overhead watering and handling wet plants, rotate crops, copper spray can slow spread."),
    ("potato", "early", "Fungus (Alternaria solani). Brown spots with concentric 'target' rings, starting on older leaves.",
     "Rotate crops, fertilise in balance, remove debris, apply a protectant fungicide as per label."),
    ("potato", "late", "Oomycete (Phytophthora infestans). Dark water-soaked blotches, white mould underneath in humid weather. Spreads very fast.",
     "Act immediately: remove infected plants, avoid overhead irrigation, follow a fungicide programme, never store infected tubers."),
    ("tomato", "bacterial", "Bacteria (Xanthomonas). Small dark water-soaked spots, often with yellow halo.",
     "Use clean seed/seedlings, avoid overhead watering, rotate crops, copper spray can slow spread."),
    ("tomato", "early", "Fungus (Alternaria solani). Brown spots with concentric rings on lower leaves, then yellowing.",
     "Remove lower infected leaves, mulch, rotate crops, apply a protectant fungicide as per label."),
    ("tomato", "late", "Oomycete (Phytophthora infestans). Large greasy dark blotches; can destroy a crop in days in cool, wet weather.",
     "Remove and destroy infected plants, avoid wetting leaves, apply fungicide quickly and repeat as advised."),
    ("tomato", "mold", "Fungus (Passalora fulva). Yellow patches on top of leaves, olive-grey mould underneath; common in humid greenhouses.",
     "Lower humidity, ventilate, space plants, remove infected leaves."),
    ("tomato", "septoria", "Fungus (Septoria lycopersici). Many small round spots with dark edges and grey centres.",
     "Remove infected lower leaves, mulch, avoid splashing water, rotate crops."),
    ("tomato", "spider", "Pest, not a disease: two-spotted spider mites. Fine yellow stippling and webbing; thrives in hot, dry weather.",
     "Spray leaf undersides with water, neem or insecticidal soap; use a miticide if heavy; keep plants well watered."),
    ("tomato", "target", "Fungus (Corynespora cassiicola). Brown spots with concentric rings.",
     "Improve airflow, remove debris, apply fungicide if spreading."),
    ("tomato", "curl", "Virus spread by whiteflies. Small, upward-curled, yellow leaves and stunted plants.",
     "No cure. Remove infected plants, control whiteflies (nets, yellow sticky traps), use resistant varieties."),
    ("tomato", "mosaic", "Virus (ToMV). Mottled light/dark green leaves, distortion; spreads by touch and tools.",
     "No cure. Remove infected plants, wash hands and disinfect tools, use resistant seed."),
]

_HEALTHY = (
    "No visible sign of disease on this leaf.",
    "Keep monitoring regularly, water at the base of plants, and keep good airflow and field hygiene.",
)
_DEFAULT = (
    "Disease detected by the model.",
    "Contact your local agriculture extension officer to confirm and choose a treatment.",
)


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def get_info(crop: str, disease: str) -> tuple[str, str]:
    c, d = _norm(crop), _norm(disease)
    if d == "healthy":
        return _HEALTHY
    for crop_kw, dis_kw, about, action in _DB:
        if crop_kw in c and dis_kw in d:
            return about, action
    return _DEFAULT
