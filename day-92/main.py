from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Necesario para usar flash messages

# Paleta de colores
colors = [
    ["#FF5733", "#33FF57", "#3357FF", "#FF33FF", "#33FFFF", "#FFD700"],
    ["#800000", "#808000", "#008000", "#008080", "#000080", "#4B0082"],
    ["#DC143C", "#FF8C00", "#FFFF00", "#7FFF00", "#00FA9A", "#4682B4"],
    ["#D2691E", "#C71585", "#9400D3", "#00CED1", "#1E90FF", "#FF4500"],
    ["#A52A2A", "#DEB887", "#5F9EA0", "#7FFF00", "#DDA0DD", "#FF69B4"],
    ["#CD5C5C", "#F4A460", "#2E8B57", "#6A5ACD", "#8A2BE2", "#20B2AA"]
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_color = request.form.get("color")
        flash(f"Color choose: {selected_color}", "info")
    return render_template("grid.html", colors=colors)

if __name__ == "__main__":
    app.run(debug=True)
