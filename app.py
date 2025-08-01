    from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
import io
import os

# Create an instance of the FastAPI application
app = FastAPI()

# Check if the port environment variable is set, otherwise default to 8000
port = int(os.environ.get("PORT", 8000))

# Test endpoint
@app.get("/test")
async def root():
    return {"message": "This is a test endpoint"}

# Endpoint to remove the background of an uploaded image
@app.post("/remove_background")
async def remove_background_endpoint(image_file: UploadFile):
    # Read the image file content
    image_content = await image_file.read()

    # Open the image using Pillow
    input_image = Image.open(io.BytesIO(image_content))

    # Remove the background
    output_image = remove(input_image)

    # Save the processed image to a buffer
    output_buffer = io.BytesIO()
    output_image.save(output_buffer, "PNG")
    output_buffer.seek(0)

    # Return the processed image as a downloadable file
    return FileResponse(output_buffer, media_type="image/png", filename="output.png")

# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
