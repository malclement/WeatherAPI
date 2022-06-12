import pymongo as pymongo
from fastapi import FastAPI, Body, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from models import UserSchema, UserLoginSchema
from urllib.parse import unquote
import requests
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer

base_url = "https://api.openweathermap.org/data/2.5/weather?"

uri = 'mongodb+srv://User:weakpass@kompozite.jrm0d0y.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(uri)
db = client.Users
app = FastAPI()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Weather API."}


@app.post("/user/signup", tags=["user"], summary="Create new user")
async def create_user(user: UserSchema = Body(...)):
    valid = await check_signup(user)
    if valid:
        user = jsonable_encoder(user)
        db["Users"].insert_one(user)
        return signJWT(user['email'])
    else:
        raise HTTPException(status_code=500, detail="Invalid User")


@app.post("/user/login", tags=["user"], summary="Log with existing user info")
async def user_login(user: UserLoginSchema = Body(...)):
    valid = await check_user(user)
    if valid:
        return signJWT(user.email)
    raise HTTPException(status_code=500, detail="Wrong Login")


async def check_user(data: UserLoginSchema):
    for results in db.Users.find({"email": data.email}):
        if results['password'] == data.password:
            return True
        else:
            return False


async def check_signup(data: UserSchema):
    for results in db.Users.find({"email": data.email}):
        if results['email'] != "":
            return False
    return True


# Return the current weather at a certain location
@app.get("/weather/{location}", dependencies=[Depends(JWTBearer())], tags=["weather"], summary="Take location and "
                                                                                               "retrieve weather")
async def get_weather(location: str):
    location = unquote(location)
    output = []
    complete_url = base_url + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + location
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]

        current_temperature = y["temp"]
        current_temperature -= 273
        current_temperature = round(current_temperature, 1)
        z = x["weather"]

        weather_description = z[0]["description"]

        output.append(" Temperature = " +
                      str(current_temperature) +
                      "\n description = " +
                      str(weather_description))
        return output
    else:
        raise HTTPException(status_code=404, detail='Location Not Found')
