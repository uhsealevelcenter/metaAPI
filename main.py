from fastapi import FastAPI
import urllib.request
import geopandas as gpd
import json

metaURL = "https://uhslc.soest.hawaii.edu/data/meta.geojson"

def load_meta():
    meta = gpd.read_file(metaURL)
    req = urllib.request.urlopen(metaURL)
    raw = json.loads(req.read().decode(req.info().get_param('charset') or 'utf-8'))
    return meta,raw

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/raw")
async def show_raw():
    df,foo = load_meta()
    return foo

@app.get("/select2")
async def create_sel2():
    df = load_meta()
    results = []

    for index, row in df.iterrows():
        if row['fd_span']['oldest'] != None:
            d = {}
            # s = '{{"id":"{}","text":"{} {}, {}"}}'.format(str(row['uhslc_id']).zfill(3),str(row['uhslc_id']).zfill(3),row['name'],row['country'])
            d = {"id": str(row['uhslc_id']).zfill(3),
                 "text": str(row['uhslc_id']).zfill(3) + ' ' + row['name'] + ' ' + row['country']}
            results.append(d)

    results = {
        "results": results,
        "pagination": {
            "more": True
        }
    }

    return results

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
