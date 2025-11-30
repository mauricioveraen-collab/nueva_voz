from flask import Flask, request, send_file, render_template
import tempfile
import os
from pydub import AudioSegment

app = Flask(__name__)

def convertir_voz(source_path, target_path, out_path):
    # Carga el audio principal
    audio = AudioSegment.from_file(source_path)

    # Exporta a WAV
    audio.export(out_path, format="wav")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    source = request.files.get("source")
    target = request.files.get("target")

    if not source or not target:
        return "FALTAN ARCHIVOS", 400

    tmp_dir = tempfile.mkdtemp()
    source_path = os.path.join(tmp_dir, "SOURCE.WAV")
    target_path = os.path.join(tmp_dir, "TARGET.WAV")
    out_path = os.path.join(tmp_dir, "OUTPUT.WAV")

    source.save(source_path)
    target.save(target_path)

    # Llama a la conversión
    convertir_voz(source_path, target_path, out_path)

    return send_file(out_path, mimetype="audio/wav", as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)
