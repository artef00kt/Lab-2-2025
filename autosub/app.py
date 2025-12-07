from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class TranscribeRequest(BaseModel):
    input_file: str
    output_dir: str = "/files"
    model: str = "base"

@app.post("/transcribe")
async def transcribe(request: TranscribeRequest):
    input_file = request.input_file
    output_dir = request.output_dir
    model = request.model
    
    if not os.path.exists(input_file):
        raise HTTPException(status_code=404, detail=f"File {input_file} not found")

    logger.info(f"Starting transcription for {input_file} using model {model}")

    try:
        # Construct command
        # auto_subtitle /files/audio.wav --output_srt --output_dir /files --model base
        command = [
            "auto_subtitle", 
            input_file, 
            "--output_srt", "True", 
            "--output_dir", output_dir, 
            "--model", model
        ]
        
        # Run process
        process = subprocess.run(
            command, 
            capture_output=True, 
            text=True
        )
        
        if process.returncode != 0:
            logger.error(f"Transcription failed: {process.stderr}")
            return {
                "status": "error",
                "message": "Transcription failed",
                "stdout": process.stdout,
                "stderr": process.stderr
            }
            
        logger.info("Transcription successful")
        return {
            "status": "success",
            "message": "Transcription successful",
            "stdout": process.stdout,
            "stderr": process.stderr
        }
        
    except Exception as e:
        logger.error(f"Exception during transcription: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
