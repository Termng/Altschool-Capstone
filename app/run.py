import uvicorn 

if __name__ == "__main__":
    uvicorn.run(
        reload=True,
        app = "main:app"
    )


