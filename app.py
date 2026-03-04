
import math
import io
from flask import Flask, request, send_file, render_template_string

app = Flask(__name__)

def digit_sum(n):
    return sum(int(d) for d in str(n) if d.isdigit())

def extract_structure(date):
    year, month, day = date.split("-")
    total_sum = digit_sum(date.replace("-", ""))
    cycle = (total_sum % 5) + 8
    day_sum = digit_sum(day)
    month_sum = digit_sum(month)
    year_sum = digit_sum(year)
    
    return {
        "total": total_sum,
        "cycle": cycle,
        "day": day_sum,
        "month": month_sum,
        "year": year_sum
    }

def generate_enhanced_svg(date1, date2):
    s1 = extract_structure(date1)
    s2 = extract_structure(date2)
    
    width = 800
    height = 800
    center_x = width / 2
    center_y = height / 2
    
    bg_color = "#002366"
    gold = "#FFD700"
    white = "#FFFFFF"
    soft_gold = "#F7D774"
    
    elements = []
    elements.append(f'<rect width="{width}" height="{height}" fill="{bg_color}"/>')
    
    outer_radius = 350
    elements.append(
        f'<circle cx="{center_x}" cy="{center_y}" r="{outer_radius}" '
        f'stroke="{gold}" stroke-width="2" fill="none" opacity="0.8"/>'
    )
    
    base_radius_1 = 200 + s1["day"] * 5
    for i in range(s1["cycle"]):
        angle = (2 * math.pi / s1["cycle"]) * i
        x_inner = center_x + 50 * math.cos(angle)
        y_inner = center_y + 50 * math.sin(angle)
        x_outer = center_x + base_radius_1 * math.cos(angle)
        y_outer = center_y + base_radius_1 * math.sin(angle)
        
        elements.append(
            f'<line x1="{x_inner}" y1="{y_inner}" x2="{x_outer}" y2="{y_outer}" '
            f'stroke="{gold}" stroke-width="2" opacity="0.9"/>'
        )
        elements.append(
            f'<circle cx="{x_outer}" cy="{y_outer}" r="4" fill="{white}" opacity="0.8"/>'
        )
    
    offset_angle = (s2["month"] / 12) * 2 * math.pi
    base_radius_2 = 200 + s2["day"] * 5
    
    for i in range(s2["cycle"]):
        angle = (2 * math.pi / s2["cycle"]) * i + offset_angle
        x_inner = center_x + 50 * math.cos(angle)
        y_inner = center_y + 50 * math.sin(angle)
        x_outer = center_x + base_radius_2 * math.cos(angle)
        y_outer = center_y + base_radius_2 * math.sin(angle)
        
        elements.append(
            f'<line x1="{x_inner}" y1="{y_inner}" x2="{x_outer}" y2="{y_outer}" '
            f'stroke="{soft_gold}" stroke-width="2" opacity="0.8"/>'
        )
        elements.append(
            f'<circle cx="{x_outer}" cy="{y_outer}" r="4" fill="{white}" opacity="0.7"/>'
        )
    
    combined_cycle = s1["cycle"] + s2["cycle"]
    ring_count = min(combined_cycle // 3, 5)
    
    for i in range(ring_count):
        ring_radius = 100 + (i * 40)
        elements.append(
            f'<circle cx="{center_x}" cy="{center_y}" r="{ring_radius}" '
            f'stroke="{white}" stroke-width="1" fill="none" opacity="{0.3 - i*0.05}"/>'
        )
    
    vesica_radius = 60
    vesica_offset = 30
    
    elements.append(
        f'<circle cx="{center_x - vesica_offset}" cy="{center_y}" r="{vesica_radius}" '
        f'stroke="{gold}" stroke-width="2" fill="none" opacity="0.9"/>'
    )
    elements.append(
        f'<circle cx="{center_x + vesica_offset}" cy="{center_y}" r="{vesica_radius}" '
        f'stroke="{gold}" stroke-width="2" fill="none" opacity="0.9"/>'
    )
    
    star_points = s1["total"] % 8 + 5
    star_radius_outer = 150
    star_radius_inner = 75
    
    star_path = []
    for i in range(star_points * 2):
        angle = (math.pi / star_points) * i
        if i % 2 == 0:
            radius = star_radius_outer
        else:
            radius = star_radius_inner
        
        x = center_x + radius * math.cos(angle - math.pi/2)
        y = center_y + radius * math.sin(angle - math.pi/2)
        
        if i == 0:
            star_path.append(f"M {x} {y}")
        else:
            star_path.append(f"L {x} {y}")
    
    star_path.append("Z")
    
    elements.append(
        f'<path d="{" ".join(star_path)}" '
        f'stroke="{white}" stroke-width="1.5" fill="none" opacity="0.4"/>'
    )
    
    elements.append(
        f'<circle cx="{center_x}" cy="{center_y}" r="8" fill="{white}" opacity="1"/>'
    )
    elements.append(
        f'<circle cx="{center_x}" cy="{center_y}" r="12" '
        f'stroke="{gold}" stroke-width="2" fill="none" opacity="0.8"/>'
    )
    
    dot_count = (s1["year"] + s2["year"]) % 20 + 30
    for i in range(dot_count):
        angle = (2 * math.pi / dot_count) * i
        dot_x = center_x + outer_radius * math.cos(angle)
        dot_y = center_y + outer_radius * math.sin(angle)
        
        elements.append(
            f'<circle cx="{dot_x}" cy="{dot_y}" r="2" fill="{white}" opacity="0.6"/>'
        )
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <filter id="glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    <g filter="url(#glow)">
        {''.join(elements)}
    </g>
</svg>'''
    
    return svg

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Core Axis - Sacred Love Glyph Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #002366 0%, #001a4d 100%);
            color: #fff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            max-width: 500px;
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
        }
        h1 {
            color: #FFD700;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2rem;
            letter-spacing: 2px;
        }
        .subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 30px;
            font-size: 0.9rem;
        }
        .form-group { margin-bottom: 20px; }
        label {
            display: block;
            color: #FFD700;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input[type="date"] {
            width: 100%;
            padding: 12px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-radius: 8px;
            color: #fff;
            font-size: 1rem;
        }
        input[type="date"]:focus {
            outline: none;
            border-color: #FFD700;
            background: rgba(255, 255, 255, 0.15);
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #FFD700, #e6c200);
            color: #002366;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4);
        }
        .info {
            text-align: center;
            margin-top: 20px;
            font-size: 0.85rem;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CORE AXIS</h1>
        <p class="subtitle">Sacred Love Glyph Generator</p>
        <form action="/download" method="GET">
            <div class="form-group">
                <label for="date1">Your Birthdate</label>
                <input type="date" id="date1" name="date1" required>
            </div>
            <div class="form-group">
                <label for="date2">Partner Birthdate</label>
                <input type="date" id="date2" name="date2" required>
            </div>
            <button type="submit">Generate Sacred Glyph</button>
        </form>
        <p class="info">Your unique symbol will be generated based on your combined cosmic moments.</p>
    </div>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/download")
def download():
    date1 = request.args.get("date1")
    date2 = request.args.get("date2")
    
    if not date1 or not date2:
        return "Both dates required", 400
    
    svg = generate_enhanced_svg(date1, date2)
    
    return send_file(
        io.BytesIO(svg.encode("utf-8")),
        mimetype="image/svg+xml",
        as_attachment=True,
        download_name=f"coreaxis_glyph_{date1}_{date2}.svg"
    )

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
