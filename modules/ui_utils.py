"""Icon and styling utilities for OctoGreen"""

# Icon mappings using emojis
ICONS = {
    "download": "⬇️",
    "upload": "📤",
    "chart": "📊",
    "data": "📈",
    "settings": "⚙️",
    "check": "✅",
    "error": "❌",
    "info": "ℹ️",
    "warning": "⚠️",
    "arrow": "→",
    "click": "👆",
    "energy": "⚡",
    "carbon": "🌍",
    "home": "🏠",
    "database": "🗄️",
    "world": "🌐",
    "bank": "🏦",
    "chart_line": "📉",
    "filter": "🔍",
    "save": "💾",
    "report": "📄",
    "success": "🎉",
}

# Minimal CSS
CUSTOM_CSS = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500&display=swap');

h1, h2, h3, h4, h5, h6 {
    font-family: "Poppins", sans-serif !important;
    font-weight: 700 !important;
}

.stButton > button {
    background-color: #10b981 !important;
    border-radius: 6px !important;
}

.stButton > button:hover {
    background-color: #059669 !important;
}
</style>
'''

def get_icon(name):
    """Get Font Awesome icon by name"""
    return ICONS.get(name, "•")
