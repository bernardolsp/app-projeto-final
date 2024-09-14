from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn
import worker


# Load environment variables

app = FastAPI(
    title="S3 Upload API",
    description="Async API for S3 Upload",
    version="1.0.2"
)

# Get the S3 bucket name from environment variable


class Item(BaseModel):
    name: str
    content: str

@app.get("/")
async def read_root():
    """
    Root endpoint that returns a list of objects in the S3 bucket.
    """
    objects = await worker.list_s3_objects()
    return {"message": "Welcome to the S3 Upload API!", "objects": objects}




@app.post("/upload")
async def upload_to_s3(item: Item, background_tasks: BackgroundTasks):
    """
    Queue the S3 upload as a background task and return immediately.
    """
    background_tasks.add_task(worker.upload_to_s3_background, item.name, item.content)
    return {"message": f"Upload of {item.name} queued successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)