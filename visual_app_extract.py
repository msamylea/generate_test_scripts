import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import pandas as pd
import glob

Image.MAX_IMAGE_PIXELS = None
load_dotenv()

genai.configure(api_key=os.environ.get("api_key"))

model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

filepath = "./docs"

# Get all JPG files in the directory
jpg_files = glob.glob(os.path.join(filepath, "*.jpg"))

for jpg_file in jpg_files:
    image = Image.open(jpg_file)
    
    # Calculate new size preserving aspect ratio
 
    
    # Save the image
    image.save("resized_image.jpg", "JPEG")
    
    response = model.generate_content(
        [
            """Read the text contained within this image. Using that exact text create a test script based on that process flow. 
            Use the exact text provided in the document, excluding the legend text. 
            You should have a column for Step #, a column for Action, and a column for Expected Result. 
            If there are branching paths follow one path at a time. Do not follow the same loop repeatedly. Only return to the same element once before moving forward.
            If it loops multiple times in the same path, assume that the loop condition is fulfilled and move forward. 
            Your branches should follow one path to its end before beginning the next path.
            Each different colored box is a different step.
            It is very important you do not skip any steps. It is also important you do not duplicate any steps. For example, if the path is "Transfer to Agent", and the next step is "Transfer to Agent", do not duplicate the step, or if the last Action was "Success", the next action should not also be "Success".
            After you reach an end (for example "Transfer to Agent", if there were any previous steps that were not followed, return and start the next path.)""", 
            image
        ], 
        request_options={"timeout": 1000}
    )    
    print(response)
    
    text = response.candidates[0].content.parts[0].text

    # Split the text into lines
    lines = text.split('\n')

    # For each line, split it into columns by the pipe character
    data = [line.split('|') for line in lines]
    df = pd.DataFrame(data)  # Create a DataFrame for the entire response

    # Generate unique sheet name
    sheet_name = os.path.splitext(os.path.basename(jpg_file))[0] 

    if os.path.exists('output.xlsx') and os.path.getsize('output.xlsx') > 0:
        # If the file exists and is not empty, append to it
        with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    else:
        # If the file doesn't exist or is empty, create it
        df.to_excel('output.xlsx', sheet_name=sheet_name, index=False)