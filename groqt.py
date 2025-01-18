from groq import Groq
import base64

def sigma(image_path = "snapshot.jpg"):
    """
    call to groq api to see what is in the photo

    argument: takes in the location of the frame we are analyzing
    """
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string
    base64_image = encode_image(image_path)

    client = Groq(api_key = "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")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image, described in two sentences?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="llama-3.2-11b-vision-preview",
    )

    print(chat_completion.choices[0].message.content)

sigma()