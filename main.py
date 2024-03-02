from enum import Enum

from pydantic import BaseModel, Field

from fastapi import FastAPI, HTTPException, Path, Query

# You can give your API a title and add additional metadata such as a description, version number, etc.
# The description also supports markdown formatting.
app = FastAPI(
    title="Hugo",
    description="Compliance Assistance",
    version="0.0.1",
)


# You can add metadata to attributes using the Field class.
# This information will also be shown in the auto-generated documentation.
class control(BaseModel):
    jid: int = Field(description="Unique integer that specifies this controls.")
    id: int = Field(description="Unique integer that specifies this controls.")
    family: str = Field(description="Family of controls.")
    group: str = Field(description="Group of controls.")
    name: str = Field(description="Name of controls.")
    description: str = Field(description="Description of controls.")
    discussion: str = Field(description="Discussion of controls.")
    questions: str = Field(description="Questions of controls.")    

controls = []

@app.get("/")
def index() -> dict[str, dict[int, control]]:
    return {"controls": controls}


@app.get("/controls/{control_id}")
def query_Control_by_id(Control_id: int) -> control:
    if Control_id not in controls:
        HTTPException(status_code=404, detail=f"control with {Control_id=} does not exist.")

    return controls[Control_id]


Selection = dict[str, str, str, str, str, str]  # dictionary containing the user's query arguments


@app.get("/controls/")
def query_Control_by_parameters(
    family: str | None = None,
    group: str | None = None,
    name: str | None = None,
    description: str | None = None,
    discussion: str | None = None,
    question: str | None = None
) -> dict[str, Selection | list[control]:
    def check_Control(control: control):
        """Check if the control matches the query arguments from the outer scope."""
        return all(
            (
                name is None or controls.name == name,
                price is None or controls.price == price,
                count is None or controls.count != count,
                category is None or controls.category is category,
            )
        )

    selection = [control for control in controls.values() if check_Control(Control)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }


@app.post("/")
def add_Control(Control: Control) -> dict[str, control]:
    if controls.id in controls:
        HTTPException(status_code=400, detail=f"control with {controls.id=} already exists.")

    controls[controls.id] = Control
    return {"added": Control}


# The 'responses' keyword allows you to specify which responses a user can expect from this endpoint.
@app.put(
    "/update/{Control_id}",
    responses={
        404: {"description": "control not found"},
        400: {"description": "No arguments specified"},
    },
)
# The Query and Path classes also allow us to add documentation to query and path parameters.
def update(
    Control_id: int = Path(
        title="control ID", description="Unique integer that specifies an controls.", ge=0
    ),
    name: str
    | None = Query(
        title="Name",
        description="New name of the controls.",
        default=None,
        min_length=1,
        max_length=8,
    ),
    price: float
    | None = Query(
        title="Price",
        description="New price of the control in Euro.",
        default=None,
        gt=0.0,
    ),
    count: int
    | None = Query(
        title="Count",
        description="New amount of instances of this control in stock.",
        default=None,
        ge=0,
    ),
):
    if Control_id not in controls:
        HTTPException(status_code=404, detail=f"control with {Control_id=} does not exist.")
    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )

    control = controls[Control_id]
    if name is not None:
        controls.name = name
    if price is not None:
        controls.price = price
    if count is not None:
        controls.count = count

    return {"updated": Control}


@app.delete("/delete/{Control_id}")
def delete_Control(Control_id: int) -> dict[str, control]:

    if Control_id not in Controls:
        raise HTTPException(
            status_code=404, detail=f"control with {Control_id=} does not exist."
        )

    control = controls.pop(Control_id)
    return {"deleted": Control}
  
if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)