from fastapi import FastAPI
echo "# petra_grasic_Abysalto_academy" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/pgrasic/petra_grasic_Abysalto_academy.git
git push -u origin main
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
