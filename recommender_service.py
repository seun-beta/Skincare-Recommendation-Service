from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vertexai.language_models import TextGenerationModel


app = FastAPI()

generation_model = TextGenerationModel.from_pretrained("text-bison@001")


class SkinTypeQuestions(BaseModel):
    oiliness: str  # e.g., "Does your skin feel oily?"
    dryness: str  # e.g., "Do you experience flakiness or dry patches?"
    sensitivity: str  # e.g., "How does your skin react to new products or environmental changes?"
    hydration: str  # e.g., "Does your skin often feel tight or dehydrated?"

@app.post("/determine-skin-type")
async def determine_skin_type(answers: SkinTypeQuestions):
    try:
        user_responses = f"Oiliness: {answers.oiliness}, Dryness: {answers.dryness}, Sensitivity: {answers.sensitivity}, Hydration: {answers.hydration}"

        # Generate a prompt to interpret the user's answers and determine skin type
        prompt = f"Determine the skin type based on the following user responses: {user_responses}."

        # Query Vertex AI for skin type determination
        completion = generation_model.predict(prompt=f"""          
                         You are a skincare assistant, skilled in determining the skin type of people based on parameters like oiliness, dryness, sensitivity and hydration
                         {prompt}
                        """).text


        detailed_response = completion


        # Parse the response to extract skin type
        skin_type = None
        if "combination skin" in detailed_response.lower():
            skin_type = "combination"
        elif "dry skin" in detailed_response.lower():
            skin_type = "dry"
        elif "oily skin" in detailed_response.lower():
            skin_type = "oily"
        elif "normal skin" in detailed_response.lower():
            skin_type = "normal"
        elif "sensitive skin" in detailed_response.lower():
            skin_type = "sensitive"

        if skin_type:
            return {"skin_type": skin_type}
        else:
            raise ValueError("Unable to determine skin type from the response.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/recommend")
async def recommend_products(skin_type: str):
    # Get current products in stock
    products_in_stock = get_products_in_stock()

    suitable_products = []

    # Evaluate each product for the given skin type
    for product in products_in_stock:
        if product['in_stock']:
            # Prepare a prompt to ask if the product is suitable for the given skin type
            prompt = f"Is the following product suitable for {skin_type} skin? Description: {product['description']}"

            # Query Vertex AI for an evaluation
            completion = generation_model.predict(prompt=f"""          
                            You are a skincare assistant, skilled in recommending skincare products for different skin types.{prompt}
                            """).text

            # Interpret the response
            if "yes" in completion.strip().lower():
                suitable_products.append(product)

    return {"recommendations": suitable_products}

# Dummy function to represent fetching products from your inventory
def get_products_in_stock() -> List[dict]:
    return [
        {"name": "Hydrating Serum", "description": "Provides intense hydration with hyaluronic acid.", "in_stock": True},
        {"name": "Oil Control Lotion", "description": "Lightweight, oil-free lotion for a matte finish.", "in_stock": True},
        {"name": "Gentle Exfoliating Scrub", "description": "Soft scrub suitable for removing dead skin cells.", "in_stock": True},
        {"name": "Sun Protection Cream", "description": "Broad-spectrum SPF 50 cream for all skin types.", "in_stock": True},
        {"name": "Anti-Aging Night Cream", "description": "Rich in retinoids, perfect for mature skin.", "in_stock": True},
        {"name": "Soothing Gel", "description": "Aloe vera gel ideal for calming sensitive skin.", "in_stock": True},
        {"name": "Brightening Essence", "description": "Vitamin C essence for a brighter complexion.", "in_stock": True},
        {"name": "Moisturizing Mask", "description": "Deep moisturizing mask with natural oils.", "in_stock": True},
        {"name": "Pore-Refining Toner", "description": "Toner for minimizing pores and smoothing skin.", "in_stock": True},
        {"name": "Acne Treatment Gel", "description": "Salicylic acid gel for acne-prone skin.", "in_stock": True}

    ]