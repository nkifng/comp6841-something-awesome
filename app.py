from flask import Flask, render_template, url_for, request, send_from_directory, flash, redirect
from forms import EncryptionForm, DecryptionForm, StegEncForm, StegDecForm, ChaosEncForm
from backend.aes_utils import aes_encrypt, aes_decrypt
from backend.triple_des_utils import triple_des_encrypt, triple_des_decrypt
from backend.stego_utils import stego_encode, stego_decode
from backend.chaos_map_utils import chaos_map_encode, chaos_map_decode
from backend.rc4_utils import rc4_encrypt, rc4_decrypt
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path

import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "614d6822a2641dee2cd223a1c5e34c7f"
app.config['UPLOAD_FOLDER']='uploads'

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# AES
@app.route("/aes")
def aes():
    form_enc = EncryptionForm()
    form_dec = DecryptionForm()
    return render_template(
        "standard.html",
        form_enc=form_enc,
        form_dec=form_dec,
        title="AES",
        encrypt_action="/aes/encrypt",
        decrypt_action="/aes/decrypt")

@app.route("/aes/encrypt", methods=["POST"])
def aes_encryption():
    form_enc = EncryptionForm()
    if request.method == "POST" and form_enc.validate_on_submit():
        key = request.form["key"]
        filename = secure_filename(form_enc.file.data.filename)
        form_enc.file.data.save("uploads/" + filename)
        name = aes_encrypt("uploads/" + filename, key)
        return redirect(url_for("aes_encrypted", name=name))

@app.route("/aes/encrypted/<path:name>")
def aes_encrypted(name):
    form_dec = DecryptionForm()
    return render_template(
        "encrypted.html",
        name=name,
        form_dec=form_dec,
        title="AES",
        decrypt_action="/aes/decrypt")

@app.route("/aes/decrypt", methods=["POST"])
def aes_decryption():
    form_dec = DecryptionForm()
    if request.method == "POST" and form_dec.validate_on_submit():
        key = request.form["decrypt_key"] 
        filename = secure_filename(form_dec.file.data.filename)
        form_dec.file.data.save("uploads/" + filename)
        initial_name = "uploads/" + filename
        name = aes_decrypt(initial_name, key)
        if name != initial_name:
            return redirect(url_for("aes_decrypted", name=name))
        else:
            flash("Secret key is incorrect", "danger")
            return redirect(url_for("aes"))

@app.route("/aes/decrypted/<path:name>")
def aes_decrypted(name):
    form_enc = EncryptionForm()
    return render_template(
        "decrypted.html",
        name=name,
        form_enc=form_enc,
        encrypt_action="/aes/encrypt",
        title="AES")
################################################################

# Triple DES
@app.route("/triple_des")
def triple_des():
    form_enc = EncryptionForm()
    form_dec = DecryptionForm()
    return render_template(
        "standard.html",
        form_enc=form_enc,
        form_dec=form_dec,
        title="Triple DES",
        encrypt_action="/triple_des/encrypt",
        decrypt_action="/triple_des/decrypt")

@app.route("/triple_des/encrypt", methods=["POST"])
def triple_des_encryption():
    form_enc = EncryptionForm()
    if request.method == "POST" and form_enc.validate_on_submit():
        key = request.form["key"]
        filename = secure_filename(form_enc.file.data.filename)
        form_enc.file.data.save("uploads/" + filename)
        name = triple_des_encrypt("uploads/" + filename, key)
        return redirect(url_for("triple_des_encrypted", name=name))

@app.route("/triple_des/encrypted/<path:name>")
def triple_des_encrypted(name):
    form_dec = DecryptionForm()
    return render_template(
        "encrypted.html",
        name=name,
        form_dec=form_dec,
        title="Triple DES",
        decrypt_action="/triple_des/decrypt")

@app.route("/triple_des/decrypt", methods=["POST"])
def triple_des_decryption():
    form_dec = DecryptionForm()
    if request.method == "POST" and form_dec.validate_on_submit():
        key = request.form["decrypt_key"] 
        filename = secure_filename(form_dec.file.data.filename)
        form_dec.file.data.save("uploads/" + filename)
        initial_name = "uploads/" + filename
        name = triple_des_decrypt(initial_name, key)
        if name != initial_name:
            return redirect(url_for("triple_des_decrypted", name=name))
        else:
            flash("Secret key is incorrect", "danger")
            return redirect(url_for("triple_des"))

@app.route("/triple_des/decrypted/<path:name>")
def triple_des_decrypted(name):
    form_enc = EncryptionForm()
    return render_template(
        "decrypted.html",
        name=name,
        form_enc=form_enc,
        encrypt_action="/triple_des/encrypt",
        title="Triple DES")
################################################################

# Steganography
@app.route("/steganography")
def steganography():
    form_enc = StegEncForm()
    form_dec = StegDecForm()
    return render_template(
        "stego.html",
        form_enc=form_enc,
        form_dec=form_dec,
        title="Steganography")

@app.route("/steganography/encode", methods=["POST"])
def stego_encoding():
    form_enc = StegEncForm()
    if request.method == "POST" and form_enc.validate_on_submit():
        message = request.form["message"]
        filename = secure_filename(form_enc.file.data.filename)
        form_enc.file.data.save("uploads/" + filename)
        name = stego_encode("uploads/" + filename, message)
        return redirect(url_for("stego_encoded", name=name))

@app.route("/steganography/encoded/<path:name>")
def stego_encoded(name):
    form_dec = StegDecForm()
    return render_template(
        "stego_encoded.html",
        name=name,
        form_dec=form_dec,
        title="Steganography")

