from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import shutil
import os


app = FastAPI()


class Request(BaseModel):
    code: str
    user_input: str = ""


@app.get("/")
def home():

    return {

        "status": "Compiler API Running"

    }


@app.post("/run")
def run(data: Request):

    folder = tempfile.mkdtemp()

    cpp = os.path.join(
        folder,
        "main.cpp"
    )

    exe = os.path.join(
        folder,
        "app"
    )

    try:

        with open(
            cpp,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                data.code
            )

        compile_result = subprocess.run(

            [

                "g++",

                cpp,

                "-O2",

                "-std=c++17",

                "-o",

                exe

            ],

            capture_output=True,

            text=True,

            timeout=15

        )

        if compile_result.returncode != 0:

            return {

                "output":

                compile_result.stderr[:5000]

            }

        run_result = subprocess.run(

            [exe],

            input=data.user_input,

            capture_output=True,

            text=True,

            timeout=5

        )

        output = run_result.stdout

        if len(output) > 50000:

            output = output[:50000]

        return {

            "output":

            output

        }

    except subprocess.TimeoutExpired:

        return {

            "output":

            "Execution Timeout"

        }

    except Exception as e:

        return {

            "output":

            str(e)

        }

    finally:

        shutil.rmtree(
            folder,
            ignore_errors=True
        )