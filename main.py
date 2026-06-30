from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import shutil
import os


app=FastAPI()


class Request(BaseModel):

    code:str

@app.get("/")

def home():

    return {

        "status":"Compiler API Running"

    }

@app.post("/run")

def run(data:Request):

    folder=tempfile.mkdtemp()

    try:

        cpp=f"{folder}/main.cpp"

        with open(cpp,"w") as f:

            f.write(data.code)


        compile_result=subprocess.run(

            [

            "g++",

            cpp,

            "-o",

            f"{folder}/app"

            ],

            capture_output=True,

            text=True

        )


        if compile_result.returncode!=0:

            return {

                "output":

                compile_result.stderr

            }


        result=subprocess.run(

            [

            f"{folder}/app"

            ],

            capture_output=True,

            text=True,

            timeout=5

        )


        return {

            "output":

            result.stdout

        }


    except subprocess.TimeoutExpired:

        return {

            "output":

            "Execution Timeout"

        }


    finally:

        shutil.rmtree(
            folder,
            ignore_errors=True
        )