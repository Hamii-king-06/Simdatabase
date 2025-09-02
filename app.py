from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# 🔑 Cookies & Headers (jo tu ne diye the)
cookies = {
    'PHPSESSID': '1e6ac5a070e31027683802597b638b31',
    '_ga': 'GA1.1.1085686139.1756787588',
    '_ga_P7QWXSJ0G3': 'GS2.1.s1756787588$o1$g1$t1756787939$j26$l0$h0',
    '_ga_X1733EFCHC': 'GS2.1.s1756787588$o1$g1$t1756787939$j26$l0$h0',
    '_ga_Q1F9FGR2HJ': 'GS2.1.s1756787589$o1$g1$t1756787939$j26$l0$h0',
}

headers = {
    'authority': 'allnetworkdata.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,ur-PK;q=0.8,ur;q=0.7',
    'referer': 'https://allnetworkdata.com/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
}


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    error = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if not query.isdigit() or len(query) < 10:
            error = "❌ Invalid number format"
        else:
            params = {"number": query}
            try:
                response = requests.get(
                    "https://allnetworkdata.com/",
                    params=params,
                    cookies=cookies,
                    headers=headers,
                    timeout=15
                )
                data = response.json()

                for key, value in data.items():
                    if isinstance(value, list):
                        value = ", ".join(value)
                    results.append((key, value))

            except Exception as e:
                error = f"⚠️ Error: {e}"

    return render_template("index.html", results=results, error=error)


if __name__ == "__main__":
    app.run(debug=True)