import os
from dotenv import load_dotenv
import base64
import uuid
import cloudinary
import cloudinary.api
import cloudinary.uploader

class CloudinaryDBClient:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Configuration
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True
        )

    def upload_image(self, username: str, image_type: str, base64_image: str) -> str:
        """
        Uploads an image to Cloudinary.

        Args:
            username (str): The username of the uploader.
            image_type (str): The type of image (e.g., 'people', 'places').
            base64_image (str): The Base64 encoded string of the image.

        Returns:
            str: URL of the uploaded image.
        """
        if image_type not in ["people", "places"]:
            raise ValueError("Invalid image type. Must be 'people' or 'places'.")

        # Ensure the Base64 string includes the data URI scheme
        if not base64_image.startswith("data:image"):
            base64_image = f"data:image/png;base64,{base64_image}"

        # Generate a unique ID for the image
        image_id = str(uuid.uuid4())

        # Create the public ID for the image
        public_id = f"{username}_{image_type}_{image_id}"

        # Upload the image to Cloudinary
        try:
            response = cloudinary.uploader.upload(
                base64_image,
                public_id=public_id,
                overwrite=True,  # Overwrite if public_id already exists
                resource_type="image"
            )
            return response.get("url")
        except cloudinary.exceptions.Error as e:
            print(f"Error uploading image: {e}")
            return ""

    def get_all_images(self) -> list:
        """
        Retrieve all images from Cloudinary.

        Returns:
            list: List of dictionaries containing image details.
        """
        try:
            response = cloudinary.api.resources(type="upload", max_results=500)
            return response.get("resources", [])
        except cloudinary.exceptions.Error as e:
            print(f"Error retrieving all images: {e}")
            return []

    def get_images_by_type(self, username: str, image_type: str) -> list:
        """
        Retrieve images of a specific type for a specific user from Cloudinary.

        Args:
            username (str): The username associated with the images.
            image_type (str): The type of image (e.g., 'people', 'places').

        Returns:
            list: List of dictionaries containing image details.
        """
        if image_type not in ["people", "places"]:
            raise ValueError("Invalid image type. Must be 'people' or 'places'.")

        prefix = f"{username}_{image_type}_"  # Adjust based on your public_id structure

        try:
            response = cloudinary.api.resources(
                type="upload",
                prefix=prefix,
                max_results=500  # Adjust as needed
            )
            return response.get("resources", [])
        except cloudinary.exceptions.Error as e:
            print(f"Error retrieving images by type: {e}")
            return []

    def update_image(self, public_id: str, new_base64_image: str) -> str:
        """
        Updates an existing image on Cloudinary.

        Args:
            public_id (str): The public ID of the image to update.
            new_base64_image (str): The new Base64 encoded string of the image.

        Returns:
            str: URL of the updated image.
        """
        try:
            response = cloudinary.uploader.upload(
                new_base64_image,
                public_id=public_id,
                overwrite=True,
                resource_type="image"
            )
            return response.get("url")
        except cloudinary.exceptions.Error as e:
            print(f"Error updating image: {e}")
            return ""

    def delete_image(self, public_id: str) -> bool:
        """
        Deletes an image from Cloudinary.

        Args:
            public_id (str): The public ID of the image to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            response = cloudinary.uploader.destroy(public_id, resource_type="image")
            return response.get("result") == "ok"
        except cloudinary.exceptions.Error as e:
            print(f"Error deleting image: {e}")
            return False

    def get_image_details(self, public_id: str) -> dict:
        """
        Retrieves details of a specific image from Cloudinary.

        Args:
            public_id (str): The public ID of the image.

        Returns:
            dict: Dictionary containing image details.
        """
        try:
            response = cloudinary.api.resource(public_id, resource_type="image")
            return response
        except cloudinary.exceptions.Error as e:
            print(f"Error retrieving image details: {e}")
            return {}

# Usage instructions
# def main():
#     client = CloudinaryDBClient()
#     username = "john_doe"
#     image_type = "people"
#     # Example Base64 string (replace with actual Base64 image)
#     base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAIAAAB7GkOtAAANG0lEQVR4nOzXj9fXdX3Gcb5xT2+NCKdGLRUVcOmC5tAcDRORbDnTQRvHzUZTwynzR5lLbbrabDVcmkvETMWUOhJuB6d0IM1ZuDaFSNvUMH9k6sYsEIJBnJCxv+I6p3Oux+MPuN7f87nPuZ/nNfT8AR8ZkfT83u+J7g9Nui66f/aeN0b3Z199Z3R//LW3RPe/PXJCdv+Ll0X3d35mXnR/3B8ti+6/d1n298/42p7o/kVz3hzdf/jEKdH9nQu3RPePWfiP0f3XRdcB+KUlAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKDU2cPi36wLn3RedHHDB8anT/5fkro/svXveG6P5b/+u06P6Kf31/dP+gY2dH94++4JPR/ReXvyO6f9K0tdH9BY+Pi+6f9Mxno/tHfnJkdP+SEW+J7u+949bovgsAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACg1dMgVm6MP3H/YM9H9Zw74cHT/pVnzo/urrvrz6P7ytW+K7i9ZuCq6/7Ez1kX393rj30b3N7/h4uj+A1/ZEt2/88Qno/snrfvn6P5Pb1oS3f/u1K3R/aefWBPddwEAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUG1wzOiD6wYfKbo/vPzn9PdP/4Eb8a3R++6IXo/lljr4nu37Z+e3T//CVHRve/sGd0dP+CC8ZH928evzm6f+TMr0b3v/WDndH9q37vw9H9//yt70T3Xzl0RXTfBQBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBo6ftza7AtT743Oj/z5mOj+H+6/ILo/+scTovubHlkd3V9119bo/oTvfyi6v+L7Y6P7C577k+j+301cGt1/70XTovtbFi+K7n/zsJOj++ccd3l0/+Ul34ruuwAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoNHp17QPSB21ddGt0fzF0T3X/9bxwd3R/x+6dE5+955G+i+5vGZL//1w5+Irq/adnU6P7wDxdE94d+sja6P2rjN6L7N267Kbr/T3Oyf98HPjczuv+dX5kU3XcBAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBvt//Y+jD2y4YXV0f/nZk6P7f/nQv0T3N+4zL7q/9cEPRvfftu5H0f3xM/eN7p827tXo/rY5N0X3J447PLq/+j8uDO8PRfcPu3RndH/5X4f/f15xd3TfBQBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBqac/ivRR/43lFrovs/fmw4uv8Xv31UdH/1tW+P7s96YVJ0//OXjYzuX379zuj++gv3je7vePbp6P4+r38wun/7S7dH99993gej+xO2PRXdv+usHdH9V/70u9F9FwBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUGow7uO7ow/8/UMbo/vvG7c2uv9nZ70c3b/n7VdH9y9+7CfR/U/PmRHdn3z+v0f3v/69L0f3r77swOj+opWzovsX7T83ur/l58PR/YcWLI7uv3TytdH9/Re/LbrvAgAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASv1/AAAA//+jt3hNDOi3twAAAABJRU5ErkJggg=="
#     # Upload an image
#     try:
#         image_url = client.upload_image(username, image_type, base64_image)
#         print(f"Uploaded Image URL: {image_url}")
#     except Exception as e:
#         print(f"Error uploading image: {e}")

#     # Get all images
#     try:
#         all_images = client.get_all_images()
#         print("All Images:", all_images)
#     except Exception as e:
#         print(f"Error retrieving all images: {e}")

#     # Get images by type
#     try:
#         people_images = client.get_images_by_type(username, "people")
#         print("People Images:", people_images)
#     except Exception as e:
#         print(f"Error retrieving people images: {e}")

#     try:
#         places_images = client.get_images_by_type(username, "places")
#         print("Places Images:", places_images)
#     except Exception as e:
#         print(f"Error retrieving places images: {e}")

#     # Upload an image
#     try:
#         image_url = client.upload_image(username, image_type, base64_image)
#         print(f"Uploaded Image URL: {image_url}")
#     except Exception as e:
#         print(f"Error uploading image: {e}")

#     # Get all images
#     try:
#         all_images = client.get_all_images()
#         print("All Images:", all_images)
#     except Exception as e:
#         print(f"Error retrieving all images: {e}")

#     # Get images by type
#     try:
#         people_images = client.get_images_by_type(username, "people")
#         print("People Images:", people_images)
#     except Exception as e:
#         print(f"Error retrieving people images: {e}")

#     try:
#         places_images = client.get_images_by_type(username, "places")
#         print("Places Images:", places_images)
#     except Exception as e:
#         print(f"Error retrieving places images: {e}")

#     # Update an image
#     try:
#         public_id = "john_doe_people_ad508881-221c-4f74-9f78-49ce978eb28b"
#         new_base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAIAAAB7GkOtAAANG0lEQVR4nOzXj9fXdX3Gcb5xT2+NCKdGLRUVcOmC5tAcDRORbDnTQRvHzUZTwynzR5lLbbrabDVcmkvETMWUOhJuB6d0IM1ZuDaFSNvUMH9k6sYsEIJBnJCxv+I6p3Oux+MPuN7f87nPuZ/nNfT8AR8ZkfT83u+J7g9Nui66f/aeN0b3Z199Z3R//LW3RPe/PXJCdv+Ll0X3d35mXnR/3B8ti+6/d1n298/42p7o/kVz3hzdf/jEKdH9nQu3RPePWfiP0f3XRdcB+KUlAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKDU2cPi36wLn3RedHHDB8anT/5fkro/svXveG6P5b/+u06P6Kf31/dP+gY2dH94++4JPR/ReXvyO6f9K0tdH9BY+Pi+6f9Mxno/tHfnJkdP+SEW+J7u+949bovgsAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACg1dMgVm6MP3H/YM9H9Zw74cHT/pVnzo/urrvrz6P7ytW+K7i9ZuCq6/7Ez1kX393rj30b3N7/h4uj+A1/ZEt2/88Qno/snrfvn6P5Pb1oS3f/u1K3R/aefWBPddwEAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUG1wzOiD6wYfKbo/vPzn9PdP/4Eb8a3R++6IXo/lljr4nu37Z+e3T//CVHRve/sGd0dP+CC8ZH928evzm6f+TMr0b3v/WDndH9q37vw9H9//yt70T3Xzl0RXTfBQBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBo6ftza7AtT743Oj/z5mOj+H+6/ILo/+scTovubHlkd3V9119bo/oTvfyi6v+L7Y6P7C577k+j+301cGt1/70XTovtbFi+K7n/zsJOj++ccd3l0/+Ul34ruuwAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoNHp17QPSB21ddGt0fzF0T3X/9bxwd3R/x+6dE5+955G+i+5vGZL//1w5+Irq/adnU6P7wDxdE94d+sja6P2rjN6L7N267Kbr/T3Oyf98HPjczuv+dX5kU3XcBAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBvt//Y+jD2y4YXV0f/nZk6P7f/nQv0T3N+4zL7q/9cEPRvfftu5H0f3xM/eN7p827tXo/rY5N0X3J447PLq/+j8uDO8PRfcPu3RndH/5X4f/f15xd3TfBQBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBqac/ivRR/43lFrovs/fmw4uv8Xv31UdH/1tW+P7s96YVJ0//OXjYzuX379zuj++gv3je7vePbp6P4+r38wun/7S7dH99993gej+xO2PRXdv+usHdH9V/70u9F9FwBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUGow7uO7ow/8/UMbo/vvG7c2uv9nZ70c3b/n7VdH9y9+7CfR/U/PmRHdn3z+v0f3v/69L0f3r77swOj+opWzovsX7T83ur/l58PR/YcWLI7uv3TytdH9/Re/LbrvAgAoJQAApQQAoJQAAJQSAIBSAgBQSgAASgkAQCkBACglAAClBACglAAAlBIAgFICAFBKAABKCQBAKQEAKCUAAKUEAKCUAACUEgCAUgIAUEoAAEoJAEApAQAoJQAApQQAoJQAAJQSAIBSAgBQSgAASv1/AAAA//+jt3hNDOi3twAAAABJRU5ErkJggg=="
#     except Exception as e:
#         print(f"Error updating image: {e}")
        
#     # Delete an image
#     try:
#         public_id = "john_doe_people_ad508881-221c-4f74-9f78-49ce978eb28b"
#         delete_success = client.delete_image(public_id)
#         print(f"Image deleted: {delete_success}")
#     except Exception as e:
#         print(f"Error deleting image: {e}")

#     # Get image details
#     try:
#         public_id = "john_doe_people_72039f7e-ee78-4acd-81f7-89aebfacaa32"
#         image_details = client.get_image_details(public_id)
#         print("Image Details:", image_details)
#     except Exception as e:
#         print(f"Error retrieving image details: {e}")

# if __name__ == "__main__":
#     main()
