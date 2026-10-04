from google.genai import types


CREATE_LEAD_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="create_lead",
            description=(
                "Create a customer lead when the customer wants "
                "the travel team to contact them."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "name": types.Schema(
                        type="STRING",
                        description="Customer's name",
                    ),
                    "phone": types.Schema(
                        type="STRING",
                        description="Customer's phone number",
                    ),
                    "message": types.Schema(
                        type="STRING",
                        description="Reason or request from the customer",
                    ),
                },
                required=["name", "phone"],
            ),
        )
    ]
)