@app.route("/steganography/decode", methods=["POST"])
def stego_decoding():
    form_dec = StegDecForm()
    if request.method == "POST" and form_dec.validate_on_submit():
        filename = secure_filename(form_dec.file.data.filename)
        form_dec.file.data.save("uploads/" + filename)
        message = stego_decode("uploads/" + filename)
        return redirect(url_for("stego_decoded", message=message))

@app.route("/steganography/decoded/<path:message>")
def stego_decoded(message):
    form_enc = StegEncForm()
    return render_template(
        "stego_decoded.html",
        message=message,
        form_enc=form_enc,
        title="Steganography")

##################################################################
# Chaos Map
@app.route("/chaos_map")
def chaos_map():
    form_enc = EncryptionForm()
    form_dec = DecryptionForm()
    return render_template(
        "standard.html",
        form_enc=form_enc,
        form_dec=form_dec,
        title="Chaos Map (Logistic)",
        encrypt_action="/chaos_map/encode",
        decrypt_action="/chaos_map/decode")

@app.route("/chaos_map/encode", methods=["POST"])
def chaos_map_encoding():
    form_enc = EncryptionForm()
    if request.method == "POST" and form_enc.validate_on_submit():
        key = request.form["key"]
        filename = secure_filename(form_enc.file.data.filename)
        form_enc.file.data.save("uploads/" + filename)
        name = chaos_map_encode("uploads/" + filename)
        get_password(key, name)
        return redirect(url_for("chaos_map_encoded", name=name))

@app.route("/chaos_map/encoded/<path:name>")
def chaos_map_encoded(name):
    form_dec = DecryptionForm()
    return render_template(
        "encrypted.html",
        name=name,
        form_dec=form_dec,
        title="Chaos Map (Logistic)",
        decrypt_action="/chaos_map/decode")

@app.route("/chaos_map/decode", methods=["POST"])
def chaos_map_decoding():
    form_dec = DecryptionForm()
    if request.method == "POST" and form_dec.validate_on_submit():
        key = request.form["decrypt_key"] 
        filename = secure_filename(form_dec.file.data.filename)
        if check_password(key, filename):
            form_dec.file.data.save("uploads/" + filename)
            name = chaos_map_decode("uploads/" + filename)
            return redirect(url_for("chaos_map_decoded", name=name))
        else: 
            flash("Secret key is incorrect", "danger")
            return redirect(url_for("chaos_map"))

@app.route("/chaos_map/decoded/<path:name>")
def chaos_map_decoded(name):
    form_enc = EncryptionForm()
    return render_template(
        "decrypted.html",
        name=name,
        form_enc=form_enc,
        encrypt_action="/chaos_map/encode",
        title="Chaos Map (Logistic)")

################################################################

# RC4
@app.route("/rc4")
def rc4():
    form_enc = EncryptionForm()
    form_dec = DecryptionForm()
    return render_template(
        "standard.html",
        form_enc=form_enc,
        form_dec=form_dec,
        title="RC4",
        encrypt_action="/rc4/encrypt",
        decrypt_action="/rc4/decrypt")

@app.route("/rc4/encrypt", methods=["POST"])
def rc4_encryption():
    form_enc = EncryptionForm()
    if request.method == "POST" and form_enc.validate_on_submit():
        key = request.form["key"]
        filename = secure_filename(form_enc.file.data.filename)
        form_enc.file.data.save("uploads/" + filename)
        name = rc4_encrypt("uploads/" + filename, key)
        return redirect(url_for("rc4_encrypted", name=name))

@app.route("/rc4/encrypted/<path:name>")
def rc4_encrypted(name):
    form_dec = DecryptionForm()
    return render_template(
        "encrypted.html",
        name=name,
        form_dec=form_dec,
        title="RC4",
        decrypt_action="/rc4/decrypt")

@app.route("/rc4/decrypt", methods=["POST"])
def rc4_decryption():
    form_dec = DecryptionForm()
    if request.method == "POST" and form_dec.validate_on_submit():
        key = request.form["decrypt_key"] 
        filename = secure_filename(form_dec.file.data.filename)
        form_dec.file.data.save("uploads/" + filename)
        initial_name = "uploads/" + filename
        name = rc4_decrypt(initial_name, key)
        if name != initial_name:
            return redirect(url_for("rc4_decrypted", name=name))
        else:
            flash("Secret key is incorrect", "danger")
            return redirect(url_for("rc4"))

@app.route("/rc4/decrypted/<path:name>")
def rc4_decrypted(name):
    form_enc = EncryptionForm()
    return render_template(
        "decrypted.html",
        name=name,
        form_enc=form_enc,
        encrypt_action="/rc4/encrypt",
        title="RC4")
################################################################

@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=folder, filename=filename)

def get_password(key, name):
    hash = generate_password_hash(key + name, "sha256")
    folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    file = os.path.join(folder, "pw.txt")
    text_file = open(file, "a")
    text_file.write(f'{hash}\n')
    text_file.close()

def check_password(key, name):
    folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    file = os.path.join(folder, "pw.txt")
    found = False
    if Path(file).exists():
        text_file = open(file, "r+")
        content = text_file.read().splitlines()
        content_copy = content.copy()
        for hash in content_copy:
            if check_password_hash(hash, key + name):
                found = True
                content.remove(hash)
                text_file.seek(0)
                text_file.write('\n'.join(content))
                text_file.truncate()
                break
        text_file.close()
    return found

if __name__ == "__main__":
    app.run(debug=True)