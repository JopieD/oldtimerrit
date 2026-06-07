# 🚗 ODG Oldtimerritten

Web-app voor navigatie tijdens oldtimerritten.

De applicatie combineert GPX-routes, PDF-roadbooks en automatisch geëxtraheerde navigatiesymbolen tot een gebruiksvriendelijke navigatie-app die draait op iPhone, Android en desktop via GitHub Pages.

---

## Functionaliteit

### 📍 GPS-navigatie

- Actuele GPS-positie
- Afstand tot actief waypoint
- Automatische waypoint-detectie
- Handmatige "Next WPT" knop
- GPS-nauwkeurigheid zichtbaar

### 🗺️ Kaartweergave

- Volledige GPX-track zichtbaar
- Waypoints zichtbaar op de kaart
- Actuele positie zichtbaar
- Werkt op iPhone, Android en desktop

### 📖 Roadbook

- Automatische import vanuit PDF
- Automatische symboolextractie
- Koppeling van symbolen aan waypoints
- Ondersteuning voor Rally Navigator roadbooks

### 📱 Mobiel gebruik

- Geschikt voor Safari op iPhone
- Toe te voegen aan beginscherm
- Eigen ODG-appicoon
- Eigen ODG-startpagina met rittenoverzicht

---

## Projectstructuur

text oldtimerrit/ 
├── input/ 
│   ├── ODG2026-1.gpx 
│   ├── ODG2026-1.pdf 
│   ├── ODG2026-2.gpx 
│   └── ODG2026-2.pdf 
│ 
├── ritten/ 
│   ├── ODG2026-1/ 
│   │   ├── index.html 
│   │   ├── route.json 
│   │   ├── track.json 
│   │   ├── roadbook.json 
│   │   ├── css/ 
│   │   ├── js/ 
│   │   └── symbols/ 
│   │ 
│   └── ODG2026-2/ 
│ 
├── templates/ 
│   
├── index.html 
│   ├── css/ 
│   │   └── style.css 
│   └── js/ 
│       └── app.js 
│ 
├── tools/ 
│   ├── gpx_to_json.py 
│   ├── roadbook_import.py 
│   ├── extract_symbols.py 
│   └── publish_rit.py 
│ 
├── index.html 
├── header.png 
├── apple-touch-icon.png 
├── requirements.txt 
└── README.md 

---

## Nieuwe rit publiceren

Plaats een GPX-bestand en PDF-roadbook in:

text input/ 

Voorbeeld:

text input/ 
├── ODG2027-1.gpx 
└── ODG2027-1.pdf 

Publiceer vervolgens:

bash python3 tools/publish_rit.py ODG2027-1 

of via de VS Code Task:

text ⌘⇧B 

Resultaat:

text ritten/ 
└── ODG2027-1/     
├── index.html     
├── route.json     
├── track.json     
├── roadbook.json     
├── css/     
├── js/     
└── symbols/ 

---

## VS Code

Voor het publiceren van een rit is een VS Code Task beschikbaar.

Gebruik:

text ⌘⇧B 

Voer vervolgens de ritnaam in:

text ODG2026-1 

De complete rit wordt automatisch opgebouwd.

---

## GitHub Pages

De applicatie wordt gepubliceerd via GitHub Pages.

Startpagina:

text https://jopied.github.io/oldtimerrit/ 

Beschikbare ritten kunnen vanaf deze pagina direct worden geopend.

---

## Installatie

### Vereisten

- Python 3.x
- Git
- Visual Studio Code

### Python modules

Installeer de vereiste modules:

bash pip install -r requirements.txt 

Voorbeeld requirements.txt:

text pdfplumber pymupdf Pillow 

---

## Ontwikkelomgeving

Ontwikkeld en getest op:

- macOS
- Visual Studio Code
- GitHub
- GitHub Pages
- Safari (iPhone)
- Chrome

---

## Workflow

Nieuwe rit maken:

1. GPX-bestand plaatsen in input
2. PDF-roadbook plaatsen in input
3. VS Code Task uitvoeren (⌘⇧B)
4. Ritnaam invoeren
5. Controle uitvoeren
6. Git commit en push

Publicatie gebeurt automatisch via GitHub Pages.

---

## Roadmap

### v1.1

#### 🎯 Centreer-knop

Met één druk op de knop centreert de kaart op de actuele GPS-positie.

#### ⚠️ Afstand tot route

Toont de afstand tussen de huidige positie en de dichtstbijzijnde positie op de GPX-track.

Voorbeeld:

text Afstand tot route: 35 m 

#### 🚨 Van-route-waarschuwing

Waarschuwing wanneer de gebruiker een ingestelde afstand van de route afwijkt.

Voorbeeld:

text ⚠️ U bent van de route geraakt 

#### 📍 Verbeterde kaartnavigatie

Optimalisaties voor gebruik tijdens het rijden, gebaseerd op praktijkervaring tijdens ritten.

---

## Huidige status

### v1.0

Gereed:

- Multi-rit architectuur
- Automatische GPX-import
- Automatische PDF-import
- Automatische symboolextractie
- Volledige GPX-trackweergave
- GPS-navigatie
- Automatische waypoint-detectie
- VS Code build task
- GitHub Pages hosting
- ODG branding
- iPhone web-app
- Rittenoverzicht

---

## Auteur

ODG Oldtimerritten Project

Ontwikkeld voor gebruik tijdens klassieke kaartleesritten en oldtimerritte