# youtube-dl Web Interface -- Threaded

from flask import Flask, render_template, redirect, request, url_for
import threading
import json
import os

app = Flask(__name__)
file = json.loads(open("web.json").read())

class dwnl(threading.Thread):
	def __init__(self, dwnl_url, dwnl_type):
		threading.Thread.__init__(self)

		self.dwnl_url = dwnl_url
		self.dwnl_type = dwnl_type
	def run(self):
    location = "" # Must set this!
  
		if "youtube" in self.dwnl_url:
			if "playlist" in self.dwnl_url:
				os.system("youtube-dl -i --yes-playlist -o '{}/%(title)s.%(ext)s' -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' {}".format(location, self.dwnl_url))
			else:
				if self.dwnl_type == "mp4":
					os.system("youtube-dl -o '{}/%(title)s.%(ext)s' -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' {}".format(location, self.dwnl_url))
				elif self.dwnl_type == "mp3":
					os.system("youtube-dl -o '{}/%(title)s_audio.%(ext)s' --extract-audio --audio-format {}".format(location, self.dwnl_url))
		else:
			os.system("youtube-dl {}".format(self.dwnl_url))

def write_json(link):
	global file

	with open("web.json", "w") as j:
		f = file["links"]
		f.append(link)
		j.write(json.dumps({"links":f}))

	file = json.loads(open("web.json").read())

@app.route("/", methods=["GET"])
def index():
	return render_template("primary.html", links_dwnl=file["links"])

@app.route("/new", methods=["POST"])
def new():
	if request.form["new_url"]:
		write_json(request.form["new_url"])
		dwnl = dwnl(request.form["new_url"]).start()

	return redirect(url_for("index"))

@app.route("/clear", methods=["GET", "POST"])
def clear():
	global file

	with open("web.json", "w") as j:
		j.write(json.dumps({"links":[]}))

	file = json.loads(open("web.json").read())

	return redirect(url_for("index"))

app.run("0.0.0.0", 8008, debug=False)
