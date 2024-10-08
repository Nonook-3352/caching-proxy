from flask import Flask, jsonify
import requests
import os
import json

app = Flask(__name__)


@app.route("/<route>")
def origin(route):
    result = requests.get(f"https://dummyjson.com/{route}")
    data = None
    from_cache = None
    if not os.path.exists(f"{os.getcwd()}/cache/{route}.json"):
        to_write = json.dumps(result.json(), indent=2)
        with open(f"{os.getcwd()}/cache/{route}.json", "w+") as file:
            file.write(to_write)
            file.close()
        data = result.json()
        from_cache = "MISS"
    else:
        with open(f"{os.getcwd()}/cache/{route}.json", "r") as file:
            cached_data = json.load(file)
            file.close()
        from_cache = "HIT"
        data = cached_data
    
    resp = jsonify(data)
    resp.headers["X-Cache"] = from_cache
    return resp


app.run(port=3000, debug=True)