from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

PROFILES_FILE = "profiles.json"
ACTIVE_FILE = "active_profile.txt"

DEFAULT_INTERVAL = 0.001
DEFAULT_ACCEL_X = 0.5
DEFAULT_ACCEL_Y = 0.5

def load_profiles():
    if not os.path.exists(PROFILES_FILE):
        return {}
    with open(PROFILES_FILE) as f:
        return json.load(f)

def save_profiles(profiles):
    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=4)

def get_active_profile():
    if os.path.exists(ACTIVE_FILE):
        with open(ACTIVE_FILE) as f:
            return f.read().strip()
    return None

@app.route("/")
def root():
    return redirect("/profiles")

@app.route("/profiles")
def profiles_page_1():
    profiles = load_profiles()
    active = get_active_profile()
    page_profiles = {name: data for name, data in profiles.items() if data.get("page", 1) == 1}
    return render_template("index.html", profiles=page_profiles, active=active, current_page=1)

@app.route("/profiles2")
def profiles_page_2():
    profiles = load_profiles()
    active = get_active_profile()
    page_profiles = {name: data for name, data in profiles.items() if data.get("page", 1) == 2}
    return render_template("index.html", profiles=page_profiles, active=active, current_page=2)

@app.route("/create", methods=["POST"])
def create_profile():
    profile_name = request.form["new_profile"]
    page = int(request.form.get("page", 1))
    profiles = load_profiles()

    if profile_name in profiles:
        return redirect(url_for("profiles_page_1" if page == 1 else "profiles_page_2"))

    profiles[profile_name] = {
        "x": 0,
        "y": 0,
        "interval": DEFAULT_INTERVAL,
        "accel_x": DEFAULT_ACCEL_X,
        "accel_y": DEFAULT_ACCEL_Y,
        "page": page
    }
    save_profiles(profiles)
    return redirect(url_for("profiles_page_1" if page == 1 else "profiles_page_2"))

@app.route("/select", methods=["POST"])
def select():
    selected_profile = request.form["profile"]
    with open(ACTIVE_FILE, "w") as f:
        f.write(selected_profile)
    profiles = load_profiles()
    page = profiles[selected_profile].get("page", 1)
    return redirect(url_for("profiles_page_1" if page == 1 else "profiles_page_2"))

@app.route("/update", methods=["POST"])
def update():
    profile_name = request.form["profile"]
    x = float(request.form["x"])
    y = float(request.form["y"])
    accel_x = float(request.form.get("accel_x", DEFAULT_ACCEL_X))
    accel_y = float(request.form.get("accel_y", DEFAULT_ACCEL_Y))

    profiles = load_profiles()
    if profile_name in profiles:
        profiles[profile_name]["x"] = x
        profiles[profile_name]["y"] = y
        profiles[profile_name]["interval"] = DEFAULT_INTERVAL
        profiles[profile_name]["accel_x"] = accel_x
        profiles[profile_name]["accel_y"] = accel_y
        page = profiles[profile_name].get("page", 1)
        save_profiles(profiles)
        return redirect(url_for("profiles_page_1" if page == 1 else "profiles_page_2"))
    return redirect("/profiles")

@app.route("/delete", methods=["POST"])
def delete():
    profile_name = request.form["profile"]
    profiles = load_profiles()
    page = profiles.get(profile_name, {}).get("page", 1)
    if profile_name in profiles:
        del profiles[profile_name]
        save_profiles(profiles)
    return redirect(url_for("profiles_page_1" if page == 1 else "profiles_page_2"))

if __name__ == "__main__":
    app.run(debug=True)
